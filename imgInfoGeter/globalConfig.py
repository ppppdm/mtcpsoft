# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import os
import configparser

import fileWatcher
import InfoProcess
import dbManager
import readRoadGPS
import mergeManager

# network


def readConfig():
    
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    cf.sections()
    
    
    dbManager.DB_HOST              = cf.get('db', 'DB_HOST')
    dbManager.USER                 = cf.get('db', 'USER')
    dbManager.PWD                  = cf.get('db', 'PWD')
    dbManager.DATABASE             = cf.get('db', 'DATABASE')
    fileWatcher.DIRECTORY_PATH                 = cf.get('parameter', 'DIRECTORY_PATH')
    InfoProcess.MOVE_FILE          = cf.getboolean('rename', 'MOVE_FILE')
    InfoProcess.RENAME_BY_EQUIP    = cf.getboolean('rename', 'RENAME_BY_EQUIP')
    InfoProcess.MOVE_FLODER        = cf.get('rename', 'MOVE_FLODER')
    InfoProcess.CAMERA_EQUIP_FILE  = cf.get('rename', 'CAMERA_EQUIP_FILE')
    InfoProcess.RENAME_BY_DATE     = cf.get('rename', 'RENAME_BY_DATE')
    InfoProcess.USING_IMG_COMPLETE = cf.getboolean('parameter', 'USING_IMG_COMPLETE')
    InfoProcess.TIME_WAIT_FOR_FTP  = cf.getint('parameter', 'TIME_WAIT_FOR_FTP')
    InfoProcess.COFFEE             = cf.getfloat('parameter', 'COFFEE')
    readRoadGPS.ROAD_GPS_FILE      = cf.get('parameter', 'ROAD_GPS_FILE')
    readRoadGPS.ROAD_ARC_FILE      = cf.get('parameter', 'ROAD_ARC_FILE')
    readRoadGPS.DATA_FROM_DB       = cf.getboolean('parameter', 'DATA_FROM_DB')
    mergeManager.DO_MERGE          = cf.getboolean('merge', 'DO_MERGE')
    mergeManager.GROUP_PIC_NUM     = cf.getint('merge', 'GROUP_PIC_NUM')
    mergeManager.MERGE_PICS_PATH   = cf.get('merge', 'MERGE_PICS_PATH')
    
    # Standardization the user input
    fileWatcher.DIRECTORY_PATH = os.path.abspath(fileWatcher.DIRECTORY_PATH)
    InfoProcess.MOVE_FLODER = os.path.abspath(InfoProcess.MOVE_FLODER) + os.path.sep
    
    
    # print configration
    print('watch floder :', fileWatcher.DIRECTORY_PATH)
    print('is rename    :', InfoProcess.MOVE_FILE)
    print('rename floder:', InfoProcess.MOVE_FLODER)
    print('time wait for ftp:', InfoProcess.TIME_WAIT_FOR_FTP)
    print('do merge pic :', mergeManager.DO_MERGE)
    print('merge pic path:', mergeManager.MERGE_PICS_PATH)

