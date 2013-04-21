# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import traceback
import datetime

# self module
import myLog


TIME_UPPER_LIMIT = 18
TIME_LOWER_LIMIT = 6

HEART_BEAT_PACKAGE_ITEM = ['HEAD', 'MAC', 'GPS STATUS', 'GPS DATE', 'GPS TIME', 
                           'X', 'Y', 'GPS SPEED', 'GPS DIRCT', 'WORK MODE', 
                           'SERVER IP', 'DEVICE IP', 'HB INTERVAL', 'UPLOAD NUM','TRACK NUM', 
                           'CAR DEFAULT RANGE', 'COMPRESSION FACTOR', 'END' 
                           ]

HEART_BEAT_PACKAGE_ITEM_LEN =[2 , 12, 1, 8, 6, 
                         10, 11, 5, 2, 1, 
                         15, 15, 2, 1, 1, 
                         4, 2, 2
                         ] 
                         
RETURN_PACKAGE_ITEM = ['HEAD', 'CMD', 'WORK MODE', 'SERVER IP', 'DEVICE IP', 
                       'HB INTERVAL', 'UPLOAD NUM', 'TRACK NUM', 'CAR DEFAULT RANGE', 'COMPRESSION FACTOR', 
                       'IS IN LANES', 'IS IN VALID PERIOD', 'END'
                       ]

RETURN_PACKAGE_ITEM_LEN = [2, 1, 1, 15, 15, 
                           2, 1, 1, 4, 2, 
                           1, 1, 2
                           ]   

DEFALUT_PACKAGE_CONTENT = {'HEAD':b'\xaa\x55', 'CMD':b'0', 'WORK MODE':b'0', 'SERVER IP':b'000.000.000.000', 'DEVICE IP':b'000.000.000.000',
                           'HB INTERVAL':b'05', 'UPLOAD NUM':b'4', 'TRACK NUM':b'4', 'CAR DEFAULT RANGE':b'0815', 'COMPRESSION FACTOR':b'70', 
                           'IS IN LANES':b'0', 'IS IN VALID PERIOD':b'0', 'END':b'\xee\x55'
                           }

LIANES_POINTS = list()

COFFEE = 0.01

###################################################################################3
def get_next_item(b_data, i, t):
    return b_data[t:t+i]

def decode_data(b_data):
    s = ''
    t = 0
    
    # skip head and end
    t += 2
    for i in HEART_BEAT_PACKAGE_ITEM_LEN[1:-1]:
        item = get_next_item(b_data, i, t)
        try:
            s += str(item, 'gbk')+'\t'
        except:
            print(traceback.format_exc())
            myLog.mylogger.debug(traceback.format_exc())
        t += i
    myLog.mylogger.debug(s)
    #print(s)
    return s

###################################################################################3

def is_in_lanes(location):
    
    x = float(location[0])
    y = float(location[1])
    
    for p in LIANES_POINTS:
        if p[0] - COFFEE < x and x < p[0] + COFFEE and p[1] - COFFEE < y and y < p[1] + COFFEE:
            return True
    
    return True

def is_valid_period():
    # valid period is 6:00 to 18:00
    tn = datetime.datetime.now().time()
    tu = datetime.time(TIME_UPPER_LIMIT)
    tl = datetime.time(TIME_LOWER_LIMIT)
    
    if tn <= tu and tn >= tl:
       return True 
    return False

def encode_return_data(b_data):
    r_data = bytearray()
    modify_items = {}
    
    # judge wether in the lanes
    location = (b_data[29:39], b_data[39:50])
    if is_in_lanes(location):
        modify_items['IS IN LANES']=b'1'
    
    # judeg wether in valid period
    if is_valid_period():
        modify_items['IS IN VALID PERIOD']=b'1'
    
    for i in RETURN_PACKAGE_ITEM:
        if i not in modify_items:
            r_data += DEFALUT_PACKAGE_CONTENT[i]
        else:
            r_data += modify_items[i]
    
    #print(r_data)
    return r_data

###################################################################################3

def store_to_db(s, conn, cur):
    arr = s.split('\t')
    
    
    if conn and cur:
        
        camera_id = arr[0]
        x = arr[4]
        y = arr[5]
        gpstime = datetime.datetime.strptime(arr[2]+arr[3], '%Y%m%d%H%M%S')
        road = ''
        try:
            mph = float(arr[6])
        except:
            mph = 0
        createtime = datetime.datetime.now()
        try:
            cur.execute("INSERT INTO tbl_heartbeatinfo( ID, camera_id, gpx, gpy, gpstime, roadname, mph, createtime) VALUES (newid(), ?, ?, ?, ?, ?, ?, ?)", 
                (camera_id, x, y, gpstime, road, mph, createtime))
            
        except:
            myLog.mylogger.debug('db excute error!\n')
            print('db excute error!\n')
        
        try:
            conn.commit()
        except:
            myLog.mylogger.debug('commit error!')
            print('commit erorr!')
            
    return


# @ primary
def process_data(b_data, dbconn, cur):
    
    # decode 
    s = decode_data(b_data)
    
    
    # store to db
    store_to_db(s, dbconn, cur)
    
    # encode 
    r_data = encode_return_data(b_data)
    
    return r_data
# 
