# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


# CMD PROTOCOL:
#   ITEM SEQUEUE:
#       TOTAL_LEN, IP_LEN, IP, CMD_LEN, CMD
#   ITEM :
#       TOTAL_LEN : total len of IP_LEN + IP + CMD_LEN + CMD , 2B    , max value is 65535
#       IP_LEN    : len of IP                                , 2B    , max value is 65535(should not be)
#       IP        : IPs                                      , Binary, 
#       CMD_LEN   : len of CMD                               , 2B    , max value is 65535(should not be)
#       CMD       : KEY,VALUE pair, between two is a ';'     , String, 

import socket
import traceback
import threading
import struct

HOST = socket.INADDR_ANY
PORT = 6331

def handleCmd(conn):
    try:
        len = 0
        total = struct.unpack('H', conn.recv(2))
        print('total', total)
        buff = bytearray()
        while len < total:
            data = conn.recv(2048)
            buff += data
            len += len(data)
        print('len', len)
        # get IPs
        len = 0
        ip_list = ()
        ip_len = 0
        ip_total = struct.unpack('H', buff[len:len+2])
        len += 2
        while ip_len < ip_total:
            ip = buff[len+ip_len:len+ip_len+4]
            ip_list.append(ip)
        len += ip_total
        # get CMDs
        cmd_list = buff[len+2:].split(';')
    except:
        print(traceback.format_exc())
    return ip_list, cmd_list

def cmdServer():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.bind((HOST, PORT))
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            print('CMD Server connected by', addr)
            new_t = threading.Thread(target=handleCmd, args=(conn, ))
            new_t.start()
        
    except:
        print(traceback.format_exc())
    return


if __name__=='__main__':
    print(__file__, 'test')
    
