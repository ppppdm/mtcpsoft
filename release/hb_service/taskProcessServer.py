# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# this server got and handle task from task interface
import socket
import threading
import traceback
import struct

# self module
import myLog
import taskList

# Global Variables
INADDR_ANY = '0.0.0.0' # OR INADDR_ANY = ''
HOST = INADDR_ANY
SERVER_PORT = 3045


# CMD PROTOCOL:
#   ITEM SEQUEUE:
#       TOTAL_LEN, MAC_NUM, MAC, CMD
#   ITEM :
#       TOTAL_LEN : total len of IP_LEN + IP + CMD_LEN + CMD , 2 bytes, Binary , max value is 65535
#       MAC_NUM   : len of MAC                               , 4 bytes, String , max value is 9999
#       MAC       : MACs                                     ,        , String , each is 12 bytes
#       CMD       : KEY,VALUE pair, between two is a ','     ,        , String , example  K:V,K:V


MAC_NUM_LEN = 4
MAC_LEN = 12
ARG_DELIM = ','
KEY_VALUE_DELIM = ':'


def processTaskData(b_data):
    
    total_mac = b_data[:MAC_NUM_LEN]
    
    macs = str(b_data[MAC_NUM_LEN:MAC_NUM_LEN+total_mac*MAC_LEN], 'utf8')
    
    args = str(b_data[MAC_NUM_LEN+total_mac*MAC_LEN:], 'utf8')
    
    tasks = (macs, args)
    
    taskList.insertTaskList(tasks)
    
    return


def handleRecvTak(conn, addr):
    try:
        buff = bytearray()
        len = 0
        # first recv the total length of task stream
        total_len = struct.unpack('H', conn.recv(2))
        while len < total_len:
           buff = conn.recv(1024)
           len += len(buff)
        print('recv task done!')
        myLog.mylogger.debug('recv task done!')
    except:
        print(traceback.format_exc())
        myLog.mylogger.debug(traceback.format_exc())
    conn.close()
    
    processTaskData(buff)
    
    return

def server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(HOST)
        sock.bind((HOST, SERVER_PORT))
        sock.listen(5)
        print('Task Process server ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('task process server connected by ', addr)
            try:
                t = threading.Thread(target=handleRecvTak, args=(conn, addr))
                t.start()
            except RuntimeError as e:
                print(e)
                myLog.mylogger.debug(e)
    except:
        print(traceback.format_exc())
        myLog.mylogger.debug(traceback.format_exc())

if __name__=='__main__':
    print(__file__, 'test')
    
