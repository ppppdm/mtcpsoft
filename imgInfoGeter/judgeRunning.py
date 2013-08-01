# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket

def program_is_running():
    try:
        # now we bind the program to a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 4045))
    except Exception as e:
        print('program bind port 4045 error')
        print(e)
        return True
    
    return False
