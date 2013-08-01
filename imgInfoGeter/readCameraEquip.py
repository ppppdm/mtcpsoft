# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import InfoProcess

def read_camera_equipment():
    if InfoProcess.RENAME_BY_EQUIP and InfoProcess.CAMERA_EQUIP_FILE != '':
        f = open(InfoProcess.CAMERA_EQUIP_FILE, 'rt')
        while True:
            ss = f.readline()
            ss = ss.strip('\n')
            if ss == '':
                break
            arr = ss.split(',')
            InfoProcess.CAMERAID_EQUIPMENTID[arr[0]] = arr[1]
        f.close()
        print('Read camera_equipment table')
    #print(InfoProcess.CAMERAID_EQUIPMENTID)
    else:
        print('Not read camera_equipment table')
