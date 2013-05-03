# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import time
import mmap
import hbMmap


if __name__=='__main__':
    print(__file__, 'test')
    
    map = hbMmap.init_mmap(mmap.ACCESS_READ)
    old_index = 0
    while True:
        index = hbMmap.getIndex(map)
        print('index', index, 'old', old_index)
        if index > old_index:
            for i in range(old_index+1, index+1):
                print(hbMmap.get(map, i))
                print()
            
        elif index < old_index:
            for i in range(old_index+1, hbMmap.MAX_NUM+1):
                print(hbMmap.get(map, i))
                print()
            for i in range(hbMmap.MIN_NUM, index+1):
                print(hbMmap.get(map, i))
                print()
        else:
            time.sleep(5)
        old_index = index
