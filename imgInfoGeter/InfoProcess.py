# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import logging.config
import traceback

logging.config.fileConfig("logging.conf")

#create logger
logger = logging.getLogger("example")

# self module

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
def store_infos(infos):
    
    return


def get_infos(f):
    infos = []
    
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
            infos.append((i, str(b_data, 'gbk')))
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
    
        store_infos(infos)
    
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
    
    TEST_FILES = ['../res/1.jpg', '../res/2013041710510982-d137-0001-3.jpg']
    for i in TEST_FILES:
        file_process(i)
    
