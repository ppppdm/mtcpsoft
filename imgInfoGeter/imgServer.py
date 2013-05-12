# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import threading

import fileWatcher
import InfoProcess
import dbManager

def do_init():
    return

def do_watch_file():
    file_name = fileWatcher.watchFileChange()
    return file_name

def do_process_file(fn):
    
    infos = do_get_file_infos(fn)
    
    do_store_db(infos)
    
    return

def do_get_file_infos(fn):
    
    infos = InfoProcess.file_process(fn)
    return infos

def do_store_db(infos):
    dbManager.store(infos)
    return

def main_server():
    
    do_init()
    
    while True:
        fn = do_watch_file()
        
        # start a new thread to process the file
        threading.Thread(target=do_process_file, args=(fn, )).start()
        
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    main_server()
