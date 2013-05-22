# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import ftplib
import os
import time
import sys
import getopt

# global variables

HOST = '10.20.1.129'
PORT = 7777      # 21
USER = 'cdmtcp4' #'camera' #
PAWD = '123'     #'camera' #

path = '../res/5.3/'


def usage():
    print('usage: python fpt_client.py [option] \n'
          '    -a addr     address of ftp server \n'
          '    -p port     port of ftp server listened \n'
          '    -U user     ftp user \n'
          '    -P pw       password of the ftp user \n'
          '    -r res      resource floder upload to ftp\n')


try:
    opts, args = getopt.getopt(sys.argv[1:], 'a:p:U:P:r:h')
except:
    usage()
    exit()

print(opts)

for o, a in opts:
    if o == '-a':
        HOST = a
    elif o == '-p':
        PORT = int(a)
    elif o == '-U':
        USER = a
    elif o == '-P':
        PAWD = a
    elif o == '-r':
        path = a
    elif o == '-h':
        usage()
        exit()
        

print(HOST, PORT, USER, PAWD)

ftp = ftplib.FTP()
ftp.connect(HOST, PORT)
print(ftp.login(USER, PAWD))
print(ftp.getwelcome())



pic_list = os.listdir(path)
print(len(pic_list))

bufsize = 1024#设置缓冲块大小 
for i in pic_list:
    if '.jpg' in i:
        handler = open(path + i, 'rb')
        ftp.storbinary('STOR %s' %os.path.basename(i), handler, bufsize)
        time.sleep(1)

time.sleep(2)


print(ftp.quit())
print(ftp.close())
