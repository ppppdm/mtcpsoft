# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import threading
import socket
import select
import queue
import time

# self module
import countCPU

HOST='localhost'
SERVER_PORT=6000

client_socket_list = list()

MAX_WORK_THREAD = 2


work_queue = queue.Queue()


def workThread():
    
    while True:
        print('work')
        s = work_queue.get()
        data = s.recv(1024)
        s.send(data)
        work_queue.task_done()
    return


def select_socket_read():

    while True:
        # in windows client_socket_list should should not be None
        # at least give one socket
        if len(client_socket_list) != 0:
            readable , writable , exceptional = select.select(client_socket_list, [], client_socket_list, 5)
            for s in readable:
                work_queue.put(s)
            for s in exceptional:
                client_socket_list.remove(s)
        
        # if no socket in client_socket_list sleep 
        time.sleep(1)

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
    
    
    # start workthread
    cpu_count = countCPU.determineNumberOfCPUs()
    
    # the defaut cpu count is 2
    if cpu_count == None:
        cpu_count = 2
    
    for i in range(cpu_count):
        t = threading.Thread(None, workThread, 'select_work_thread')
        t.start()
