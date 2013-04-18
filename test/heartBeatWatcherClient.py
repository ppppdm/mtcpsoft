# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import logging
import socket
import sys
import getopt

SERVER_ADDR = ''
REMOTE_CONTROL_PORT = 6320

LOG_FILE   = 'client_log.txt'
LOG_LEVEL  = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(levelname)8s %(thread)d %(name)s %(message)s"
logging.basicConfig(filename = LOG_FILE, 
                    level    = LOG_LEVEL, 
                    format   = LOG_FORMAT)
log = logging.getLogger(__name__)

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

def client():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_ADDR, REMOTE_CONTROL_PORT))
        print('client connected to server')
        while True:
            b_data = sock.recv(1024)
            # process data
            process_data(b_data)
    except Exception as e:
        print(e)
        log.debug(e)
    return

if __name__=='__main__':
    print(__file__, 'test run')
    print(sys.argv)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:')
    except getopt.GetoptError as err:
        # print usage
        print(err)
        exit(-1)
    
    for o, a in opts:
        if o == '-a':
            SERVER_ADDR = a
    
    client()


