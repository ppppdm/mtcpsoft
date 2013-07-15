import multiprocessing
import os
import socket
from multiprocessing.reduction import reduce_socket, rebuild_socket
#from multiprocessing.reduction import reduce_handle
#from multiprocessing.reduction import rebuild_handle

def f(a, b):
    
    print('sub process', os.getpid())
    try:
        print('size', b.qsize())
        h = b.get()
        s = rebuild_socket(h, socket.AF_INET,socket.SOCK_STREAM, 0)
        #fd = rebuild_handle(h)
        #s = socket.fromfd(fd,socket.AF_INET,socket.SOCK_STREAM)
        s.send(b'1111')
        print(s)
        print(s.getsockname())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    
    help(rebuild_socket)
    a = multiprocessing.Manager().list()
    b = multiprocessing.Queue()
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(('localhost', 4040))
    s2.connect(('localhost', 4040))
    print(s1.getsockname(), s2.getsockname())
    h1 = reduce_socket(s1)
    h2 = reduce_socket(s2)
    #h1 = reduce_handle(s1.fileno())
    #h2 = reduce_handle(s2.fileno())
    b.put(h1)
    b.put(h2)
    a.append(1)
    print(os.getpid())
    print(a)
    p = multiprocessing.Process(target = f, args = (a, b))
    print(p.pid)
    print(os.getpid())
    p.start()
    print(p.pid)
    p.join()
    print(a)
    
    p1 = multiprocessing.Process(target = f, args = (a, b))
    p1.start()
