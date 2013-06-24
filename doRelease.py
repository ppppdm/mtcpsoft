# -*- coding:gbk -*-
import tarfile
import datetime
import os
import shutil


# constant values
TEMP_FLODER = 'tmp' + os.path.sep
RELEASE_FLODER = 'release' + os.path.sep

# global values
CONFIG_NAME = ['hefei', 'chengdu']
WORK_PROJECT = ['hb_service', 'imgInfoGeter']



def create_tmp_floder():
    if os.path.exists(TEMP_FLODER) == False:
        os.mkdir(TEMP_FLODER)


def copy_to_tmp_floder(project_name, config_name):
    
    pro_dir = project_name + os.path.sep
    print(pro_dir)
    
    for filename in os.listdir(pro_dir):
        if '.py' in filename or '.ini' in filename or '.conf' in filename:
            #print(filename)
            shutil.copy(pro_dir + filename, TEMP_FLODER + filename)

    cfg_dir = pro_dir + config_name + os.path.sep
    
    for filename in os.listdir(cfg_dir):
        if '_'+config_name+'.' in filename:
            #print(filename)
            shutil.copy(cfg_dir + filename, TEMP_FLODER + filename.replace('_'+config_name, ''))
    
    if os.path.exists(TEMP_FLODER+'log') == False:
        os.mkdir(TEMP_FLODER+'log')


def tar_tmp_floder(project_name, config_name):
    
    dst_name = RELEASE_FLODER + project_name + '-' + config_name + '-' + datetime.datetime.now().strftime('%Y%m%d_%H%M')+ '.tar'    
    tar = tarfile.open(dst_name, 'w')
    print(dst_name)
    
    dir = TEMP_FLODER
    for filename in os.listdir(dir):
        print(filename)
        tar.add(dir + '/' + filename, project_name + '/' +filename)
    
    tar.close()

def delete_tmp_floder():
    for i in os.listdir(TEMP_FLODER):
        if os.path.isdir(TEMP_FLODER+'/'+i):
            os.removedirs(TEMP_FLODER+'/'+i)
        else:
            os.remove(TEMP_FLODER+'/'+i)
    os.removedirs(TEMP_FLODER)



if __name__=='__main__':
    print(WORK_PROJECT)
    print('选择一个项目，输入0或1:', end = '')
    op = input()
    project_name = WORK_PROJECT[int(op)]
    print('选择了', project_name)
    print()
    
    print(CONFIG_NAME)
    print('选择一个配置，输入0或1:', end = '')
    op = input()
    config_name = CONFIG_NAME[int(op)]
    print('选择了', config_name)
    print()
    
    
    create_tmp_floder()
    
    copy_to_tmp_floder(project_name, config_name)
    
    tar_tmp_floder(project_name, config_name)
    
    delete_tmp_floder()
    
    print('完成')


