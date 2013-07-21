# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import traceback
import datetime

# self module
import myLog
import readRoadGPS
import dbUpdater


TIME_UPPER_LIMIT = 18
TIME_LOWER_LIMIT = 6

HEART_BEAT_PACKAGE_ITEM = ['HEAD', 'MAC', 'GPS STATUS', 'GPS DATE', 'GPS TIME', 
                           'X', 'Y', 'GPS SPEED', 'GPS DIRCT', 'WORK MODE', 
                           'SERVER IP', 'DEVICE IP', 'HB INTERVAL', 'UPLOAD NUM','TRACK NUM', 
                           'CAR DEFAULT RANGE', 'COMPRESSION FACTOR', 'END' 
                           ]

HEART_BEAT_PACKAGE_ITEM_LEN_old =[2 , 12, 1, 8, 6, 
                         10, 11, 5, 2, 1, 
                         15, 15, 2, 1, 1, 
                         4, 2, 2
                         ] 

HEART_BEAT_PACKAGE_ITEM_LEN = {'HEAD':2, 'MAC':12, 'GPS STATUS':1, 'GPS DATE':8, 'GPS TIME':6, 
                           'X':10, 'Y':11, 'GPS SPEED':5, 'GPS DIRCT':2, 'WORK MODE':1, 
                           'SERVER IP':15, 'DEVICE IP':15, 'HB INTERVAL':2, 'UPLOAD NUM':1,'TRACK NUM':1, 
                           'CAR DEFAULT RANGE':4, 'COMPRESSION FACTOR':2, 'END':2 }
                         
RETURN_PACKAGE_ITEM = ['HEAD', 'CMD', 'WORK MODE', 'SERVER IP', 'DEVICE IP', 
                       'HB INTERVAL', 'UPLOAD NUM', 'TRACK NUM', 'CAR DEFAULT RANGE', 'COMPRESSION FACTOR', 
                       'IS IN LANES', 'IS IN VALID PERIOD', 'END'
                       ]

RETURN_PACKAGE_ITEM_LEN = [2, 1, 1, 15, 15, 
                           2, 1, 1, 4, 2, 
                           1, 1, 2
                           ]   

DEFALUT_PACKAGE_CONTENT = {'HEAD':b'\xaa\x55', 'CMD':b'0', 'WORK MODE':b'0', 'SERVER IP':b'000.000.000.000', 'DEVICE IP':b'000.000.000.000',
                           'HB INTERVAL':b'05', 'UPLOAD NUM':b'4', 'TRACK NUM':b'4', 'CAR DEFAULT RANGE':b'0815', 'COMPRESSION FACTOR':b'70', 
                           'IS IN LANES':b'0', 'IS IN VALID PERIOD':b'0', 'END':b'\xee\x55'
                           }


COFFEE = 0.0001
IS_USE_LANES = False
IS_USE_VALID_PERIOD = False
DO_UPDATE = False
ROAD_TIME_TYPE_Tidal = '8a9481d03f79b7d6013f7a0948310002'
ROAD_TIME_TYPE_Daytime = '8a9481d03f79b7d6013f7a0948310003'

###################################################################################3
def get_next_item(b_data, i, t):
    return b_data[t:t+i]

def changeToFormate(data):
    '12-34-56-78-90-ab'
    data = data[0:2] + '-' + data[2:4] + '-' + data[4:6] + '-' + data[6:8] + '-' + data[8:10] + '-' + data[10:12]
    return data

def get_road_id_from_location(location):
    road_id = ''
    try:
        # the location format is ddmm.mmmm dddmm.mmmm
        x = float(location[0])
        y = float(location[1])
    except:
        myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    # the unit of COFFEE is degree, the minute of mCOFFEE = 60*COFFEE
    mCOFFEE = 60*COFFEE
    
    for p in readRoadGPS.ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        try:
            rID = p[2]
        except:
            myLog.mylogger.error('road gps have no name')
            rID = ''
        if rX - mCOFFEE < x and x < rX + mCOFFEE and rY - mCOFFEE < y and y < rY + mCOFFEE:
            road_id = rID
            return road_id
    
    return road_id

def get_road_arcinfo_by_id(road_id):
    if road_id == '':
        return None
    
    arc_info = None
    for i in readRoadGPS.ROAD_ARC_INFO_LIST:
        if road_id == i[0]:
            arc_info = i
    return arc_info

def decode_data(b_data):
    #s = ''
    infos = {}
    t = 2 # skip head and end
    
    for i in HEART_BEAT_PACKAGE_ITEM[1:-1]:
        item_len = HEART_BEAT_PACKAGE_ITEM_LEN[i]
        b_item = get_next_item(b_data, item_len, t)
        try:
            if i == 'X' or i == 'Y':
                b_item = b_item[:-1]
            
            # convert to str
            item = str(b_item, 'gbk')
            
            if i == 'MAC':
                item = changeToFormate(item)
            
            
            #s += item + '\t'
            infos[i] = item
        except:
            #print(traceback.format_exc())
            myLog.mylogger.error(traceback.format_exc())
        t+=item_len
    
    # get the road ID info if is in lanes
    location = (infos['X'], infos['Y'])
    road_id = get_road_id_from_location(location)
    infos['ROAD_ID'] = road_id
    
    
    # get road arcinfo by road ID
    arcinfo = get_road_arcinfo_by_id(road_id)
    if arcinfo:
        infos['ROAD STATUS'] = arcinfo[1]
        infos['ROAD'] = arcinfo[2]
        infos['ROAD TIME_TYPE'] = arcinfo[3]
        infos['ROAD TIME '] = arcinfo[4]
        infos['ROAD sTIME'] = arcinfo[5]
        infos['ROAD eTIME'] = arcinfo[6]
    
    #myLog.mylogger.debug(s)
    myLog.mylogger.debug(infos)
    
    return infos

###################################################################################3

def is_in_lanes(location):
    if IS_USE_LANES == False:
        # if not use lanes, always return true
        return True
    
    try:
        # the location from camera should be transform from ddmm.mmmm to dd.dddddddd..
        #xd = float(location[0][:2])
        #xm = float(location[0][2:])
        #yd = float(location[1][:3])
        #ym = float(location[1][3:])
        
        #x = xd + xm/60
        #y = yd + ym/60
        
        # the location format is ddmm.mmmm dddmm.mmmm
        x = float(location[0])
        y = float(location[1])
    except:
        myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    # the unit of COFFEE is degree, the minute of mCOFFEE = 60*COFFEE
    mCOFFEE = 60*COFFEE
    
    for p in readRoadGPS.ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        if rX - mCOFFEE < x and x < rX + mCOFFEE and rY - mCOFFEE < y and y < rY + mCOFFEE:
            print('camera in lanes')
            myLog.mylogger.debug('camera in lanes')
            return True
    
    print('camera not in lanes')
    myLog.mylogger.debug('camera not in lanes')
    return False

def is_valid_period():
    if IS_USE_VALID_PERIOD == False:
        # if not use valid preiod, always reutrn true
        return True
    
    # valid period is 6:00 to 18:00
    tn = datetime.datetime.now().time()
    tu = datetime.time(TIME_UPPER_LIMIT)
    tl = datetime.time(TIME_LOWER_LIMIT)
    
    if tn <= tu and tn >= tl:
        print('camera in valid_period')
        myLog.mylogger.debug('camera in valid_period')
        return True 
    
    print('camera not in valid_period')
    myLog.mylogger.debug('camera not in valid_period')
    return False

def is_in_lanes_new(infos):
    if IS_USE_LANES == False:
        # if not use lanes, always return true
        return True
    
    road_id = infos['ROAD_ID']
    if road_id != '':
        road_status = infos['ROAD STATUS']
        if road_status == 0:
            return True
    
    return False

def get_time_last(time_str):
    time_arr = time_str.split('至')
    low = time_arr[0].split(':')
    up = time_arr[1].split(':')
    try:
        l_time = datetime.time(int(low[0]),int(low[1]))
        u_time = datetime.time(int(up[0]),int(up[1]))
        return l_time,u_time
    except:
        l_time = datetime.time(0)
        u_time = datetime.time(0)
        return l_time,u_time

def is_valid_period_new(infos):
    if IS_USE_VALID_PERIOD == False:
        # if not use valid preiod, always reutrn true
        return True
    
    road_id = infos['ROAD_ID']
    if road_id != '':
        road_status = infos['ROAD STATUS']
        if road_status == 0:
            road_time_type = infos['ROAD TIME_TYPE']
            if road_time_type == ROAD_TIME_TYPE_Tidal:
                tn = datetime.datetime.now().time()
                print(road_time_type)
                limit_stime = infos['ROAD sTIME']
                limit_etime = infos['ROAD eTIME']
                lsl,lsu = get_time_last(limit_stime)
                lel,leu = get_time_last(limit_etime)
                if ( lsl < tn and tn < lsu) or (lel < tn and leu):
                    return True
            if road_time_type == ROAD_TIME_TYPE_Daytime:
                tn = datetime.datetime.now().time()
                print(road_time_type)
                road_time = infos['ROAD TIME']
                rtl, rtu = get_time_last(road_time)
                if rtl < tn and tn < rtu:
                    return True
                
    return False

def encode_return_data(infos, changed_args=dict()):
    r_data = bytearray()
    modify_items = {}
    
    # judge wether in the lanes
    #location = (infos['X'], infos['Y'])
    #if is_in_lanes(location):
    #    modify_items['IS IN LANES']=b'1'
    
    if is_in_lanes_new(infos):
        modify_items['IS IN LANES']=b'1'
    
    # judeg wether in valid period
    #if is_valid_period():
    #    modify_items['IS IN VALID PERIOD']=b'1'
    
    # CMD
    if len(changed_args) != 0:
         modify_items['CMD'] = b'1'
    
    # Server IP
    if 'SERVER IP' in changed_args:
        modify_items['SERVER IP'] = changed_args['SERVER IP'] # should have 15 chars
    else:
        modify_items['SERVER IP'] = bytes(infos.get('SERVER IP','000.000.000.000'), 'gbk')
    
    # HB INTERVAL
    if 'HB INTERVAL' in changed_args:
        modify_items['HB INTERVAL'] = changed_args['HB INTERVAL']
    else:
        modify_items['HB INTERVAL'] = bytes(infos['HB INTERVAL'], 'gbk')
    
    # UPLOAD NUM
    if 'UPLOAD NUM' in changed_args:
        modify_items['UPLOAD NUM'] = changed_args['UPLOAD NUM']
    else:
        modify_items['UPLOAD NUM'] = bytes(infos['UPLOAD NUM'], 'gbk')
    
    # TRACK NUM
    if 'TRACK NUM' in changed_args:
        modify_items['TRACK NUM'] = changed_args['TRACK NUM']
    else:
        modify_items['TRACK NUM'] = bytes(infos['TRACK NUM'], 'gbk')
    
    # CAR DEFAULT RANGE
    if 'CAR DEFAULT RANGE' in changed_args:
        modify_items['CAR DEFAULT RANGE'] = changed_args['CAR DEFAULT RANGE']
    else:

        modify_items['CAR DEFAULT RANGE'] = bytes(infos['CAR DEFAULT RANGE'], 'gbk')
    
    # COMPRESSION FACTOR
    if 'COMPRESSION FACTOR' in changed_args:
        modify_items['COMPRESSION FACTOR'] = changed_args['COMPRESSION FACTOR']
    else:
        modify_items['COMPRESSION FACTOR'] = bytes(infos['COMPRESSION FACTOR'], 'gbk')
    
    for i in RETURN_PACKAGE_ITEM:
        if i not in modify_items:
            r_data += DEFALUT_PACKAGE_CONTENT[i]
        else:
            r_data += modify_items[i]
    
    #print(r_data)
    myLog.mylogger.debug(r_data)
    return r_data

###################################################################################3

def store_to_db(infos, conn, cur):
    
    if conn and cur:

        try:
            gpstime = datetime.datetime.strptime(infos['GPS DATE']+infos['GPS TIME'], '%Y%m%d%H%M%S')
        except:
            gpstime = datetime.datetime.now()
        
        try:
            mph = float(infos.get('GPS SPEED', '0'))
        except:
            mph = 0
        
        try:
            hb_interval = float(infos.get('HB INTERVAL', '5'))
        except:
            hb_interval = 5
        
        try:
            upload_num = int(infos.get('UPLOAD NUM', '3'))
        except:
            upload_num = 3
        
        try:
            track_num  = int(infos.get('TRACK NUM', '3'))
        except:
            track_num = 3
        
        try:
            compression_factor  = float(infos.get('COMPRESSION FACTOR', '5'))
        except:
            compression_factor = 3
        
        camera_id    = infos.get('MAC', 'ID error')
        x            = infos.get('X', 'X error')
        y            = infos.get('Y', 'Y error')
        road         = infos.get('ROAD', '')
        direction    = infos.get('GPS DIRCT', 'ss')
        car_distance = infos.get('CAR DEFAULT RANGE', '')
        createtime   = datetime.datetime.now()
        
        print(gpstime, camera_id, x, y, road, mph)
        myLog.mylogger.debug('%s %s %s %s %s %s', gpstime, camera_id, x, y, road, mph)
        
        try:
            cur.execute("INSERT INTO tbl_heartbeatinfo( ID, camera_id, gpx, gpy, gpstime, roadname, mph, createtime, direction, hb_interval, upload_num, track_num, car_distance, compression_factor) VALUES (newid(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (camera_id, x, y, gpstime, road, mph, createtime, direction, hb_interval, upload_num, track_num, car_distance, compression_factor))
            
        except:
            myLog.mylogger.error('db excute error! %s\n', infos)
            print('db excute error!\n')
            return
            
        try:
            conn.commit()
            myLog.mylogger.debug('store to db success!')
        except:
            myLog.mylogger.error('commit error! %s\n', infos)
            print('commit erorr!')
            
    return

def update_to_heartbeatinfo_new(infos, conn, cur):
    if conn and cur:
        try:
            gpstime = datetime.datetime.strptime(infos['GPS DATE']+infos['GPS TIME'], '%Y%m%d%H%M%S')
        except:
            gpstime = datetime.datetime.now()
        
        try:
            mph = float(infos.get('GPS SPEED', '0'))
        except:
            mph = 0
        '''
        try:
            hb_interval = float(infos.get('HB INTERVAL', '0'))
        except:
            hb_interval = 5
        
        try:
            upload_num = int(infos.get('UPLOAD NUM', '0'))
        except:
            upload_num = 3
        
        try:
            track_num  = int(infos.get('TRACK NUM', '0'))
        except:
            track_num = 3
        
        try:
            compression_factor  = float(infos.get('COMPRESSION FACTOR', '0'))
        except:
            compression_factor = 3
        '''
        
        camera_id    = infos.get('MAC', '')
        gpx          = infos.get('X', '')
        gpy          = infos.get('Y', '')
        roadname     = infos.get('ROAD', '')
        #direction    = infos.get('GPS DIRCT', '')
        #car_distance = infos.get('CAR DEFAULT RANGE', '')
        createtime   = datetime.datetime.now()
        
        #print(gpstime, camera_id, gpx, gpy, road, mph)
        #myLog.mylogger.debug('%s %s %s %s %s %s', gpstime, camera_id, x, y, road, mph)
        
        try:
            sql = "update tbl_heartbeatinfo_new set gpx = ?, gpy = ?, gpstime = ?, roadname = ?, mph = ?, createtime = ? where (camera_id = ?)"
            cur.execute(sql, gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
            
        except:
            myLog.mylogger.error('db excute error! %s\n', infos)
            print('db excute error!\n')
            return
        try:
            conn.commit()
            myLog.mylogger.debug('store to db success!')
        except:
            myLog.mylogger.error('commit error! %s\n', infos)
            print('commit erorr!')
    return

def put_to_dbUpdater_quuee(infos):
    sql = "update tbl_heartbeatinfo_new set gpx = ?, gpy = ?, gpstime = ?, roadname = ?, mph = ?, createtime = ? where (camera_id = ?)"
    
    try:
        gpstime = datetime.datetime.strptime(infos['GPS DATE']+infos['GPS TIME'], '%Y%m%d%H%M%S')
    except:
        gpstime = datetime.datetime.now()
        
    try:
        mph = float(infos.get('GPS SPEED', '0'))
    except:
        mph = 0
    
    camera_id    = infos.get('MAC', '')
    gpx          = infos.get('X', '')
    gpy          = infos.get('Y', '')
    roadname     = infos.get('ROAD', '')
    createtime   = datetime.datetime.now()
    
    dbUpdater.q.put((sql, gpx, gpy, gpstime, roadname, mph, createtime, camera_id))
    return

# @ primary
def process_data(b_data, dbconn, cur):
    
    # decode 
    infos = decode_data(b_data)
    
    
    # store to db
    store_to_db(infos, dbconn, cur)
    
    # update data to heartbeatinfo_new
    if DO_UPDATE:
        #update_to_heartbeatinfo_new(infos, dbconn, cur)
        put_to_dbUpdater_quuee(infos)
    
    # encode 
    r_data = encode_return_data(infos)
    
    return r_data
# 
