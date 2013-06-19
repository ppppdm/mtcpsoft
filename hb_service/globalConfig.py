# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import configparser

network_ops = ['SERVER_PORT']
db_ops = ['DB_HOST', 'USER', 'PWD', 'DATABASE']
gpsdata_ops = ['ROAD_GPS_FILE']
parameter_ops = ['TIME_UPPER_LIMIT', 'TIME_LOWER_LIMIT', 'COFFEE']

sections = {'network':network_ops, 'db':db_ops, 'gpsdata':gpsdata_ops, 'parameter':parameter_ops}

# Global Values (default value)

# network
SERVER_PORT = 44444

# db
DB_HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'

# gpsdata
ROAD_GPS_FILE = 'roadgps.txt'


#
import processData




def readConfig():
    global SERVER_PORT, DB_HOST, USER, PWD, DATABASE, ROAD_GPS_FILE, TIME_UPPER_LIMIT, TIME_LOWER_LIMIT, COFFEE
    
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    cf.sections()
    
    SERVER_PORT      = cf.getint('network', 'SERVER_PORT')
    DB_HOST          = cf.get('db', 'DB_HOST')
    USER             = cf.get('db', 'USER')
    PWD              = cf.get('db', 'PWD')
    DATABASE         = cf.get('db', 'DATABASE')
    ROAD_GPS_FILE    = cf.get('gpsdata', 'ROAD_GPS_FILE')
    
    processData.TIME_UPPER_LIMIT    = cf.get('parameter', 'TIME_UPPER_LIMIT')
    processData.TIME_LOWER_LIMIT    = cf.get('parameter', 'TIME_LOWER_LIMIT')
    processData.COFFEE              = cf.getfloat('parameter', 'COFFEE')
    processData.IS_USE_LANES        = cf.getboolean('gpsdata', 'IS_USE_LANES')
    processData.IS_USE_VALID_PERIOD = cf.getboolean('parameter', 'IS_USE_VALID_PERIOD')
    
    
    print(SERVER_PORT, DB_HOST, USER, PWD, DATABASE, ROAD_GPS_FILE)

if __name__=='__main__':
    readConfig()

