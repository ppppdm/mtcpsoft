# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import os
import datetime
import mergePics


DO_MERGE = False
GROUP_PIC_NUM = 3
MERGE_PICS_PATH = '../合成图片/'

group_infos = dict()

TIME_DELTA = datetime.timedelta(0, 0, 0, 0, 1)

# store infos in group_infos, 
# return True if have a group info, so can merge pics
# else return False
def have_a_group_info(infos, camera_id, serial_num, collect_time, num):
    infos_list = list()
    _serial_num = 0
    _collect_time = datetime.datetime.now()
    g_infos = group_infos.get(camera_id)
    if g_infos != None:
        infos_list = g_infos[0]
        _serial_num = g_infos[1]
        _collect_time = g_infos[2]
    
    print(_serial_num, _collect_time)
    if g_infos == None:
        infos_list = [infos]
        group_infos[camera_id] = (infos_list, serial_num, collect_time)
        print('merge group info none')
        return False
    elif _serial_num != serial_num:
        infos_list.clear()
        infos_list.append(infos)
        group_infos[camera_id] = (infos_list, serial_num, collect_time)
        print('merge num not equal')
        return False
    elif collect_time - _collect_time > TIME_DELTA:
        infos_list.clear()
        infos_list.append(infos)
        group_infos[camera_id] = (infos_list, serial_num, collect_time)
        print('merge collect time > time delta')
        return False
    else:
        infos_list.append(infos)
        group_infos[camera_id] = (infos_list, serial_num, collect_time)
        if num == GROUP_PIC_NUM and len(infos_list) == GROUP_PIC_NUM:
            return True
        else:
            print('num,len(infos_list)', num, len(infos_list))
            return False

def get_infos(camera_id):
    try:
        return group_infos[camera_id][0]
    except:
        print('have not ', camera_id)
    return

def remove_infos(camera_id):
    try:
        del group_infos[camera_id]
    except:
        print('have not ', camera_id)
    return

def merge_manager(infos):
    if DO_MERGE:
        camera_id = infos.get('MAC', '')
        serial_num = infos.get('SERIAL NUMBER', '0')
        collect_time = infos.get('RTC')
        num = int(infos.get('NO.', '0'))
        try:
            collect_time = datetime.datetime.strptime(collect_time, '%Y%m%d%H%M%S%f')
        except:
            collect_time = datetime.datetime.now()
        
        
        if have_a_group_info(infos, camera_id, serial_num, collect_time, num):
            infos_list = get_infos(camera_id)
            if infos_list != None:
                save_path = os.path.abspath(MERGE_PICS_PATH)
                #print(save_path)
                mergePics.merge_group_imgs(infos_list, save_path)
            remove_infos(camera_id)
        else:
            print('merge wait for a group')
    return


if __name__=='__main__':
    DO_MERGE = True
    merge_manager({'MAC':'00', 'NO.':'01'})
    merge_manager({'MAC':'00', 'NO.':'02'})
    merge_manager({'MAC':'00', 'NO.':'03'})
