# -*- coding:utf8 -*-
# auther : pdm
# email : ppppdm@gmail.com

import ftplib
import os
import time

HOST = '10.20.1.128'
USER = 'camera'
PAWD = '123456'


ftp = ftplib.FTP(HOST)
print(ftp.login(USER, PAWD))
print(ftp.getwelcome())

print(ftp.retrlines('LIST'))
print(ftp.cwd('tmp'))
print(ftp.pwd())

filename = '../res/2013041710510982-d137-0001-3.jpg'

bufsize = 1024#设置缓冲块大小 
file_handler = open(filename,'rb')#以读模式在本地打开文件 
print(ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize))
s = ftp.retrlines('LIST')
#print(s.encode('utf8').decode('gbk'))
#print(ftp.retrlines('LIST'))

time.sleep(2)
#ftp.delete(os.path.basename(filename))

print(ftp.quit())
print(ftp.close())
