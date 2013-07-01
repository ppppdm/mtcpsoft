# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# copy 6.26_hefei img file to ftp for watch

import os
import shutil
import time

imgfiles = os.listdir('../res/6.26_hefei')
print(imgfiles)

imgfiles1 =  ['20130626064148-dcd0-0001-1.jpg', '20130626064154-dcd0-0001-2.jpg', '20130626064154-dcd0-0001-3.jpg']
imgfiles2 =  ['20130626104824-dcd0-0001-1.jpg', '20130626104824-dcd0-0001-2.jpg', '20130626104825-dcd0-0001-3.jpg']

for i in imgfiles1:
    shutil.copy('../res/6.26_hefei/' + i, 'd:/ftp')
    time.sleep(10)

time.sleep(60)
for i in imgfiles2:
    shutil.copy('../res/6.26_hefei/' + i, 'd:/ftp')
    time.sleep(10)
