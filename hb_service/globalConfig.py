# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import configparser

import dbManager

network_ops = ['SERVER_PORT']
db_ops = ['DB_HOST', 'USER', 'PWD', 'DATABASE']
gpsdata_ops = ['ROAD_GPS_FILE']
parameter_ops = ['TIME_UPPER_LIMIT', 'TIME_LOWER_LIMIT', 'COFFEE']

sections = {'network':network_ops, 'db':db_ops, 'gpsdata':gpsdata_ops, 'parameter':parameter_ops}

# Global Values (default value)

# network
SERVER_PORT = 44444

# db
#DB_HOST = '10.20.1.200' # '210.73.152.201'
#USER = 'sa'
#PWD = 'sa'
#DATABASE = 'CDMTCP'

# gpsdata
ROAD_GPS_FILE = 'roadgps.txt'
ROAD_ARC_FILE = 'arcinfo.txt'

#
import processData
import readRoadGPS




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
    processData.DO_UPDATE           = cf.getboolean('parameter', 'DO_UPDATE')
    readRoadGPS.DATA_FROM_DB        = cf.getboolean('gpsdata', 'DATA_FROM_DB')
    
    print('SERVER_PORT:', SERVER_PORT)
    print('DB:', dbManager.DB_HOST, dbManager.USER, dbManager.PWD, dbManager.DATABASE)
    print('ROAD_GPS_FILE:', ROAD_GPS_FILE)
    print('ROAD_ARC_FILE:', ROAD_ARC_FILE)
    print('Read Config Done')

if __name__=='__main__':
    readConfig()

