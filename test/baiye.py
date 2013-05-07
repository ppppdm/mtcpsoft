# -*- coding:gbk -*-

infiles = ['ye.c', 'bai.c']
inpath = '../res/'

out_pre = 'new'


def process_file(path, filename):
    f = open(path+filename, 'rb')
    s = f.read()
    f.close()
    
    #print(s)
    outfile = out_pre + filename
    of = open(outfile, 'wt')
    
    t = 0
    for i in s:
        of.write('0x%02x, '%i)
        print('0x%02x,'%i, end=' ')
        t+=1
        if t%16 == 0:
            print()
            of.write('\n')
    
    of.close()
    return

for f in infiles:
    print(f)
    process_file(inpath, f)
