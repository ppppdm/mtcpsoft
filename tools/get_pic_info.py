import os
import datetime
BEFORE_INFO_LEN = 6
INFO_LEN        = 89
TOTAL_MARK_LEN  = 124

INFO_ITMES = ['MAC', 'RTC', 'X', 'Y', 'SPEED', 
              'DIRECT', 'CAR LICENSE', 'LICENSE COLOR', 'CAR DISTENCE', 'SERIAL NUMBER', 
              'NO.', 'CAPTURE FALG'
              ]

INFO_ITEM_LEN = [12, 17, 10, 11, 5, 
                 2, 16, 8, 2, 4, 
                 1, 1
                 ]
def changeToFormate(data):
    data = data[0:2] + b'-' + data[2:4] + b'-' + data[4:6] + b'-' + data[6:8] + b'-' + data[8:10] + b'-' + data[10:12]
    return data

def get_infos(f):
    infos = {}
    
    # in test print the info
    f.seek(BEFORE_INFO_LEN)
    b_data = f.read(INFO_LEN)
    
    
    f.seek(BEFORE_INFO_LEN)
    
    for i in INFO_ITMES:
        item_len = INFO_ITEM_LEN[INFO_ITMES.index(i)]
        b_data = f.read(item_len)
        try:
            if i == 'CAR LICENSE':
                b_data = b_data[:8]
            if i == 'LICENSE COLOR':
                b_data = b_data[:2]
            if i == 'X' or i == 'Y':
                b_data = b_data[:-1]
            if i == 'MAC':
                b_data = changeToFormate(b_data)
            #infos.append((i, str(b_data, 'gbk')))
            infos[i] = str(b_data, 'gbk')
        except:
            print('decode item %s error!'%(i), b_data)
            #logger.debug('decode item %s error! %s'%(i, str(b_data)))
        
    #print(infos)
    
    return infos

def get_file_time(fn):
    file_st = os.stat(fn)
    return datetime.datetime.fromtimestamp(file_st.st_mtime), datetime.datetime.fromtimestamp(file_st.st_atime)

img_file = '20130620180730-dcd0-0027-1.jpg'
f = open(img_file, 'rb')
infos = get_infos(f)
print(infos)

print(get_file_time(img_file))
