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

# process parameter 
TIME_UPPER_LIMIT = 18
TIME_LOWER_LIMIT = 6
COFFEE = 0.01



def readConfig():
    global SERVER_PORT, DB_HOST, USER, PWD, DATABASE, ROAD_GPS_FILE, TIME_UPPER_LIMIT, TIME_LOWER_LIMIT, COFFEE
    
    cf = configparser.ConfigParser()
    print(cf.read('config.ini'))
    print(cf.sections())
    
    SERVER_PORT      = cf.getint('network', 'SERVER_PORT')
    DB_HOST          = cf.get('db', 'DB_HOST')
    USER             = cf.get('db', 'USER')
    PWD              = cf.get('db', 'PWD')
    DATABASE         = cf.get('db', 'DATABASE')
    ROAD_GPS_FILE    = cf.get('gpsdata', 'ROAD_GPS_FILE')
    TIME_UPPER_LIMIT = cf.get('parameter', 'TIME_UPPER_LIMIT')
    TIME_LOWER_LIMIT = cf.get('parameter', 'TIME_LOWER_LIMIT')
    COFFEE           = cf.get('parameter', 'COFFEE')
    

if __name__=='__main__':
    readConfig()

