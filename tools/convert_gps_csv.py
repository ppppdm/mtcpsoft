import sys
import os

IN_FILE = '../res/合肥专用道6月20日_Point.txt.csv'
OUT_FILE = '../res/roadgps.txt'

if len(sys.argv) > 1:
    IN_FILE = sys.argv[1]
if len(sys.argv) > 2:
    OUT_FILE = sys.argv[2]

print('Input file: ', IN_FILE)
print('Output file: ', OUT_FILE)



# read from file
hb_list = list()

try:
    in_f = open(IN_FILE, 'rt')
except Exception as e:
    print(e)
    exit()
print('First line in input file')
print(in_f.readline())

while True:
    ss = in_f.readline()
    ss = ss.strip('\n')
    if ss == '':
        break
    arr = ss.split(',')
    hb_list.append(arr)
in_f.close()




print('Enter the column number of 纬度 经度 路段名 in input file, start from 0')
print('Example   : 1,2,6')
print('Enter Here: ', end='')

cols = input().split(',')
if len(cols) < 3:
    print('Need three numbers')
    exit()


# write to file, the file should be 纬度，经度，路段名
try:
    s=''
    x = int(cols[0])
    y = int(cols[1])
    r = int(cols[2])
    for i in hb_list:
        print(i[x], i[y], i[r])
        s += i[x]+','+i[y]+','+i[r]+'\n'
    s = s.strip('\n')
except Exception as e:
    print(e)
    exit()




out_f = open(OUT_FILE, 'wt')
out_f.write(s)
out_f.close()

print('Convert done, to file ', os.path.abspath(OUT_FILE))
