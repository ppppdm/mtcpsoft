# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import threading

# import self module
import heartBeatServer
import remoteControlServer
import dbManager


if __name__=='__main__':
    t = threading.Thread(target=heartBeatServer.Server)
    t.start()
    
    t = threading.Thread(target=remoteControlServer.Server)
    t.start()
    
    dbManager.init_db()
