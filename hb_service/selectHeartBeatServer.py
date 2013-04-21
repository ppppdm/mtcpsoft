# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import threading
import socket
import select
import queue

HOST='localhost'
SERVER_PORT=6000

client_socket_list = list()

MAX_WORK_THREAD = 2


work_queue = queue.Queue()


def workThread():
    
    while True:
        print('work')
    return


def select_socket_read(sock):
    i = 0
    while i < 5:
        readable , writable , exceptional = select.select(client_socket_list, [], [], 5)
        for s in readable:
            data = s.recv(1024)
            print(data)
        i+=1

def Server():
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((HOST, SERVER_PORT))
        server_sock.listen(5)
        while True:
            sock, addr = server_sock.accept()
            print('connected by', addr)
            client_socket_list.append(sock)
    except Exception as e:
        print(e)


if __name__=='__main__':
    print(__file__, 'test')
    # start server 
    t = threading.Thread(None, Server, 'server')
    t.start()
    
    
    # start select_socket_read 
    t = threading.Thread(None, select_socket_read, 'select_socket_read')
    t.start()
