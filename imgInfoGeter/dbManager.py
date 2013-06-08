# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import logging.config
import datetime

try:
    import pyodbc
except:
    print('no module pyodbc, should init first!')

# create logger
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example")

# global variabls
DB_HOST = '10.20.1.129' # '210.73.152.201'
USER = 'sa'
PWD = 'skcl@2013'
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


groupCount = dict()

def isTheFirstOfGroup(camera_id, backup1, captrue_serial_num):
    ret = False
    ginfo = groupCount.get(camera_id)
    if  ginfo == None:
        groupCount[camera_id] = (backup1, captrue_serial_num)
        ret =  True
    elif ginfo[0] < backup1:
        groupCount[camera_id] = (backup1, captrue_serial_num)
        ret = True
    elif ginfo[1] < captrue_serial_num:
        groupCount[camera_id] = (ginfo[0], captrue_serial_num)
        ret = True
    
    return ret

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
        recieve_timeN        = infos.get('MODIFY TIME', '')
        car_distanceN        = infos.get('CAR DISTENCE', '')
        speedN               = infos.get('SPEED', '')
        backup1              = infos.get('DATE', '')
        picture_name         = infos.get('FILE', '')
        No                   = infos.get('NO.', '0')
        No                   = str(int(No))
        
        #print('collect_dateN', collect_dateN)
        
        try:
            collect_dateN = datetime.datetime.strptime(collect_dateN, '%Y%m%d%H%M%S%f')
        except:
            collect_dateN = datetime.datetime.now()
            
        #print('collect_dateN', collect_dateN)
        
        try:
            recieve_begin_timeN = datetime.datetime.strptime(collect_dateN, '%Y%m%d%H%M%S%f')
        except:
            recieve_begin_timeN = datetime.datetime.now()
        
        try:
            recieve_timeN = datetime.datetime.strptime(collect_dateN, '%Y%m%d%H%M%S%f')
        except:
            recieve_timeN = datetime.datetime.now()

        create_time = datetime.datetime.now()
        
        #print('picture_name', picture_name)
        
        collect_date = 'collect_date' + No
        recieve_begin_time = 'recieve_begin_time' + No
        recieve_time = 'recieve_time' + No
        gps_x = 'gps_x' + No
        gps_y = 'gps_y' + No
        car_distance = 'car_distance' + No
        speed = 'speed' + No
        
        # change backup1 type to str
        backup1 = backup1.strftime('%Y-%m-%d')
        
        db_conn = get_db_connect()
        if db_conn:
            cur              = db_conn.cursor()
            try:
                if isTheFirstOfGroup(camera_id, backup1, captrue_serial_num):
                    # change 2013.6.1 
                    recieve_time = 'recieve_time'
                    gps_x = 'gps_x'
                    gps_y = 'gps_y'
                    recieve_picture_nums = 1
                    
                    
                    sql = "INSERT INTO LS_pictures(camera_id, picture_name, direction, car_id, license_color, captrue_serial_num, recieve_picture_nums, " + \
                                                collect_date + ',' + \
                                                recieve_begin_time + ',' + \
                                                recieve_time + ',' + \
                                                gps_x + ',' + \
                                                gps_y + ',' + \
                                                car_distance + ',' + \
                                                speed + ',' + \
                                                "create_time, backup1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    logger.debug(sql)
                    
                
                    cur.execute(sql, 
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
                            recieve_timeN, 
                            gps_xN,
                            gps_yN,
                            car_distanceN,
                            speedN, 
                            create_time, 
                            backup1
                            ))
                else:
                    
                    sql = "UPDATE LS_pictures SET picture_name = picture_name + ',' + ?,recieve_picture_nums = recieve_picture_nums + 1," + \
                                                collect_date + '=?,' + \
                                                recieve_begin_time + '=?,' + \
                                                recieve_time+ '=?,' + \
                                                gps_x + '=?,' + \
                                                gps_y + '=?,' + \
                                                car_distance + '=?,' + \
                                                speed + '=?,' + \
                                                "create_time = ? WHERE (camera_id = ?) and (backup1 = ?) and (captrue_serial_num = ?)"
                    logger.debug(sql)
                    
                    cur.execute(sql, 
                            (
                            picture_name, 
                            collect_dateN, 
                            recieve_begin_timeN, 
                            recieve_timeN, 
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
        logger.debug('info none')
    
    return
