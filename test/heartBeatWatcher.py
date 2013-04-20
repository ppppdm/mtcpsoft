# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import logging
import socket
import threading
import datetime
import traceback

# Global Variables
HOST = socket.gethostbyname(socket.gethostname()) #socket.INADDR_ANY
SERVER_PORT = 44444
REMOTE_CONTROL_PORT = 6320

TIME_UPPER_LIMIT = 18
TIME_LOWER_LIMIT = 6

LOG_FILE   = 'log.txt'
LOG_LEVEL  = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(levelname)s %(thread)d %(message)s"
logging.basicConfig(filename = LOG_FILE, 
                    level    = LOG_LEVEL, 
                    format   = LOG_FORMAT)

log = logging.getLogger(__name__)

SIMPLE_RETURN_FRAME = b'\xaa\x55\x00'

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
                           'IS IN LANES':b'0', 'IS IN VALID PERIOD':b'0', 'END':b'\xee\x55'}

remote_control_client_list = []

MAX_DB_CONNECT = 1000
DB_CONNECT_NOT_USE_LIST = list()
DB_CONNECT_USED_LIST = list()

def init_db_connect_list():
    for i in range(MAX_DB_CONNECT):
        try:
            db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
            DB_CONNECT_NOT_USE_LIST.append(db_conn)
        except: # not print db execption yet
            #log.debug(e)
            #print(e)
            break
    print('init db conn done!')
    return

def get_one_db_connect():
    db_conn = None
    try:
        db_conn = DB_CONNECT_NOT_USE_LIST.pop()
        DB_CONNECT_USED_LIST.append(db_conn)
    except ValueError:
        print('not enough db_conn!')
        log.debug('not enough db_conn!')
    except Exception as e:
        print(e)
        log.debug(e)
    return db_conn

def close_one_db_connect(conn):
    if conn:
        # if the conn is usable
        try:
            conn.commit()
        except : # db except not print yet
            log.debug('connect can not used')
            print('connect can not used')
            DB_CONNECT_USED_LIST.remove(conn)
            return
        
        try:
            DB_CONNECT_USED_LIST.remove(conn)
            DB_CONNECT_NOT_USE_LIST.append(conn)
        except Exception as e:
            log.debug(e)
            print(e)
    return



g_db_conn_lock = threading.Lock()

try:
    import pyodbc
    DB_HOST = '10.20.1.200' # '210.73.152.201'
    USER = 'sa'
    PWD = 'sa'
    DATABASE = 'CDMTCP'

    #conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    #print(conn)
except:
    log.debug(traceback.foormat_exc())
    #conn = None

def send_to_remote(b_data):
    for conn in remote_control_client_list:
        try:
            conn.send(b_data)
        except:
            print(traceback.format_exc())
            log.debug(traceback.format_exc())
            remote_control_client_list.remove(conn)
            conn.close()

def get_next_item(b_data, i, t):
    return b_data[t:t+i]

def process_data(b_data):
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
            log.debug(traceback.format_exc())
        t += i    
    log.debug(s)
    print(s)
    return s

def is_in_lanes(location):
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
    
    print(r_data)
    return r_data

def get_db_conn():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    except:
        conn = None
    return conn
    
def close_db_conn(conn):
    if conn:
        conn.close()
    return

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
            log.debug('db excute error!\n')
            print('db excute error!\n')
        
        try:
            conn.commit()
        except:
            log.debug('commit error!')
            print('commit erorr!')
            
    return

def handleConnect(sock, addr):
    dbconn = get_one_db_connect()
    cur = None
    if dbconn:
        cur = dbconn.cursor()
    
    while True:
        try:
            b_data = sock.recv(1024)
            if b_data == b'':
                print('reomte closed!')
                sock.close()
                break
            
            print(len(b_data), b_data)
            log.debug('recv %s %s %s',addr[0], addr[1], str(b_data))
            #　process data
            s  = process_data(b_data)
            
            # store data
            store_to_db(s, dbconn, cur)
            
            #　send to remote control client
            send_to_remote(b_data)
            
            #　encode return data
            r_data = encode_return_data(b_data)
            sock.send(r_data)
        except:
            print(traceback.format_exc())
            log.debug(traceback.format_exc())
            break
    
    sock.close()
    if dbconn:
        cur.close()
    close_one_db_connect(dbconn)
    return

def mainServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(HOST)
        sock.bind((HOST, SERVER_PORT))
        sock.listen(5)
        print('main server ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            t = threading.Thread(target=handleConnect, args=(conn, addr))
            t.start()
    except:
        print(traceback.format_exc())
        log.debug(traceback.format_exc())

def remoteControlServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(HOST)
        sock.bind((HOST, REMOTE_CONTROL_PORT))
        sock.listen(5)
        print('remote control ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            remote_control_client_list.append(conn)
    except:
        print(traceback.format_exc())
        log.debug(traceback.format_exc())

if __name__=='__main__':
    import os
    print(__file__, 'test')
    t = threading.Thread(target=remoteControlServer)
    t.start()
    init_db_connect_list()
    mainServer()
    os.system('pause')
    
