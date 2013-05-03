# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import logging.config
import datetime
import os
import time

logging.config.fileConfig("logging.conf")

#create logger
logger = logging.getLogger("example")

# self module
import dbManager

BEFORE_INFO_LEN = 6
INFO_LEN        = 89
TOTAL_MARK_LEN  = 124

INFO_ITMES = ['MAC', 'RTC', 'X', 'Y', 'SPEED', 
              'DIRECT', 'CAR LICENSE', 'LICENSE COLOR', 'CAR DISTENCE', 'SERIAL NUMBER', 
              'NO.', 'CAPTURE FALG'
              ]

INFO_ITEM_LEN = [12, 17, 10, 11, 5, 
                 2, 16, 8, 2, 4, 
                 1, 1
                 ]

MAX_WAIT_OPEN_TIME = 600 # second
EACH_WAIT_OPEN_TIME = 20

# read file and get info in the image
# before the info we want there is 6 bytes file head
# after that is the info we want, the item of info see
# the INFO_ITMES, each item's len see the INFO_ITEM_LEN


def store_infos(infos, file):
    
    # store to logfile
    logger.debug(infos)
    
    # store to db
    db_conn = dbManager.get_db_connect()
    if db_conn:
        
        try:
            cur                = db_conn.cursor()
            
            camera_id          = infos.get('MAC', '')
            picture_name       = os.path.basename(file)
            gps_x              = infos.get('X', '')
            gps_y              = infos.get('Y', '')
            direction          = infos.get('DIRECT', '')
            collect_date1      = infos.get('RTC', '')
            car_id             = infos.get('CAR LICENSE', '')
            license_color      = infos.get('LICENSE COLOR', '')
            captrue_serial_num = infos.get('SERIAL NUMBER', '')
            minor_captrue_num  = infos.get('NO.', '')
            flag1              = infos.get('CAPTURE FALG', '')
            
            try:
                collect_date1 = datetime.datetime.strptime(collect_date1, '%Y%m%d%H%M%S%f')
            except:
                collect_date1 = datetime.datetime.now()

            recieve_time = collect_date1 = datetime.datetime.now()

            cur.execute("INSERT INTO LS_pictures(camera_id, picture_name, gps_x, gps_y, direction, collect_date1, car_id, license_color, captrue_serial_num, minor_captrue_num, flag1, recieve_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
                (
                camera_id, 
                picture_name,
                gps_x,
                gps_y, 
                direction, 
                collect_date1, 
                car_id, 
                license_color, 
                captrue_serial_num, 
                minor_captrue_num, 
                flag1,
                recieve_time
                ))
            
        except: # just not print db error
            print('db execute error!')
            logger.debug('db execute error!')
            logger.error('Error file:%s', file)
        
        try:
            db_conn.commit()
            
        except: # just not print db error
            print('db commit error!')
            logger.debug('db commit error!')
            logger.error('Error file:%s', file)
    else:
        # get db connect none
        print('get db connect error!')
        logger.debug('get db connect error!')
        logger.error('Error file:%s', file)
        
    dbManager.close_db_connect(db_conn)
    
    return

def get_infos(f):
    infos = {}
    
    # in test print the info
    f.seek(BEFORE_INFO_LEN)
    b_data = f.read(INFO_LEN)
    logger.debug(b_data)
    #
    
    
    f.seek(BEFORE_INFO_LEN)
    
    for i in INFO_ITMES:
        item_len = INFO_ITEM_LEN[INFO_ITMES.index(i)]
        b_data = f.read(item_len)
        try:
            if i == 'CAR LICENSE':
                b_data = b_data[:8]
            if i == 'LICENSE COLOR':
                b_data = b_data[:2]
            if i == 'X' or i == 'Y':
                b_data = b_data[:-1]
            #infos.append((i, str(b_data, 'gbk')))
            infos[i] = str(b_data, 'gbk')
        except Exception as e:
            print('decode item %s error!'%(i), e)
            logger.debug(e)
        
    #print(infos)
    
    return infos

def file_process(file):
    
    
    print('process file')
    total = 0
    while MAX_WAIT_OPEN_TIME > total:
        # try open file, if ok then process data
        # else sleep for next open
        try:
            f = open(file, 'rb')
            print('open file ok')
            
            infos = get_infos(f)
            print(infos)
            # get info done ,file could close
            f.close()
            
            store_infos(infos, file)
            
            break
        except:
            time.sleep(EACH_WAIT_OPEN_TIME)
            total+=EACH_WAIT_OPEN_TIME
    
    if MAX_WAIT_OPEN_TIME <= total:
        print('open file false, permission denied.')
        logger.debug('open file false, permission denied.')
        logger.error('Error file:%s', file)
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    t = 0
    for i in INFO_ITEM_LEN:
        t += i
    print(t)
    '''
    TEST_FILES = ['../res/1.jpg', '../res/2013041710510982-d137-0001-3.jpg']
    for i in TEST_FILES:
        file_process(i)
    '''
    # test insert to db
    infos = {'MAC': '08002812d137', 'CAR DISTENCE': '40', 'RTC': '20130417105109823', 'SERIAL NUMBER': '001\x02', 'Y': '1848.3899,', 'X': '157.7773,', 'CAR LICENSE': '誂0D928\x00', 'LICENSE COLOR':'蓝'}
    store_infos(infos, '../res/2013041710510982-d137-0001-3.jpg')
    
    infos = {'MAC': '08002812d137', 'CAR DISTENCE': '40', 'RTC': '20134417105109823', 'SERIAL NUMBER': '001\x02', 'Y': '1848.3899,', 'X': '157.7773,', 'CAR LICENSE': '誂0D928\x00', 'LICENSE COLOR':'蓝'}
    store_infos(infos, '../res/2013041710510982-d137-0001-3.jpg')
    
