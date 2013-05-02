# -*- coding : gbk -*-
# author : pdm


# add up total recv of server , each client sending


client_list = list()
count_list = list()
TOTAL_RECV = 0

def __add(name):
    if name in client_list:
        i = client_list.index(name)
        count_list[i] += 1
    else:
        client_list.append(name)
        count_list.append(1)
    return

def add_up(filename):
    global TOTAL_RECV
    f = open(filename, 'rt')
    
    while True:
        ss = f.readline()
        if ss == '':
            break
        arr = ss.split()
        
        if len(arr) > 4 and arr[4] == 'recv':
            TOTAL_RECV+=1
            __add((arr[5], arr[6]))
    
    f.close()

def show_statistics():
    print('total recv :', TOTAL_RECV)
    for i in client_list:
        print(i, count_list[client_list.index(i)])
    print('total recv :', TOTAL_RECV)

if __name__=='__main__':
    import sys
    
    
    add_up(sys.argv[1])
    show_statistics()
