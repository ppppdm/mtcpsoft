# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import sys
import fileWatcher
import InfoProcess
import dbManager


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
        if action == 1 and 'jpg' in file:
            print(file)
            do_process_file(file)


def main_server():
    fileWatcher.watchFileChange(DIRECTORY_PATH, handle_change)
    return

if __name__=='__main__':
    print(__file__, 'test')
    
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
