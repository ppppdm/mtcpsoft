# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import sys

def isImageComplete(f):
    # the image file formate is JPEG
    # find the sign of end of image (0xFF 0xD9), if found return true
    ret = False
    f.seek(0)
    
    buff = f.read()
    
    if b'\xff\xd9' in buff:
        print('now len is ', f.tell())
        ret = True
    f.seek(0)
    return ret

if __name__=='__main__':
    print(__file__)
    
    if len(sys.argv[1]) > 1:
        f = open(sys.argv[1], 'rb')
        print(isImageComplete(f))
