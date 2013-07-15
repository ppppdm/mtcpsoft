# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import os
import mergePics


DO_MERGE = False
GROUP_PIC_NUM = 3
MERGE_PICS_PATH = '../合成图片/'

gourp_infos = dict()

def keep_infos_temporary(infos, camera_id):
    infos_list = gourp_infos.get(camera_id)
    if infos_list == None:
        infos_list = [infos]
        gourp_infos[camera_id] = infos_list
    else:
        infos_list.append(infos)
    return

def get_infos(camera_id):
    try:
        return gourp_infos[camera_id]
    except:
        print('have not ', camera_id)
    return

def remove_infos(camera_id):
    try:
        del gourp_infos[camera_id]
    except:
        print('have not ', camera_id)
    return

def merge_manager(infos):
    if DO_MERGE:
        camera_id = infos.get('MAC', '')
        No = infos.get('NO.', '0')
        
        if int(No) < GROUP_PIC_NUM:
            keep_infos_temporary(infos, camera_id)
            
        if int(infos['NO.']) == GROUP_PIC_NUM:
            keep_infos_temporary(infos, camera_id)
            infos_list = get_infos(camera_id)
            if infos_list != None:
                mergePics.merge_group_imgs(infos_list, os.path.abspath(MERGE_PICS_PATH)+os.path.sep)
            remove_infos(camera_id)
    return


if __name__=='__main__':
    DO_MERGE = True
    merge_manager({'MAC':'00', 'NO.':'01'})
    merge_manager({'MAC':'00', 'NO.':'02'})
    merge_manager({'MAC':'00', 'NO.':'03'})
