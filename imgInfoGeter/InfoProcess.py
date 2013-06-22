# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import logging.config
import datetime
import os
import time


#create logger
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example")


# Global variabls
MOVE_FILE = False
RENAME_BY_EQUIP = False
CAMERAID_EQUIPMENTID = dict()
CAMERA_EQUIP_FILE = ''
MOVE_FLODER = os.path.abspath('../PICS/')+os.path.sep

USING_IMG_COMPLETE = False
MODIFY_LAST_BYTE_RTC = False


BEFORE_INFO_LEN = 6
INFO_LEN        = 89
TOTAL_MARK_LEN  = 124
TIME_WAIT_FOR_FTP = 60

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

def changeToFormate(data):
    data = data[0:2] + b'-' + data[2:4] + b'-' + data[4:6] + b'-' + data[6:8] + b'-' + data[8:10] + b'-' + data[10:12]
    return data

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
            if i == 'MAC':
                b_data = changeToFormate(b_data)
            #infos.append((i, str(b_data, 'gbk')))
            infos[i] = str(b_data, 'gbk')
        except:
            #print('decode item %s error!'%(i), b_data)
            logger.debug('decode item %s error! %s'%(i, str(b_data)))
            
    #print(infos)
    return infos

def do_open_file(fn):
    while True:
        # check the file content's length, if not have the infomation ,close and wait
        if os.path.getsize(fn) < BEFORE_INFO_LEN + INFO_LEN:
            time.sleep(EACH_WAIT_OPEN_TIME)
            continue
        try:
            f = open(fn, 'rb')
            break;
        except:
            time.sleep(EACH_WAIT_OPEN_TIME)
    return f

def get_file_time(fn):
    file_st = os.stat(fn)
    return datetime.datetime.fromtimestamp(file_st.st_mtime), datetime.datetime.fromtimestamp(file_st.st_ctime)

def isImageComplete(f):
    # if not use this function always return True
    if USING_IMG_COMPLETE == False:
        return True
    
    # the image file formate is JPEG
    # find the sign of end of image (0xFF 0xD9), if found return true
    ret = False
    f.seek(0)
    
    buff = f.read()
    #print('now len is ', f.tell())
    if b'\xff\xd9' in buff:
        ret = True
    f.seek(0)
    return ret

def rename_file(fn, infos):
    print('Is move file', MOVE_FILE)
    if MOVE_FILE:
        if RENAME_BY_EQUIP:
            camera_id = infos['MAC'].upper()
            print(camera_id)
            # There should change to equipment_id with camera_id
            equipment_id = CAMERAID_EQUIPMENTID.get(camera_id, '000000000000')
        
        
            date = infos['DATE'].strftime('%y%m%d%H%M%S')
            number = infos['NO.']
            new_fn = MOVE_FLODER + equipment_id + '-' + date + '-0-000000000000-00000-000-3-' + number + '.jpg'
        else:
            new_fn = MOVE_FLODER + os.path.basename(fn)
        
        old_fn = os.path.abspath(fn)
        # new file should in another directory, else will find the new file created
        os.rename(old_fn, new_fn)
    
        return new_fn
    else:
        return fn

def do_get_file_infos(fn):
    
    # open the file
    f = do_open_file(fn)
    
    # Determine the integrity of the image file
    # As the image file has not upload completed when open and read it ,
    # we should sleep and wait for the file upload complete.
    
    # sleep 120 second 
    time.sleep(TIME_WAIT_FOR_FTP)
    
    isCmp = isImageComplete(f)
    print(isCmp)
    if isCmp != True:
        logger.error('Error file Img Not Complete:%s', fn)
        f.close()
        return None
    
    infos = get_infos(f)
    
    # close the file after get the info inside 
    f.close()
    
    # get the file create_time and last_modify_time
    m_time, c_time = get_file_time(fn)
    infos['MODIFY TIME'] = m_time
    infos['CREATE TIME'] = c_time
    
    # modify the RTC last byte
    if MODIFY_LAST_BYTE_RTC:
        rtc = infos.get('RTC', '')
        if rtc != '' and rtc[-1] > '9':
            infos['RTC'] = rtc[:-1] + '9'
    
    # get the date
    pic_date = infos.get('RTC', '')
    if pic_date == '':
        pic_date = datetime.datetime.now().date() 
    else:
        #print(pic_date)
        try:
            pic_date = datetime.datetime.strptime(pic_date, '%Y%m%d%H%M%S%f').date()
        except:
            pic_date = datetime.datetime.now().date()
    
    infos['DATE'] = pic_date
    #infos['FILE'] = os.path.basename(fn)
    
    # rename the pic file
    new_fn = rename_file(fn, infos)
    infos['FILE'] = os.path.basename(new_fn)
    
    return infos

if __name__=='__main__':
    print(__file__, 'test')
    
    t = 0
    for i in INFO_ITEM_LEN:
        t += i
    print(t)

    
    fl = ['../res/5.3/20130503170514-db98-0002-1.jpg', 
          '../res/5.3/20130503170514-db98-0002-2.jpg', 
          '../res/5.3/20130503170516-db98-0003-1.jpg']
    for i in fl:
        print(i)
        print(do_get_file_infos(i))

