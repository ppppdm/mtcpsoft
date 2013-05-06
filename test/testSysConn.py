# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
#import time
import threading
import sys
import getopt

HOST = ''
SERVER_ADDR = 'localhost'
PORT = 4001

TOTAL_CLIENT = 65536 # default is 1000
CREATE_THREAD_SLEEP_TIME = 0.001 # default is 0.001

gConnectList = []
gClientList = []
t_ce = 0

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    
    while True:
        conn, addr = sock.accept()
        #print('connected by', addr)
        
        gConnectList.append(conn)
        total = len(gConnectList)
        print('total conn', total)

def client():
    global t_ce
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_ADDR, PORT))
        gClientList.append(sock)
        #time.sleep(60)
    except Exception as e:
        print('client', e)
        t_ce+=1
    
    #sock.close()
    #print('client exit')

def multiClient():
    for i in range(TOTAL_CLIENT):
        #
        #new_t = threading.Thread(target=client)
        #new_t.start()
        #time.sleep(CREATE_THREAD_SLEEP_TIME)
        
        # not use thread to run a client
        client()
    
    # if not use thread to run a client , close client here
    while len(gClientList):
        client_sock = gClientList.pop()
        client_sock.close()
    
    print('multi client exit')
    print('t_ce', t_ce)
        
if __name__=='__main__':
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'sc')
        print(opts)
    except getopt.GetoptError as err:
        print(err)
    
        
    for o, a in opts:
        if o=='-s':
            print('start server')
            t_s = threading.Thread(target=server)
            t_s.start()
            break
        if o=='-c':
            print('start client')
            t_mc = threading.Thread(target=multiClient)
            t_mc.start()
            break
