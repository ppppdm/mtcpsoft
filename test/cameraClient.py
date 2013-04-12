# -*- coding:gbk -*-
# auther : pdm
#
# camera client do two things:
# 1. send camera status per x secends as heart beat package
# 2. recv server cmd and process

import logging
import socket

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")
log                     = logging.getLogger(__name__)

def cameraClient(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    
    sock.send(b'12345')
    data = sock.recv(1024)
    
    print(len(data))
    sock.close()
    pass

if __name__=='__main__':
    print(__file__, 'test')
    host = 'localhost'
    port = 6000
    client = cameraClient((host, port))
    
