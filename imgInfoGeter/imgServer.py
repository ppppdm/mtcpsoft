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
    dbManager.store_group_infos(infos)
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
    
