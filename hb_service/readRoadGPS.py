# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


ROAD_GPS_POINT_LIST = list()

ROAD_GPS_FILE = 'roadgps.txt'


def set_list(data_str):
    global ROAD_GPS_POINT_LIST
    coor_arr = data_str.split('\n')
    for i in coor_arr:
        point = i.split(',')
        ROAD_GPS_POINT_LIST.append(point)
    return

def initRoadGPS(filename):
    try:
        f = open(filename, 'rt')
        
        data = f.read()
        # set ROAD_GPS_POINT_LIST with data
        set_list(data)
        
        f.close()
    except Exception as e:
        print(e)

if __name__=='__main__':
    initRoadGPS(ROAD_GPS_FILE)
