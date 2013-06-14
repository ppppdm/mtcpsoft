# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import os
import sys
import configparser

import fileWatcher
import InfoProcess
import dbManager

DIRECTORY_PATH = ''

def do_process_file(fn):
    infos = do_get_file_infos(fn)
    do_store_db(infos)
    return

def do_get_file_infos(fn):
    infos = InfoProcess.do_get_file_infos(fn)
    return infos

def do_store_db(infos):
    dbManager.store_pic_infos(infos)
    return


def handle_change(changes):
    for action, file in changes:
        parent_path = os.path.dirname(os.path.abspath(file))
        if action == 1 and 'jpg' in file and parent_path == DIRECTORY_PATH:
            print(file)
            do_process_file(file)

def readConfig():
    global DIRECTORY_PATH
    
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    cf.sections()
    
    
    dbManager.DB_HOST          = cf.get('db', 'DB_HOST')
    dbManager.USER             = cf.get('db', 'USER')
    dbManager.PWD              = cf.get('db', 'PWD')
    dbManager.DATABASE         = cf.get('db', 'DATABASE')
    DIRECTORY_PATH             = cf.get('parameter', 'DIRECTORY_PATH')
    
    # Standardization the user input
    DIRECTORY_PATH = os.path.abspath(DIRECTORY_PATH)

def main_server():
    
    # init global variables from file config.ini 
    readConfig()
    
    print('watch foder:', DIRECTORY_PATH)
    fileWatcher.watchFileChange(DIRECTORY_PATH, handle_change)
    return

if __name__=='__main__':
    print('imgInfoGeter imgServer start')
    
    if len(sys.argv) > 1:
        DIRECTORY_PATH = sys.argv[1]
    else:
        DIRECTORY_PATH = '.'
    main_server()
    
    ''' # test do process
    fl = ['../res/5.3/20130503170514-db98-0002-1.jpg', 
          '../res/5.3/20130503170514-db98-0002-2.jpg', 
          '../res/5.3/20130503170515-db98-0002-3.jpg']
    for i in fl:
        print(i)
        print(do_process_file(i))
    '''
