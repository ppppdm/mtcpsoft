# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import dbManager
import globalConfig

DATA_FROM_DB = False
ROAD_GPS_POINT_LIST = list()
ROAD_ARC_INFO_LIST = list()

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
        print('Read road gps from file done')
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
        print('Read road arc info from file done')
    except Exception as e:
        print(e)

def read_data_from_file():
    initRoadGPS(globalConfig.ROAD_GPS_FILE)
    initRoadArc(globalConfig.ROAD_ARC_FILE)

def initRoadGPS_db(cur):
    global ROAD_GPS_POINT_LIST
    # read arcpoints
    try:
        cur.execute("select LATITUDE, LONGITUDE, ARC_ID from t_arcpoints")
        ROAD_GPS_POINT_LIST = cur.fetchall()
        return True
    except:
        return False

def initRoadArc_db(cur):
    global ROAD_ARC_INFO_LIST
    # read arcinfo
    try:
        cur.execute("select ID,status,Road_Name,backup1,backup2,Limit_stime,Limit_etime from t_arcinfo")
        ROAD_ARC_INFO_LIST = cur.fetchall()
        return True
    except:
        return False

def read_data_from_db():
    ret = False
    conn = dbManager.get_db_connect()
    if conn:
        cur = conn.cursor()
        # read arcpoints & # read arcinfo
        if initRoadGPS_db(cur) and initRoadArc_db(cur):
            print('Read gps info from db done!')
            ret = True
        else:
            ret = False
    
    dbManager.close_db_connect(conn)
    return ret

def initRoadInfo():
    print('DATA_FROM_DB', DATA_FROM_DB)
    if DATA_FROM_DB:
        if read_data_from_db() != True:
            read_data_from_file()
    else:
        read_data_from_file()

if __name__=='__main__':
    
    #initRoadGPS('roadgps_hefei.txt')
    print(ROAD_GPS_POINT_LIST)
