# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

ROAD_GPS_POINT_LIST = list()
COFFEE = 0.001


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

def is_in_lanes(location):
    try:
        # the location from camera should be transform from ddmm.mmmm to dd.dddddddd..
        xd = float(location[0][:2])
        xm = float(location[0][2:-1])
        yd = float(location[1][:3])
        ym = float(location[1][3:-1])
        
        x = xd + xm/60
        y = yd + ym/60
        print(x, y)
    except:
        #myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    for p in ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            #myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        if rX - COFFEE < x and x < rX + COFFEE and rY - COFFEE < y and y < rY + COFFEE:
            print('camera in lanes')
            #myLog.mylogger.debug('camera in lanes')
            print(p[2])
            return True
    
    print('camera not in lanes')
    #myLog.mylogger.debug('camera not in lanes')
    return False

#----------------------------------------------------------------------------
# read log file gps data

locations = list()
logfile = open('rotate_log.txt', 'rt')
while True:
    ss = logfile.readline()
    if ss == '':
        break
    if 'X' in ss:
        index1 = ss.find('X')
        index2 = ss.find('Y')
        x = ss[index1+5:index1+14]
        y = ss[index2+5:index2+15]
        print(x, y)
        locations.append((x, y))


# read raodgps_hefei.txt
initRoadGPS('roadgps_hefei.txt')
#print(ROAD_GPS_POINT_LIST)


# calculate
for i in locations:
    print(is_in_lanes(i))
    
