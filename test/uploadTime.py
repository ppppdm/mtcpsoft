#coding=utf-8
import os
import sys
import datetime

DataPath = '//10.20.1.129/ftp/tmp1'

def main():
    total = 0
    delta_list = []
    files = os.listdir(DataPath)
    for file in files:
        if '.jpg' in file:
            try:
                #print(file)
                #判断文件的最后修改时间
                fileName = os.path.join(DataPath, file)
                file_st = os.stat(fileName)
                delta = file_st.st_mtime - file_st.st_ctime
                print(delta)
                delta_list.append(delta)
            except Exception as e:
                print(e)
    
    for i in delta_list:
        total += i
    
    print('average :', total/len(delta_list))
    pass

def get_file_time(fn):
    file_st = os.stat(fn)
    print(file_st)
    return datetime.datetime.fromtimestamp(file_st.st_mtime), datetime.datetime.fromtimestamp(file_st.st_atime)
  

if __name__ == '__main__':
    #main()
    
    # test get_file_time
    if len(sys.argv[1]) > 1:
        print(get_file_time(sys.argv[1]))
