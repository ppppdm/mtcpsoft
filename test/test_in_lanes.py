# -*- coding:gbk -*-

ROAD_GPS_POINT_LIST = list()
IS_USE_LANES = True
COFFEE = 0.0001


def is_in_lanes(location):
    if IS_USE_LANES == False:
        # if not use lanes, always return true
        return True
    
    try:
        # the location from camera should be transform from ddmm.mmmm to dd.dddddddd..
        #xd = float(location[0][:2])
        #xm = float(location[0][2:])
        #yd = float(location[1][:3])
        #ym = float(location[1][3:])
        
        #x = xd + xm/60
        #y = yd + ym/60
        
        # the location format is ddmm.mmmm dddmm.mmmm
        x = float(location[0])
        y = float(location[1])
        
        print(x, y)
    except:
        #myLog.mylogger.error('camera location value error! x:%s y:%s'%(location[0][:-1], location[1][:-1]))
        x, y = 0, 0
    
    # the unit of COFFEE is degree, the minute of mCOFFEE = 60*COFFEE
    mCOFFEE = 60*COFFEE
    
    for p in ROAD_GPS_POINT_LIST:
        try:
            rX = float(p[0])
            rY = float(p[1])
        except:
            #myLog.mylogger.error('road gps value error! rX:%s rY:%s'%(p[0], p[1]))
            rX , rY = 0, 0
        if rX - mCOFFEE < x and x < rX + mCOFFEE and rY - mCOFFEE < y and y < rY + mCOFFEE:
            print('camera in lanes')
            #myLog.mylogger.debug('camera in lanes')
            return True
    
    print('camera not in lanes')
    #myLog.mylogger.debug('camera not in lanes')
    return False

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
        #print(ROAD_GPS_POINT_LIST)
        f.close()
    except Exception as e:
        print(e)

if __name__=='__main__':
    print(__file__, 'test')
    gps_file = '../res/roadgps.txt'
    print('GPS FILE :', gps_file)
    initRoadGPS(gps_file)
    
    locations = ('3151.8230', '11717.9183'), ('3151.8234', '11717.9199'), ('3151.8235', '11717.9211')
    for i in locations:
        print(is_in_lanes(i))
    print('done')
