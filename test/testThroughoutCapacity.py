# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import queue
import threading
import time

# optional settings
LONG_CONNECT    = True
NUM_CONNECT     = 1
INTERVAL_TIME   = 0
IS_RECIVE       = True
SEND_AFTER_RECV = True
RECV_BUFF_SIZE  = 1024


SEND_CONTENT    = b'XXXX_XXXX_XXXX_XXXX'
TEST_TIME       = 60 # sec

# user settings
SERVER_ADDR     = 'localhost'
SERVER_PORT     = 44444


# global variables
gStatictisQueue = queue.Queue()   # for store client information after client run over
gTotalSend      = 0               # total Bytes send in test time

gClientThreads  = list()          # the list of threads start a client
gRunning        = True            # for client to run if True

def client():
    global gRunning
    total = 0
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_ADDR, SERVER_PORT))
        
        while gRunning:
            sock.send(SEND_CONTENT)
            total += len(SEND_CONTENT)
            
            if IS_RECIVE:
                sock.recv(RECV_BUFF_SIZE)
            
        #print('client', gRunning)
    except Exception as e:
        print(e)
    
    gStatictisQueue.put(total)
    #print('client exit')
    return

def mainControl():
    global gRunning
    global gTotalSend
    print(SEND_CONTENT)
    gRunning = True
    for i in range(NUM_CONNECT):
        t = threading.Thread(target = client)
        t.start()
        gClientThreads.append(t)
    
    # after start all the client thread, sleep 
    time.sleep(TEST_TIME)
    
    
    # set gRunning to false
    gRunning = False
    print('test running', gRunning)
    
    # wait for client thread finish
    for i in gClientThreads:
        i.join()
    print('all client done')
    
    # statictis the total send bytes
    while 1:
        try:
            gTotalSend += gStatictisQueue.get_nowait()
            #print(gTotalSend)
        except:
            break
    print('total send ', gTotalSend)
    return

HEART_BEAT_PACKAGE_ITEM_CONTENT = [b'\xaa\x55', b'08002812d137', b'A', b'20120414', b'102113', 
                                   b'5678.12345', b'12345.67891', b'25.23', b'EN', b'1', 
                                   b'192.168.001.010', b'192.168.001.100', b'05', b'4', b'4', 
                                   b'0050', b'12', b'\xee\x55'
                                   ]
def encode_data():
    data = bytearray()
    for i in HEART_BEAT_PACKAGE_ITEM_CONTENT:
        data += i
    return data

if __name__=='__main__':
    SEND_CONTENT = encode_data()
    tasklist = [1, 10, 100, 200, 500, 900]
    for i in tasklist:
        NUM_CONNECT = i
        mainControl()
