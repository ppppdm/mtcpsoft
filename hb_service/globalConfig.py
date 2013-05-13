# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import configparser

# Global Values

# network
SERVER_PORT = 44444

# db
DB_HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'

# gpsdata
ROAD_GPS_FILE = 'roadgps.txt'


def readConfig():
    global SERVER_PORT, DB_HOST, USER, PWD, DATABASE, ROAD_GPS_FILE
    
    cf = configparser.ConfigParser()
    print(cf.read('config.ini'))
    print(cf.sections())
    
    SERVER_PORT   = cf.getint('network', 'SERVER_PORT')
    DB_HOST       = cf.get('db', 'DB_HOST')
    USER          = cf.get('db', 'USER')
    PWD           = cf.get('db', 'PWD')
    DATABASE      = cf.get('db', 'DATABASE')
    ROAD_GPS_FILE = cf.get('gpsdata', 'ROAD_GPS_FILE')
    

if __name__=='__main__':
    readConfig()

