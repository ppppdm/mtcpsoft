#!/usr/bin
# -*- coding : gbk -*-
# author : pdm

import threading
import time
import socket

# constant value
DEFAULT_PORT = 6000

# global value
m_sleepTime = 5
m_threadLoopCount = 100



SUPER_LONG_MSG=('644gafaasffsahfjhmasf;a;sljfdffspfaisfamj;a;fasfjlsjfas;fljasof.'
                'pfaisfamj;a;fasfjlsjfas;fljasof.paosfjafaskfjjas;fja;jfsf;lajf;a'
                'paosfjafaskfjjas;fja;jfsf;lajf;aasfasfsasfllopopquonpoaijfa;lsfj'
                'jf;ajfaasfdklsadnfa,l;jkf;askfmlaaaaa;lfffffffffffffffffffffff;a'
                'aaaaaaaaaaasfwefwqfqptoiui[qogghhhhhhqpgq,pgiqoppqi4992rpojqwjtt'
                'dnfa,l;jkf;askfmlaaaaa;lfffffffasfd;aklfd;dddasf2r11334t1nmzxvva'
                'ipituwwwtrhhhhhhhhhhhhhh232ogghhhhhhqpgq,pgiqoppqi4992rpoaaf34t3'
                'jgggggggggggggggggggggggggoeiq[iiiq][wpeggggggggggertggxxxxxasff'
                '644gafaasffsahfjhmasf;a;sljfdffspfaisfamj;a;fasfjlsjfas;fljasof.'
                'pfaisfamj;a;fasfjlsjfas;fljasof.paosfjafaskfjjas;fja;jfsf;lajf;a'
                'paosfjafaskfjjas;fja;jfsf;lajf;aasfasfsasfllopopquonpoaijfa;lsfj'
                'jf;ajfaasfdklsadnfa,l;jkf;askfmlaaaaa;lfffffffffffffffffffffff;a'
                'aaaaaaaaaaasfwefwqfqptoiui[qogghhhhhhqpgq,pgiqoppqi4992rpojqwjtt'
                'dnfa,l;jkf;askfmlaaaaa;lfffffffasfd;aklfd;dddasf2r11334t1nmzxvva'
                'ipituwwwtrhhhhhhhhhhhhhh232ogghhhhhhqpgq,pgiqoppqi4992rpoaaf34t3'
                'jgggggggggggggggggggggggggoeiq[iiiq]?wpeggggggggggertggggqerhhhh'
                )

# 一个模拟的摄像头客户端
def cameraClient():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', DEFAULT_PORT))
        for i in range(m_threadLoopCount):
            #msg = 'this is camera client '+str(threading.currentThread().ident)+' count '+str(i)+'\n'
            sock.send(bytearray(SUPER_LONG_MSG, 'utf8'))
            #sock.send(bytearray(msg,'utf8')
            time.sleep(m_sleepTime)
        
        sock.close()
    except Exception as e:
        print('Error!', e, 'in thread', threading.currentThread().ident)
    
    print(threading.currentThread().getName())
    return

# 控制运行摄像头线程
def runCameraSimu(total_threads):
    for i in range(total_threads):
        new_t = threading.Thread(None, cameraClient, 'thread'+str(i), (), None)
        new_t.start()
        time.sleep(1)
    return


if __name__=='__main__':
    import sys
    print(__file__, 'test')
    print(sys.argv)
    
    threads_total = 0
    sleep_time = 5
    
    if len(sys.argv) > 3:
        threads_total_number = int(sys.argv[1])
        sleep_time = int(sys.argv[2])
        thread_loop_count = int(sys.argv[3])
        m_sleepTime = sleep_time
        m_threadLoopCount = thread_loop_count
    else:
        print('App arguments error!')
        exit()
    
    runCameraSimu(threads_total_number)
    

