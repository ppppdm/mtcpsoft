# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import dbManager

DATA_FROM_DB = False
ROAD_GPS_POINT_LIST = list()
ROAD_ARC_INFO_LIST = list()

def set_list(data_str):
    global ROAD_GPS_POINT_LIST
    coor_arr = data_str.split('\n')
    for i in coor_arr:
        point = i.split(',')
        ROAD_GPS_POINT_LIST.append(point)
    return

def read_data_from_file(filename):
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        set_list(data)
        
        f.close()
    except Exception as e:
        print(e)
    return


def read_data_from_db():
    global ROAD_GPS_POINT_LIST
    global ROAD_ARC_INFO_LIST
    ret = False
    conn = dbManager.get_one_db_connect()
    if conn:
        cur = conn.cursor()
        
        # read arcpoints
        cur.execute("select LATITUDE, LONGITUDE, ARC_ID from t_arcpoints")
        ROAD_GPS_POINT_LIST = cur.fetchall()
        
        # read arcinfo
        cur.execute("select ID,status,Road_Name,backup1,backup2,Limit_stime,Limit_etime from t_arcinfo")
        ROAD_ARC_INFO_LIST = cur.fetchall()
        
        print('read gps info from db done!')
        ret = True
    
    dbManager.close_one_db_connect(conn)
    return ret

def initRoadGPS(filename):
    if DATA_FROM_DB:
        if read_data_from_db():
            read_data_from_file(filename)
    else:
        read_data_from_file(filename)

if __name__=='__main__':
    
    initRoadGPS('roadgps_hefei.txt')
    print(ROAD_GPS_POINT_LIST)
