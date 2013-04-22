# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


# self module

BEFORE_INFO_LEN = 6
INFO_LEN        = 87
TOTAL_MARK_LEN  = 124

INFO_ITMES = ['MAC', 'RTC', 'X', 'Y', 'SPEED'
              'DIRECT', 'CAR LICENSE', 'LICENSE COLOR', 'CAR DISTENCE', 'SERIAL NUMBER', 
              'NO.'
              ]

INFO_ITEM_LEN = [12, 16, 10, 11, 5, 
                 2, 16, 8, 2, 4, 
                 1
                 ]

def store_infos(infos):
    return


def get_infos(f):
    return

def file_process(file):
    
    f = open(file, 'rb')
    
    infos = get_infos(f)
    
    store_infos(infos)
    
    f.close()
    
    return

if __name__=='__main__':
    print(__file__, 'test')
