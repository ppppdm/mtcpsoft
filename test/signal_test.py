# -*- coding:gbk -*-
# author : pdm
# email : ppppdm@gmail.com
#

import os  
import signal  
from time import sleep  
   
def onsignal_term(a,b):  
    print('收到SIGTERM信号')
   
#这里是绑定信号处理函数，将SIGTERM绑定在函数onsignal_term上面  
signal.signal(signal.SIGTERM,onsignal_term)  
   
def onsignal_usr1(a,b):  
    print('收到SIGUSR1信号')  
#这里是绑定信号处理函数，将SIGUSR1绑定在函数onsignal_term上面  
signal.signal(signal.SIGINT,onsignal_usr1)  
   
while 1:  
    print('我的进程id是',os.getpid())  
    sleep(10)  
