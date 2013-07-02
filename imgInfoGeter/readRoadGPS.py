# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

ROAD_GPS_FILE = ''
ROAD_ARC_FILE = ''
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

if __name__=='__main__':
    
    initRoadGPS('roadgps_hefei.txt')
    print(ROAD_GPS_POINT_LIST)
