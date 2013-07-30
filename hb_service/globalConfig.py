# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import configparser
import dbManager
import processData
import readRoadGPS
import processDB

# network
SERVER_PORT = 44444
ROAD_GPS_FILE = 'roadgps.txt'
ROAD_ARC_FILE = 'arcinfo.txt'


def readConfig():
    global SERVER_PORT, ROAD_GPS_FILE, ROAD_ARC_FILE
    
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    cf.sections()
    
    SERVER_PORT      = cf.getint('network', 'SERVER_PORT')
    dbManager.DB_HOST          = cf.get('db', 'DB_HOST')
    dbManager.USER             = cf.get('db', 'USER')
    dbManager.PWD              = cf.get('db', 'PWD')
    dbManager.DATABASE         = cf.get('db', 'DATABASE')
    ROAD_GPS_FILE    = cf.get('gpsdata', 'ROAD_GPS_FILE')
    ROAD_ARC_FILE    = cf.get('gpsdata', 'ROAD_ARC_FILE')
    
    processData.TIME_UPPER_LIMIT    = cf.getint('parameter', 'TIME_UPPER_LIMIT')
    processData.TIME_LOWER_LIMIT    = cf.getint('parameter', 'TIME_LOWER_LIMIT')
    processData.COFFEE              = cf.getfloat('parameter', 'COFFEE')
    processData.IS_USE_LANES        = cf.getboolean('gpsdata', 'IS_USE_LANES')
    processData.IS_USE_VALID_PERIOD = cf.getboolean('parameter', 'IS_USE_VALID_PERIOD')
    processDB.DO_UPDATE           = cf.getboolean('parameter', 'DO_UPDATE')
    readRoadGPS.DATA_FROM_DB        = cf.getboolean('gpsdata', 'DATA_FROM_DB')
    
    print('SERVER_PORT:', SERVER_PORT)
    print('DB:', dbManager.DB_HOST, dbManager.USER, dbManager.PWD, dbManager.DATABASE)
    print('ROAD_GPS_FILE:', ROAD_GPS_FILE)
    print('ROAD_ARC_FILE:', ROAD_ARC_FILE)
    print('Read Config Done')

if __name__=='__main__':
    readConfig()

