# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import threading

# import self module
import heartBeatServer
import remoteControlServer
import dbManager
import readRoadGPS


if __name__=='__main__':
    # init road data
    readRoadGPS.initRoadGPS(readRoadGPS.ROAD_GPS_FILE)
    
    t = threading.Thread(target=heartBeatServer.Server)
    t.start()
    
    t = threading.Thread(target=remoteControlServer.Server)
    t.start()
    
    dbManager.init_db()
