# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import mmap
import hbMmap
import time

if __name__=='__main__':
    print(__file__, 'test')
    
    #hbMmap.init_mmap_file()
    map = hbMmap.init_mmap(mmap.ACCESS_WRITE)
    
    i = 0
    while True:
        hbMmap.writeNext(map, 'xxxxx %d'%i)
        i+=1
        time.sleep(1)
    
    
