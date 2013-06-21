import os
import sys
import datetime
try:
    file = sys.argv[1]
    fst = os.stat(file)
    #print(fst)
    print(datetime.datetime.fromtimestamp(fst.st_mtime))
    print(datetime.datetime.fromtimestamp(fst.st_ctime))
    print(datetime.datetime.fromtimestamp(fst.st_atime))
except:
    print('error')
    
