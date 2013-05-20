# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import time
import sys
import getopt
import datetime

# Global Variables
SERVER_ADDR = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 44444

TOTAL_COUNT = 1
SLEEP_TIME = 5

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

HEART_BEAT_PACKAGE_ITEM_CONTENT = [b'\xaa\x55', b'08002812d137', b'A', b'20120414', b'102113', 
                                   b'5678.12345', b'12345.67891', b'25.23', b'EN', b'1', 
                                   b'192.168.001.010', b'192.168.001.100', b'05', b'4', b'4', 
                                   b'0050', b'12', b'\xee\x55'
                                   ]

def encode_data():
    data = bytearray()
    for i in HEART_BEAT_PACKAGE_ITEM_CONTENT:
        if i == b'20120414':
            i = bytes(datetime.datetime.today().date().strftime('%Y%m%d'), 'gbk')
        if i == b'102113':
            i = bytes(datetime.datetime.today().time().strftime('%H%M%S'), 'gbk')
        data += i
    return data

def client():
    i = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_ADDR, SERVER_PORT))
        while i < TOTAL_COUNT:
            b_data = encode_data()
            sock.send(b_data)
            print(sock.recv(156))
            time.sleep(SLEEP_TIME)
            i+=1
        sock.close()
    except Exception as e:
        print(e)
        sock.close()
    return

def usage():
    print(' usage: python heartBeatClient.py [options]\n'
          ' options:\n'
          '     -c Count    count of gps information sending to server, default is 1\n'
          '     -t Time     second of sleep time between two sending, default is 5\n'
          '     -a Address  server address, default is local IP\n'
          '     -p Port     server port, defalut is 44444'
          '     -h, --help  print this help\n')
    print()

if __name__=='__main__':
    print(__file__, 'test')
    
    # test client
    print(sys.argv)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:t:a:p:h', ['help'])
    except getopt.GetoptError as err:
        # print usage
        print(err)
        usage()
        exit(-1)
    for o, a in opts:
        if o == '-c':
            TOTAL_COUNT = int(a)
        elif o == '-t':
            SLEEP_TIME = float(a)
        elif o == '-a':
            SERVER_ADDR = a
        elif o == '-p':
            SERVER_PORT = int(a)
        elif o == '-h' or o == '--help':
            usage()
            exit()
    
    client()
    
