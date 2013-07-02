# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

ROAD_GPS_POINT_LIST = list()
ROAD_ARC_INFO_LIST = list()
COFFEE = 0.0005


def set_list(data_str):
    l = list()
    coor_arr = data_str.split('\n')
    for i in coor_arr:
        point = i.split(',')
        l.append(point)
    #print(len(ROAD_GPS_POINT_LIST))
    return l

def initRoadGPS(filename):
    global ROAD_GPS_POINT_LIST
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        ROAD_GPS_POINT_LIST = set_list(data)
        
        f.close()
    except Exception as e:
        print(e)

def initRoadArc(filename):
    global ROAD_ARC_INFO_LIST
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        ROAD_ARC_INFO_LIST = set_list(data)
        
        f.close()
    except Exception as e:
        print(e)

def is_in_lanes(location):
    try:
        print(location[0], location[1])
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
        
        #print(x, y)
    except:
        #myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    # the unit of COFFEE is degree, the minute of mCOFFEE = 60*COFFEE
    mCOFFEE = 60*COFFEE
    
    for p in ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            #myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        if rX - mCOFFEE < x and x < rX + mCOFFEE and rY - mCOFFEE < y and y < rY + mCOFFEE:
            print('camera in lanes')
            #myLog.mylogger.debug('camera in lanes')
            print(get_road_arcinfo_by_id(p[2])[2])
            return True
    
    print('camera not in lanes')
    #myLog.mylogger.debug('camera not in lanes')
    return False

def is_in_lanes_old(location):
    try:
        print(location[0], location[1])
        # the location from camera should be transform from ddmm.mmmm to dd.dddddddd..
        xd = float(location[0][:2])
        xm = float(location[0][2:])
        yd = float(location[1][:3])
        ym = float(location[1][3:])
        
        x = xd + xm/60
        y = yd + ym/60
        #print(x, y)
    except:
        #myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    for p in ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            #myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        if rX - COFFEE < x and x < rX + COFFEE and rY - COFFEE < y and y < rY + COFFEE:
            print('camera in lanes')
            #myLog.mylogger.debug('camera in lanes')
            print(p[2])
            return True
    
    print('camera not in lanes')
    #myLog.mylogger.debug('camera not in lanes')
    return False

def get_road_arcinfo_by_id(road_id):
    arc_info = None
    for i in ROAD_ARC_INFO_LIST:
        if road_id == i[0]:
            arc_info = i
    return arc_info

#----------------------------------------------------------------------------
# read log file gps data

locations = list()
logfile = open('rotate_log.txt', 'rt')
while True:
    ss = logfile.readline()
    if ss == '':
        break
    if 'X' in ss:
        index1 = ss.find('X')
        index2 = ss.find('Y')
        x = ss[index1+5:index1+14]
        y = ss[index2+5:index2+15]
        #print(x, y)
        locations.append((x, y))


OLD = 1
if OLD:
    initRoadGPS('roadgps_22_heifei.txt')
    for i in locations:
        print(is_in_lanes_old(i))
else:
    initRoadArc('arcinfo_heifei.txt')
    initRoadGPS('arcinfo_db.txt')
    for i in locations:
        print(is_in_lanes(i))

    
