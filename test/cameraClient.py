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


class cameraClient():
    
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM
    
    
    def __init__(self, address, timesleep = 5, loopCount = 100):
        self.address = address
        client_socket= socket.socket(self.address_family, self.socket_type)
        client_socket.connect(address)
        

if __name__=='__main__':
    print(__file__, 'test')
    host = 'localhost'
    port = 6000
    client = cameraClient((host, port))
    
