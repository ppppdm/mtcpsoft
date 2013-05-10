# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import fileWatcher

def do_init():
    return

def main_server():
    
    do_init()
    
    while True:
        fileWatcher.watchFileChange()
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    main_server()
