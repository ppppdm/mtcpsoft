# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import logging
import socket
import threading

# Global Variables
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
                           'SERVER IP', 'IP', 'interval time', 'upload pics','follow pics', 
                           'car dist', 'yasuoyinzi', 'END' 
                           ]

HEART_BEAT_PACKAGE_ITEM_LEN =[2 , 12, 1, 8, 6, 
                         10, 11, 5, 2, 1, 
                         15, 15, 2, 1, 1, 
                         4, 2, 2
                         ] 

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
    for i in HEART_BEAT_PACKAGE_ITEM_LEN:
        item = get_next_item(b_data, i, t)
        s += str(item, 'utf8')
        t += i
    log.debug(s)
    print(s)
    return

def handleConnect(sock):
    try:
        while True:
            b_data = sock.recv(1024)
            print(len(b_data), b_data)
            log.debug(b_data)
            ##process data
            process_data(b_data)
            ##send to remote control client
            send_to_remote(b_data)
            
            sock.send(SIMPLE_RETURN_FRAME)
    except Exception as e:
        log.debug(e)
        print(e)
        sock.close()
    return

def mainServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', SERVER_PORT))
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
            conn.settimeout(1)
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
    
