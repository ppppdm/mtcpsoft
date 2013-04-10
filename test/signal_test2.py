import os  
import signal  
   

#发送信号，5252 是signal_test.py那个绑定信号处理函数的pid，需要自行修改  
os.kill(3248,signal.SIGINT) 


#发送信号，5252 是signal_test.py那个绑定信号处理函数的pid，需要自行修改  
#os.kill(3444,signal.SIGTERM)  
