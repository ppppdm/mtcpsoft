# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import time
import datetime
import dbManager
import threading

DATA_FROM_DB = False
ROAD_GPS_FILE = ''
ROAD_ARC_FILE = ''
ROAD_GPS_POINT_LIST = list()
ROAD_ARC_INFO_LIST = list()

READ_DB_ROAD_INFO_SLEEP_TIME = 3600 # sec

ROAD_GPS_LOCK = threading.Lock()

LAST_UPDATE_TIME = None


def set_list(data_str):
    l = list()
    coor_arr = data_str.split('\n')
    for i in coor_arr:
        point = i.split(',')
        l.append(point)
    return l

def initRoadGPS(filename):
    global ROAD_GPS_POINT_LIST
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        ROAD_GPS_POINT_LIST = set_list(data)
        
        f.close()
        print('read road gps done')
    except Exception as e:
        print(e)

def initRoadArc(filename):
    global ROAD_ARC_INFO_LIST
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        ROAD_ARC_INFO_LIST = set_list(data)
        
        f.close()
        print('read road arc info done')
    except Exception as e:
        print(e)

def initRoadGPS_db(cur):
    global ROAD_GPS_POINT_LIST
    # read arcpoints
    cur.execute("select LATITUDE, LONGITUDE, ARC_ID from t_arcpoints")
    ROAD_GPS_POINT_LIST = cur.fetchall()

def initRoadArc_db(cur):
    global ROAD_ARC_INFO_LIST
   # read arcinfo
    cur.execute("select ID,status,Road_Name,backup1,backup2,Limit_stime,Limit_etime from t_arcinfo")
    ROAD_ARC_INFO_LIST = cur.fetchall()

def read_data_from_db():
    global LAST_UPDATE_TIME
    ret = False
    conn = dbManager.get_db_connect()
    if conn:
        cur = conn.cursor()
        initRoadGPS_db(cur)
        initRoadArc_db(cur)
        print('read gps info from db done!')
        
        LAST_UPDATE_TIME = datetime.datetime.now()
        ret = True
    
    dbManager.close_db_connect(conn)
    return ret

def read_data_from_file():
    initRoadGPS(ROAD_GPS_FILE)
    initRoadArc(ROAD_ARC_FILE)
    return

def initRoadInfo():
    print('DATA_FROM_DB', DATA_FROM_DB)
    if DATA_FROM_DB:
        if read_data_from_db() != True:
            read_data_from_file()
    else:
        read_data_from_file()

def get_last_update_db():
    luu = datetime.datetime(1, 1, 1)
    conn = dbManager.get_db_connect()
    if conn:
        cur = conn.cursor()
        sql = "SELECT last_user_update FROM sys.dm_db_index_usage_stats WHERE object_id=object_id('t_arcinfo') and database_id = db_id('CDMTCP')"
        cur.execute(sql)
        rec = cur.fetchone()
        t_arcinfo_luu  = rec[0]
        
        sql = "SELECT last_user_update FROM sys.dm_db_index_usage_stats WHERE object_id=object_id('t_arcpoints') and database_id = db_id('CDMTCP')"
        cur.execute(sql)
        rec = cur.fetchone()
        t_arcpoints_luu = rec[0]
        
        if t_arcinfo_luu > t_arcpoints_luu:
            luu = t_arcinfo_luu
        else:
            luu = t_arcpoints_luu
        
        
        
    dbManager.close_db_connect(conn)
    return luu

def needUpdate():
    global LAST_UPDATE_TIME
    if LAST_UPDATE_TIME == None:
        return True
    luu = get_last_update_db()
    if luu > LAST_UPDATE_TIME:
        LAST_UPDATE_TIME = luu
        return True
    
    return False

def roadInfoDaemon():
    while DATA_FROM_DB:
        time.sleep(READ_DB_ROAD_INFO_SLEEP_TIME)
        # if t_arcpoints or t_arcinfo updated, then update road info
        # use sys.dm_db_index_usage_stats, the system table of SQL Server
        if needUpdate():
            #ROAD_GPS_LOCK.acquire()
            read_data_from_db()
            #ROAD_GPS_LOCK.release()
            print('update roadinfo from db')
        else:
            print('not needed update roadinfo')

if __name__=='__main__':
    initRoadGPS('roadgps_hefei.txt')
    print(ROAD_GPS_POINT_LIST)
