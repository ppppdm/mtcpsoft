# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

DO_UPDATE = False

import datetime
import myLog
import dbUpdater

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
    #sql = "update tbl_heartbeatinfo_new set gpx = ?, gpy = ?, gpstime = ?, roadname = ?, mph = ?, createtime = ? where (camera_id = ?)"
    
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
    
    dbUpdater.q.put((gpx, gpy, gpstime, roadname, mph, createtime, camera_id))
    return



# @ primary
def process_db(infos, dbconn, cur):
    
    # store to db
    store_to_db(infos, dbconn, cur)
    
    # update data to heartbeatinfo_new
    if DO_UPDATE:
        #update_to_heartbeatinfo_new(infos, dbconn, cur)
        put_to_dbUpdater_quuee(infos)
    
    return
