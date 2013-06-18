
IN_FILE = '../res/合肥专用道_Point（6月18日）.txt.csv'
OUT_FILE = '../res/roadgps_hefei.txt'

hb_list = list()

# read from file
in_f = open(IN_FILE, 'rt')

in_f.readline()
while True:
    ss = in_f.readline()
    ss = ss.strip('\n')
    if ss == '':
        break
    arr = ss.split(',')
    print(arr)
    hb_list.append(arr)
in_f.close()

# write to file
out_f = open(OUT_FILE, 'wt')
for i in hb_list:
    s = i[1]+','+i[2]+','+i[7]+'\n'
    out_f.write(s)

out_f.close()
