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



# ---------------------------------------------- DB API --------------------------------------------------

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

# -----------------------------------------------------------------------------------------------------

TIME_DELTA = datetime.timedelta(0, 0, 0, 0, 1)
groupCount = dict()

def isTheFirstOfGroup(camera_id, backup1, captrue_serial_num, collect_date):
    ret = False
    ginfo = groupCount.get(camera_id)
    if  ginfo == None:
        print('group info none')
        groupCount[camera_id] = (backup1, captrue_serial_num, collect_date)
        ret =  True
    elif ginfo[0] < backup1:
        print('date < group info date')
        groupCount[camera_id] = (backup1, captrue_serial_num, collect_date)
        ret = True
    elif ginfo[1] < captrue_serial_num:
        print('num < group info num')
        groupCount[camera_id] = (ginfo[0], captrue_serial_num, collect_date)
        ret = True
    elif (collect_date - ginfo[2] > TIME_DELTA):
        print('time - group info time > ', TIME_DELTA)
        groupCount[camera_id] = (backup1, captrue_serial_num, collect_date)
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
        data_direction        = infos.get('FILE SUB PATH', '')
        road                 = infos.get('ROAD', '')
        road_id              = infos.get('ROAD_ID', '')
        No                   = infos.get('NO.', '0')
        No                   = str(int(No))
        
        #print('collect_dateN', collect_dateN)
        
        try:
            collect_dateN = datetime.datetime.strptime(collect_dateN, '%Y%m%d%H%M%S%f')
        except:
            collect_dateN = datetime.datetime.now()
            
        #print('collect_dateN', collect_dateN)
        
        try:
            recieve_begin_timeN = datetime.datetime.strptime(recieve_begin_timeN, '%Y%m%d%H%M%S%f')
        except:
            recieve_begin_timeN = datetime.datetime.now()
        
        try:
            recieve_timeN = datetime.datetime.strptime(recieve_timeN, '%Y%m%d%H%M%S%f')
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
                if isTheFirstOfGroup(camera_id, backup1, captrue_serial_num, collect_dateN):
                    print(picture_name, 'is the first of group')
                    # change 2013.6.1 
                    if No == '1':
                        recieve_time = 'recieve_time'
                    gps_x = 'gps_x'
                    gps_y = 'gps_y'
                    recieve_picture_nums = 1
                    
                    
                    sql = "INSERT INTO LS_pictures(camera_id, data_direction, picture_name, direction, road, road_id, car_id, license_color, captrue_serial_num, recieve_picture_nums, " + \
                                                collect_date + ',' + \
                                                recieve_begin_time + ',' + \
                                                recieve_time + ',' + \
                                                gps_x + ',' + \
                                                gps_y + ',' + \
                                                car_distance + ',' + \
                                                speed + ',' + \
                                                "create_time, backup1) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    logger.debug(sql)
                    
                
                    cur.execute(sql, 
                            (
                            camera_id, 
                            data_direction, 
                            picture_name,
                            direction,
                            road, 
                            road_id, 
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
                    print(picture_name, 'is not the first of group')
                    sql = "UPDATE LS_pictures SET data_direction = data_direction + ',' + ?, picture_name = picture_name + ',' + ?,recieve_picture_nums = recieve_picture_nums + 1," + \
                                                collect_date + '=?,' + \
                                                recieve_begin_time + '=?,' + \
                                                recieve_time+ '=?,' + \
                                                gps_x + '=?,' + \
                                                gps_y + '=?,' + \
                                                car_distance + '=?,' + \
                                                speed + '=? ' + \
                                                "WHERE (camera_id = ?) and (backup1 = ?) and (captrue_serial_num = ?) and ( ? - collect_date1 < ?)"
                    logger.debug(sql)
                    
                    cur.execute(sql, 
                            (
                            data_direction, 
                            picture_name, 
                            collect_dateN, 
                            recieve_begin_timeN, 
                            recieve_timeN, 
                            gps_xN,
                            gps_yN,
                            car_distanceN,
                            speedN,
                            camera_id, 
                            backup1, 
                            captrue_serial_num, 
                            collect_dateN, 
                            str(TIME_DELTA)
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
