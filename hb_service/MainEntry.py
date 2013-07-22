# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import threading

# import self module
import heartBeatServer
import remoteControlServer
#import dbManager
import readRoadGPS
import globalConfig
import dbUpdater


if __name__=='__main__':
    
    # init global values from config file
    globalConfig.readConfig()
    
    # init database
    #dbManager.init_db()
    
    # init road data
    #readRoadGPS.initRoadGPS(globalConfig.ROAD_GPS_FILE)
    readRoadGPS.initRoadInfo()
    
    t = threading.Thread(target=heartBeatServer.Server)
    t.start()
    
    t = threading.Thread(target=remoteControlServer.Server)
    t.start()
    
    t = threading.Thread(target=dbUpdater.update_db_server)
    t.start()
    
