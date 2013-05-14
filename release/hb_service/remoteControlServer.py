# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import traceback

# self module
import myLog

HOST = socket.gethostbyname(socket.gethostname()) #socket.INADDR_ANY
REMOTE_CONTROL_PORT = 6320


remote_control_client_list = []

def send_to_remote(b_data):
    for conn in remote_control_client_list:
        try:
            conn.send(b_data)
        except:
            print(traceback.format_exc())
            myLog.mylogger.debug(traceback.format_exc())
            remote_control_client_list.remove(conn)
            conn.close()


def Server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, REMOTE_CONTROL_PORT))
        sock.listen(5)
        print('remote control ready to accept...')
        while True:
            conn, addr = sock.accept()
            print('connected by ', addr)
            remote_control_client_list.append(conn)
    except:
        print(traceback.format_exc())
        myLog.mylogger.debug(traceback.format_exc())
    return
    



