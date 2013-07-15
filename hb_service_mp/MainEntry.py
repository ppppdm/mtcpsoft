# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import sys
import traceback
import multiprocessing
import platform

import dbManager
import processData

def do_init():
    dbconn = None
    cur = None
    dbconn = dbManager.get_db_connect()
    if dbconn:
        cur = dbconn.cursor()
    return dbconn, cur

def do_finish(dbconn, cur, sock):
    if dbconn:
        cur.close()
    dbManager.close_db_connect(dbconn)
    # close socket
    sock.close()
    return

def handleConnect(queue):
    if platform.system() == 'Windows':
        sock = queue.get()
    
    dbconn, cur = do_init()
    
    while True:
        try:
            b_data = sock.recv(1024)
            #print(b_data)
            if b_data == b'':
                print('reomte closed!')
                sock.close()
                break
            
            r_data  = processData.process_data(b_data, dbconn, cur)
            sock.send(r_data)
            #print('send over')
        except:
            print(traceback.format_exc())
            break
    do_finish(dbconn, cur, sock)
    print('sub process done')
    return

def Server(HOST, SERVER_PORT):
    workProcess = list()
    PORT = SERVER_PORT
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(HOST, PORT)
        sock.bind((HOST, PORT))
        sock.listen(5)
        socket_queue = multiprocessing.Queue()
        print('main server ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            try:
                # This code just run in Windows, While in Linux , give the socket to subprocess by Queue
                # should import multiprocessing.reduction reduce_handle, rebuild_handle Or reduce_socket, rebuild_socket
                if platform.system() == 'Windows':
                    socket_queue.put(conn)
                    p = multiprocessing.Process(target=handleConnect, args=(socket_queue, ))
                    workProcess.append((p, conn))
                    p.start()
            except RuntimeError as e:
                print(e)
                #myLog.mylogger.error(e)
            print('total sub process', len(workProcess))
    except:
        print(traceback.format_exc())
        #myLog.mylogger.error(traceback.format_exc())
    finally:
        # terminate all subprocess by sending signal
        
        # terminate all subprocess force
        for p, sock in workProcess:
            try:
                p.terminate()
                p.join()
                sock.close()
            except Exception as e:
                print(e)
                continue
        # if server error exit
        sys.exit()
    
    

if __name__=='__main__':
    HOST = INADDR_ANY = '0.0.0.0'
    PORT = 4040
    Server(HOST, PORT)
