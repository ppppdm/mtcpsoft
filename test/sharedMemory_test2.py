# -*- coding:gbk -*-
# author : pdm
# email : ppppdm@gmail.com
#
# test shareMemory use


import mmap

with mmap.mmap(-1, 13) as map:
    map.write(b'helloworld')
