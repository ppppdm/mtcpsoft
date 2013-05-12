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

GROUP_COMPLETE_NUM = 3

g_info_group = {}
g_file_pre_name = None

class infoarray:
    def __init__(self):
        self.array = list()
        self.flag = 0
        self.count = 0
        return
    
    def store_one_info(self, fn, infos):
        
        infos['FILE'] = os.path.abspath(fn)
        self.array.append(infos)
        
        return
    
    def get_group_info(self):
        ret = None
        base = self.array[0]
        dt = base['RTC'][0:8]       # date
        gn = base['SERIAL NUMBER']  # group number
        self.count = 1
        
        for i in self.array[1:]:
            if i['RTC'][0:8] != dt or i['SERIAL NUMBER'] != gn:
                self.flag = 1
            else:
                self.count += 1
        
        if self.flag == 1 or self.count == GROUP_COMPLETE_NUM:
            ret = self.array[:self.count]
            self.array = self.array[self.count:]
            self.flag = 0
        return ret
    
    def get_array(self):
        return self.array

g_info_array = infoarray()

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

def do_open_file(fn):
    while True:
        try:
            f = open(fn, 'rb')
            break;
        except:
            time.sleep(EACH_WAIT_OPEN_TIME)
    return f

def do_get_file_infos(fn):
    
    # open the file
    f = do_open_file(fn)
    
    infos = get_infos(f)
    
    # close the file after get the info inside 
    f.close()
    
    # store the infos to group
    g_info_array.store_one_info(fn, infos)
    
    
    # retrun info group
    re = g_info_array.get_group_info()
    
    # just has a problem when the last group of picture is not complete
    # some day , this grop may return when the next day picture come.
    
    return re

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
    
    # test insert to db
    infos = {'MAC': '08002812d137', 'CAR DISTENCE': '40', 'RTC': '20130417105109823', 'SERIAL NUMBER': '001\x02', 'Y': '1848.3899,', 'X': '157.7773,', 'CAR LICENSE': '誂0D928\x00', 'LICENSE COLOR':'蓝'}
    store_infos(infos, '../res/2013041710510982-d137-0001-3.jpg')
    
    infos = {'MAC': '08002812d137', 'CAR DISTENCE': '40', 'RTC': '20134417105109823', 'SERIAL NUMBER': '001\x02', 'Y': '1848.3899,', 'X': '157.7773,', 'CAR LICENSE': '誂0D928\x00', 'LICENSE COLOR':'蓝'}
    store_infos(infos, '../res/2013041710510982-d137-0001-3.jpg')
    '''
    
    fl = ['../res/5.3/20130503170514-db98-0002-1.jpg', 
          '../res/5.3/20130503170514-db98-0002-2.jpg', 
          '../res/5.3/20130503170516-db98-0003-1.jpg']
    for i in fl:
        print(i)
        print(do_get_file_infos(i))
    
    print(g_info_array.get_array())
