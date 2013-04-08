# -*- coding:gbk -*-
# author : pdm
# email : ppppdm@gmail.com
#


import socket
import threading
import select
import logging

#CONSTANT VALUE
SERVER_PORT = 6000

# GLOBAL VALUE
_client_list = []

def workThread():
    while True:
        readable , writable , exceptional = select.select(_client_list, [], [], 2)
        for s in readable:
            data = s.recv(1024)
            print(data)
    return


def mainServer():
    
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSock.bind(('localhost', SERVER_PORT))
        serverSock.listen(5)
        while(True):
            conn, addr = serverSock.accept()
            _client_list.append(conn)
            logging.warning('new client %s', addr)
    except Exception as e:
        logging.warning(e)
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    new_t = threading.Thread(target=workThread)
    new_t.start()
    
    mainServer()
