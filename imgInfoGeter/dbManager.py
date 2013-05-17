# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import os
import InfoProcess


try:
    import pyodbc
except:
    print('no module pyodbc, should init first!')

logging.config.fileConfig("logging.conf")

#create logger
logger = logging.getLogger("example")

DB_HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'

def get_db_connect():
    db_conn = None
    try:
        db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    except: # not print db execption yet
        logger.debug('init db got an error!')
        print('init db got an error!')
    return db_conn

def close_db_connect(db_conn):
    if db_conn:
        db_conn.close()

'''

DB_CONNECT_LOCK = threading.Lock()

MAX_DB_CONNECT = 10
DB_CONNECT_NOT_USE_LIST = list()
DB_CONNECT_USED_LIST = list()

def init_db_connect_list():
    for i in range(MAX_DB_CONNECT):
        try:
            db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_NOT_USE_LIST.append(db_conn)
            # release lock
            DB_CONNECT_LOCK.release()
        except: # not print db execption yet
            logger.debug('init db got an error!')
            print('init db got an error!')
            break
    print('init db conn done!')
    logger.debug('init db conn done!')
    return

def get_one_db_connect():
    db_conn = None
    try:
        # lock
        DB_CONNECT_LOCK.acquire()
        db_conn = DB_CONNECT_NOT_USE_LIST.pop()
        DB_CONNECT_USED_LIST.append(db_conn)
        # release lock
        DB_CONNECT_LOCK.release()
        
    except ValueError:
        print('not enough db_conn!')
        logger.debug('not enough db_conn!')
    except Exception as e:
        print(e)
        logger.debug(e)
    return db_conn

def close_one_db_connect(conn):
    if conn:
        # if the conn is usable
        try:
            conn.commit()
        except : # not print db except  yet
            print('connect can not used')
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_USED_LIST.remove(conn)
            # release lock
            DB_CONNECT_LOCK.release()
            return
        
        try:
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_USED_LIST.remove(conn)
            DB_CONNECT_NOT_USE_LIST.append(conn)
            # release lock
            DB_CONNECT_LOCK.release()
        except Exception as e:
            print(e)
            logger.debug(e)
    return
'''

import datetime
#import os
def store_group_infos(groupinfos):
    
    
    # store to db
    if groupinfos:
        # store to logfile
        logger.debug(groupinfos)
        
        infos                = groupinfos[0]   # use the first info in group
        camera_id            = infos.get('MAC', '')
        gps_x                = infos.get('X', '')
        gps_y                = infos.get('Y', '')
        direction            = infos.get('DIRECT', '')
        collect_date1        = infos.get('RTC', '')
        car_id               = infos.get('CAR LICENSE', '')
        license_color        = infos.get('LICENSE COLOR', '')
        captrue_serial_num   = infos.get('SERIAL NUMBER', '')
        minor_captrue_num    = infos.get('NO.', '')
        flag1                = infos.get('CAPTURE FALG', '')
        recieve_picture_nums = len(groupinfos)
        
        if recieve_picture_nums == InfoProcess.GROUP_COMPLETE_NUM:
            flag             = 1
        else:
            flag             = 0
        
        try:
            collect_date1 = datetime.datetime.strptime(collect_date1, '%Y%m%d%H%M%S%f')
        except:
            collect_date1 = datetime.datetime.now()

        recieve_time = datetime.datetime.now()
        
        picture_name = ''
        for i in groupinfos:
            fn = i.get('FILE', '')
            if fn != '':
                picture_name += os.path.abspath(fn) + ','
            
        #print('picture_name', picture_name)
        
        db_conn = get_db_connect()
        if db_conn:
            cur                  = db_conn.cursor()
            try:
                cur.execute("INSERT INTO LS_pictures(camera_id, picture_name, gps_x, gps_y, direction, collect_date1, flag, car_id, license_color, captrue_serial_num, minor_captrue_num, flag1, recieve_time, recieve_picture_nums) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                    (
                    camera_id, 
                    picture_name,
                    gps_x,
                    gps_y, 
                    direction, 
                    collect_date1, 
                    flag, 
                    car_id, 
                    license_color, 
                    captrue_serial_num, 
                    minor_captrue_num, 
                    flag1,
                    recieve_time, 
                    recieve_picture_nums
                    ))
            
            except: # just not print db error
                print('db execute error!')
                logger.debug('db execute error! %s', groupinfos)
                logger.error('db execute error! %s', groupinfos)
        
            try:
                db_conn.commit()
            
            except: # just not print db error
                print('db commit error!')
                logger.debug('db commit error! %s', groupinfos)
                logger.error('db commit error! %s', groupinfos)
        else:
            # get db connect none
            print('get db connect error!')
            logger.debug('get db connect error! %s', groupinfos)
            logger.error('get db connect error! %s', groupinfos)
        
        close_db_connect(db_conn)
    else:
        print('group info none')
    return

def isTheFirstOfGroup():
    return False

# store one image infos
def store_pic_infos(infos):
    
    # store to db
    if infos:
        # store to logfile
        logger.debug(infos)
        
        camera_id            = infos.get('MAC', '')
        gps_xN               = infos.get('X', '')
        gps_yN               = infos.get('Y', '')
        direction            = infos.get('DIRECT', '')
        collect_dateN        = infos.get('RTC', '')
        car_id               = infos.get('CAR LICENSE', '')
        license_color        = infos.get('LICENSE COLOR', '')
        captrue_serial_num   = infos.get('SERIAL NUMBER', '')
        recieve_begin_timeN  = infos.get('CREATE TIME', '')
        receive_timeN        = infos.get('MODIFY TIME', '')
        car_distanceN        = infos.get('CAR DISTENCE', '')
        speedN               = infos.get('SPEED', '')
        backup1              = infos.get('DATE', '')
        picture_name         = infos.get('FILE', '')
        
        try:
            collect_dateN = datetime.datetime.strptime(collect_dateN, '%Y%m%d%H%M%S%f')
        except:
            collect_dateN = datetime.datetime.now()

        create_time = datetime.datetime.now()
        
        #print('picture_name', picture_name)
        
        db_conn = get_db_connect()
        if db_conn:
            cur                  = db_conn.cursor()
            try:
                if isTheFirstOfGroup():
                
                    recieve_picture_nums = 1
                
                    cur.execute("INSERT INTO LS_pictures(camera_id, picture_name, direction, car_id, license_color, captrue_serial_num, recieve_picture_nums, collect_dateN, recieve_begin_timeN, receive_timeN, gps_xN, gps_yN, car_distanceN , speedN, create_time ,backup1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                            (
                            camera_id, 
                            picture_name,
                            direction,
                            car_id, 
                            license_color, 
                            captrue_serial_num, 
                            recieve_picture_nums, 
                            collect_dateN, 
                            recieve_begin_timeN,
                            receive_timeN,
                            gps_xN,
                            gps_yN,
                            car_distanceN,
                            speedN,
                            create_time,
                            backup1
                            ))
                else:
                    cur.execute("UPDATE LS_pictures SET picture_name = picture_name + ?,receive_picture_nums = recieve_picture_nums + 1,collect_dateN = ?,recieve_begin_timeN = ?,receive_timeN = ?,gps_xN = ?,gps_yN = ?,car_distanceN = ?,speedN = ?,create_time = ?WHERE (camera_id = ?,backup1 = ?,capture_serial_num = ?)", 
                            (
                            picture_name, 
                            collect_dateN, 
                            recieve_begin_timeN, 
                            receive_timeN, 
                            gps_xN,
                            gps_yN,
                            car_distanceN,
                            speedN,
                            create_time, 
                            camera_id, 
                            backup1, 
                            captrue_serial_num
                            ))
            except:
                print('db execute error!')
                logger.debug('db execute error! %s', infos)
                logger.error('db execute error! %s', infos)
            
            try:
                db_conn.commit()
            
            except: # just not print db error
                print('db commit error!')
                logger.debug('db commit error! %s', infos)
                logger.error('db commit error! %s', infos)
                
        else:
            # get db connect none
            print('get db connect error!')
            logger.debug('get db connect error! %s', infos)
            logger.error('get db connect error! %s', infos)
        
        close_db_connect(db_conn)
    else:
        print('group info none')
    
    return
