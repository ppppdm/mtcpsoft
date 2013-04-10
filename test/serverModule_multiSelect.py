# -*- coding:gbk -*-
# author : pdm
# email : ppppdm@gmail.com
#


import socket
import threading
#import select
import logging

#CONSTANT VALUE
SERVER_PORT = 6000

# GLOBAL VALUE
_client_list = []

def handleConnect(sock):
    data = None
    try:
        data = sock.recv(1024)
        if data == b'':
            logging.warning('client closed')
            _client_list.remove(sock)
            sock.close()
            return
        rdata = data + b'server return!'
        sock.send(rdata)
    except Exception as e:
        logging.error(e)
        _client_list.remove(sock)
        sock.close()

def mainServer():
    
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSock.bind(('localhost', SERVER_PORT))
        serverSock.listen(5)
        while(True):
            conn, addr = serverSock.accept()
            _client_list.append(conn)
            logging.warning('new client %s', addr)
            t = threading.Thread(target=handleConnect, args=(conn, ))
            t.start()
            logging.warning('client num %d', len(_client_list))
    except Exception as e:
        logging.error(e)
        
    
    return

if __name__=='__main__':
    print(__file__, 'test')
    mainServer()
