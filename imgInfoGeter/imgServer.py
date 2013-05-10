# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import fileWatcher
import InfoProcess
import dbManager

def do_init():
    return

def main_server():
    
    do_init()
    
    while True:
        file_name = fileWatcher.watchFileChange()
        
        infos = InfoProcess.file_process(file_name)
        
        dbManager.store(infos)
        
        
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    main_server()
