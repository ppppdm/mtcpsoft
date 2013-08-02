# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import os
import sys
import threading

import fileWatcher
import InfoProcess
import dbManager
import readRoadGPS
import mergeManager
import globalConfig
import readCameraEquip
import judgeRunning


def do_process_file(fn):
    infos = do_get_file_infos(fn)
    do_store_db(infos)
    do_merge_file(infos)
    return

def do_get_file_infos(fn):
    infos = InfoProcess.do_get_file_infos(fn)
    return infos

def do_store_db(infos):
    dbManager.store_pic_infos(infos)
    return

def do_merge_file(infos):
    mergeManager.merge_manager(infos)
    return


def handle_change(changes):
    for action, file in changes:
        parent_path = os.path.dirname(os.path.abspath(file))
        if action == 1 and 'jpg' in file and parent_path == fileWatcher.DIRECTORY_PATH:
            print(file)
            do_process_file(file)

def main_server():
    
    # should make sure that just one imgServer run on one machine
    if judgeRunning.program_is_running():
        print('Program is running')
        exit()
    
    # init global variables from file config.ini 
    globalConfig.readConfig()
    
    # init roadgps
    readRoadGPS.initRoadInfo()
    
    # start road info demon
    t = threading.Thread(target=readRoadGPS.roadInfoDaemon)
    t.start()
    
    # init camera_equipment_table
    readCameraEquip.read_camera_equipment()
    
    fileWatcher.watchFileChange(fileWatcher.DIRECTORY_PATH, handle_change)
    return

if __name__=='__main__':
    print('imgInfoGeter imgServer start')
    
    if len(sys.argv) > 1:
        DIRECTORY_PATH = sys.argv[1]
    else:
        DIRECTORY_PATH = '.'
    main_server()




