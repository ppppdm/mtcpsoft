# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import logging.config
import traceback
import datetime


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
        '''
        try:
            cur                = db_conn.cursor()
            
            camera_id          = infos.get('MAC', '')
            picture_name       = file
            x                  = infos.get('X', '')
            y                  = infos.get('Y', '')
            collect_date1      = infos.get('RTC', '')
            direction          = infos.get('DIRECT', '')
            car_id             = infos.get('CAR LICENSE', '')
            license_color      = infos.get('LICENSE COLOR', '')
            captrue_serial_num = infos.get('SERIAL NUMBER', '')
            minor_captrue_num  = infos.get('NO.', '')
            flag1              = infos.get('CAPTURE FALG', '')
            
            print(camera_id)
            
            if collect_date1 != '':
                collect_date1 = datetime.datetime.strptime(collect_date1, '%Y%m%d%H%M%S%f')
            else:
                collect_date1 = None
            
            #
            cur.execute("""INSERT INTO LS_pictures( camera_id, picture_name) VALUES (?, ?)""", 
                (
                camera_id, 
                picture_name
                ))
        except Exception as e:
            print('db execute error!', e)
            logger.debug('db execute error!')
        
        try:
            db_conn.commit()
            
            
            print(cur.execute('select * from LS_pictures where camera_id=08002812d137').fetchall())
        except Exception as e:
            print('db commit error!', e)
            logger.debug('db commit error!')
        '''
    dbManager.close_db_connect(db_conn)
    
    return

'''
, 
                picture_name, 
                gps_x, 
                gps_y, 
                collect_date1, 
                direction, 
                car_id, 
                license_color, 
                captrue_serial_num, 
                minor_captrue_num, 
                flag1)
                
                , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                
                , 
                picture_name, 
                x, 
                y, 
                collect_date1, 
                direction,
                car_id, 
                license_color, 
                captrue_serial_num, 
                minor_captrue_num, 
                flag1
'''
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
        
    print(infos)
    
    return infos

def file_process(file):
    
    try:
        print('process file')
        f = open(file, 'rb')
    
        infos = get_infos(f)
    
        store_infos(infos, file)
    
        f.close()
    except Exception as e:
        print('file ', file, 'open error!', e)
        logger.debug(e)
        
        print(traceback.format_exc())
    
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
    infos = {'MAC': '08002812d137', 'CAR DISTENCE': '40', 'RTC': '20130417105109823', 'SERIAL NUMBER': '001\x02', 'Y': '1848.3899,', 'X': '157.7773,', 'CAR LICENSE': '誂0D928\x00'}
    store_infos(infos, '../res/2013041710510982-d137-0001-3.jpg')
    
