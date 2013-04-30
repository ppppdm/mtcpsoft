# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import threading
import socket
import select
#import queue
import time
import logging
import multiprocessing


logger = logging.getLogger()
handler = logging.FileHandler('log1.txt')
logger.addHandler(handler)

# self module
import countCPU

HOST=''
SERVER_PORT=44444

client_socket_list = list()

MAX_WORK_THREAD = 2


work_queue = multiprocessing .Queue()


def workThread():
    
    while True:
        print('work')
        logger.debug('work')
        s = work_queue.get()
        print('ready to recv')
        data = s.recv(1024)
        if data:
            s.send(data)
            print(data)
            logger.debug(data)
        else:
            print('socket ', s.getpeername(), 'recv nothing, will close')
            logger.debug('socket close')
            client_socket_list.remove(s)
            s.close()
        work_queue.task_done()
    return

'''
def select_socket_read():

    while True:
        # in windows client_socket_list should should not be None
        # at least give one socket
        if len(client_socket_list) != 0:
            readable , writable , exceptional = select.select(client_socket_list, [], client_socket_list, 5)
            for s in readable:
                print('put')
                logger.debug('put')
                work_queue.put(s)
            for s in exceptional:
                print('exception on socket', s.getpeername())
                client_socket_list.remove(s)
                s.close()
        
        # if no socket in client_socket_list sleep 
        time.sleep(1)
'''
def Server():
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((HOST, SERVER_PORT))
        server_sock.listen(5)
        
        client_socket_list.append(server_sock)
        while True:
            readable , writable , exceptional = select.select(client_socket_list, [], client_socket_list, 5)
            for s in readable:
                if s is server_sock:
                    sock, addr = server_sock.accept()
                    print('connected by', addr)
                    logger.debug('connected by %s', addr)
                    client_socket_list.append(sock)
                else:
                    print('put')
                    logger.debug('put')
                    work_queue.put(s)
            for s in exceptional:
                if s is server_sock:
                    print('server exception')
                    break
                else:
                    print('exception on socket', s.getpeername())
                    client_socket_list.remove(s)
                    s.close()
            time.sleep(5)
    except Exception as e:
        print(e)


if __name__=='__main__':
    print(__file__, 'test')
    # start server 
    t = threading.Thread(None, Server, 'server')
    t.start()
    
    
    # start select_socket_read 
    #t = threading.Thread(None, select_socket_read, 'select_socket_read')
    #t.start()
    
    
    # start workthread
    cpu_count = countCPU.determineNumberOfCPUs()
    
    # the defaut cpu count is 2
    if cpu_count == None:
        cpu_count = 2
    '''
    for i in range(cpu_count):
        t = threading.Thread(None, workThread, 'select_work_thread')
        t.start()
    '''
    
    # use process instead of thread
    for i in range(cpu_count):
        t = multiprocessing.Process(None, workThread, 'select_work_thread')
        t.start()
