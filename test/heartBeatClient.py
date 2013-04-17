# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import time
import sys
import getopt

# Global Variables
SERVER_ADDR = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 44444

TOTAL_COUNT = 1
SLEEP_TIME = 5

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

HEART_BEAT_PACKAGE_ITEM_CONTENT = [b'\xaa\x55', b'E2C34D5E992F', b'A', b'20120414', b'102113'
                                   b'5678.12345', b'12345.67891', b'25.23', b'EN', b'1', 
                                   b'192.168.001.010', b'192.168.001.100', b'05', b'4', b'4', 
                                   b'0050', b'12', b'\xaa\x55'
                                   ]

def encode_data():
    data = bytearray()
    for i in HEART_BEAT_PACKAGE_ITEM_CONTENT:
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
            print(sock.recv(16))
            time.sleep(SLEEP_TIME)
            i+=1
        sock.close()
    except Exception as e:
        print(e)
        sock.close()
    return

def usage():
    print()

if __name__=='__main__':
    print(__file__, 'test')
    
    # test client
    print(sys.argv)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:t:a:')
    except getopt.GetoptError as err:
        # print usage
        print(err)
        usage()
        exit(-1)
    for o, a in opts:
        if o == '-c':
            TOTAL_COUNT = int(a)
        elif o == '-t':
            SLEEP_TIME = int(a)
        elif o == '-a':
            SERVER_ADDR = a
    
    client()
    
