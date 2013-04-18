# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import logging
import socket
import threading
#import traceback

# Global Variables
HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 44444
REMOTE_CONTROL_PORT = 6320

LOG_FILE   = 'log.txt'
LOG_LEVEL  = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(levelname)8s %(thread)d %(name)s %(message)s"
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

def send_to_remote(b_data):
    for conn in remote_control_client_list:
        try:
            conn.send(b_data)
        except socket.timeout as e:
            print(e)
            log.debug(e)
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
        s += str(item, 'gbk')+'\t'
        t += i
    log.debug(s)
    print(s)
    return

def is_in_lanes(location):
    return True

def is_valid_period():
    return True

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

def handleConnect(sock):
    try:
        while True:
            b_data = sock.recv(1024)
            if b_data == b'':
                print('reomte closed!')
                sock.close()
                break
            
            print(len(b_data), b_data)
            log.debug(b_data)
            #　process data
            process_data(b_data)
            
            #　send to remote control client
            send_to_remote(b_data)
            
            #　encode return data
            r_data = encode_return_data(b_data)
            sock.send(r_data)
    except Exception as e:
        log.debug(e)
        print(e)
        sock.close()
    return

def mainServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, SERVER_PORT))
        sock.listen(5)
        print('main server ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            t = threading.Thread(target=handleConnect, args=(conn, ))
            t.start()
    except Exception as e:
        print(e)
        log.debug(e)

def remoteControlServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', REMOTE_CONTROL_PORT))
        sock.listen(5)
        print('remote control ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            remote_control_client_list.append(conn)
    except Exception as e:
        print(e)
        log.debug(e)

if __name__=='__main__':
    import os
    print(__file__, 'test')
    t = threading.Thread(target=remoteControlServer)
    t.start()
    
    mainServer()
    os.system('pasue')
    
