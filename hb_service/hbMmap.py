# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# heart beat recv from camera client will write to mmap file

import os
import mmap

# the content of mmap file :

# the mmap file
FILE_NAME = 'recv_c.tmp'

# the content's of mmap file
FILE_HEAD_LEN = 3
FILE_ITEM_NUM = 300
ITEM_LEN = 40

# total len of mmap file
MMAP_LEN = FILE_HEAD_LEN + FILE_ITEM_NUM * ITEM_LEN

# the min and max index
MIN_NUM = 0
MAX_NUM = FILE_ITEM_NUM - 1


def init_mmap_file():
    # if file not exist create it
    f = open(FILE_NAME,'wb')
    print(f)
    
    # set the file size to MMAP_LEN
    buff = bytes(MMAP_LEN)
    f.write(buff)
    
    # as in windows the file should not be empty
    f.seek(0)
    f.write(b'000')
    
    f.flush()
    f.close()

def init_mmap(a = mmap.ACCESS_COPY):
    # access:
    #   ACCESS_WRITE 2
    #   ACCESS_READ  1
    #   ACCESS_COPY  3
    map = None
    try:
        f = open(FILE_NAME,'r+b')
        map = mmap.mmap(fileno = f.fileno(), length = 0, access = a)
    except Exception as e:
        print(e)
    
    return map

def close_mmap(map):
    if map:
        map.close()
        print('mmap is closed :', map.closed)
    pass


def getIndex(map):
    map.seek(os.SEEK_SET)
    b_index = map.read(3)
    index = int(b_index)
    
    return index

def setIndex(map, num):
    map.seek(os.SEEK_SET)
    #print(num)
    b_index = bytes(str(num).zfill(3), 'utf8')
    #print(b_index)
    map.write(b_index)
    map.flush()
    return

def writeNext(map, infos):
    
    # get the index in the file head
    index = getIndex(map)
    
    # wirte infos, the len of info should not bigger than ITEM_LEN
    map.seek(FILE_HEAD_LEN+ITEM_LEN*index)
    map.write(bytes(infos, 'utf8'))
    
    index += 1
    if index > MAX_NUM:
        index = MIN_NUM
    
    setIndex(map, index)
    return

def get(map, index):
    
    # index should not bigger than MAX_NUM
    if index > MAX_NUM:
        return None
    
    map.seek(FILE_HEAD_LEN+ITEM_LEN*index)
    b_info = map.read(ITEM_LEN)
    #print(b_info)
    info = str(b_info, 'utf8')
    return info

def getLast():
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    init_mmap_file()
    
    map = init_mmap(mmap.ACCESS_WRITE)
    
    for i in range(310):
        writeNext(map, 'hello bb erasdf %d'%i)
    
    for i in range(99):
        setIndex(map, getIndex(map)+1)
    
    for i in range(305):
        print(get(map, i))
    #map.write(b'hello world!')
    
    close_mmap(map)
    
    
    
    #help(mmap)
    
