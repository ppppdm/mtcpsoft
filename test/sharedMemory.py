# -*- coding:utf8 -*-
# author : pdm
# email : ppppdm@gmail.com
#
# test shareMemory use

import mmap

def myfun():
    print(1)


try:
    wtext = 'www.vimer.cn'
    f = open('hello.txt','w+b')
    f.truncate(len(wtext))
    map = mmap.mmap(f.fileno(), len(wtext))
    #map.write(wtext.encode('utf8'))
    map.flush()
except Exception as e:
    print(e)
