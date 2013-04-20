#!/usr/bin
# -*- coding : gbk -*-
# author : pdm

import threading
import time
import getopt
#import socket

# using heartBeatClient.py for simu a camera client
import heartBeatClient

# constant value
# DEFAULT_PORT = 6000

# global value
CREATE_THREAD_SLEEP_TIME = 1         # sleep time between two create thread   
TOTAL_THREAD = 1                 # total number of thread to create

TARGET = heartBeatClient.client   # using heartBeatClient.client for simu a camera client


'''
# 一个模拟的摄像头客户端
def cameraClient():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', DEFAULT_PORT))
        for i in range(m_threadLoopCount):
            msg = 'this is camera client '+str(threading.currentThread().ident)+' count '+str(i)+'\n'
            #sock.send(bytearray(SUPER_LONG_MSG, 'utf8'))
            sock.send(bytearray(msg,'utf8'))
            data=sock.recv(2048)
            print(data)
            time.sleep(m_sleepTime)
        
        sock.close()
    except Exception as e:
        print('Error!', e, 'in thread', threading.currentThread().ident)
    
    print(threading.currentThread().getName())
    return
'''


# 控制运行摄像头线程
def runCameraSimu():
    for i in range(TOTAL_THREAD):
        new_t = threading.Thread(target=TARGET)
        new_t.start()
        time.sleep(CREATE_THREAD_SLEEP_TIME)
    return

def usage():
    print(' usage: python multi_client_test.py [options]\n'
          ' options:\n'
          '     -c count    count of gps information sending to server, default is 1\n'
          '     -t time     seconds of sleep time between two sending, default is 5\n'
          '     -C Count    total thread, one thread respent one client, default is 1\n'
          '     -T Time     seconds between create two threads, default is 1\n'
          '     -a Address  server address, default is local IP\n'
          '     -h, --help  print this help\n')
    return

if __name__=='__main__':
    import sys
    print(__file__, 'test')
    print(sys.argv)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:t:a:C:T:h', ['help'])
    except getopt.GetoptError as err:
        # print usage
        print(err)
        usage()
        exit(-1)
    for o, a in opts:
        if o == '-c':
            heartBeatClient.TOTAL_COUNT = int(a)
        elif o == '-t':
            heartBeatClient.SLEEP_TIME = float(a)
        elif o == '-a':
            heartBeatClient.SERVER_ADDR = a
        elif o == '-T':
            CREATE_THREAD_SLEEP_TIME = float(a)
        elif o == '-C':
            TOTAL_THREAD = int(a)
    
    runCameraSimu()
    

