BUSID_CAMERAID_TABLE_FILE = '../res/busId_cameraId_table_chengdu.txt'
BUSID_EQUIPMENTID_TABLE_FILE = '../res/四期300台设备编号.csv'
CAMERAID_EQUIPMENTID_TABLE_FILE = '../res/cameraId_equipmentId_table_chengdu.txt'


# read BUSID_CAMERAID_TABLE_FILE
bus_camera_list = list()
f = open(BUSID_CAMERAID_TABLE_FILE, 'rt')
while True:
    ss = f.readline()
    ss = ss.strip('\n')
    if ss == '':
        break
    arr = ss.split(',')
    print(arr)
    bus_camera_list.append(arr)

f.close()

# read BUSID_EQUIPMENTID_TABLE_FILE
bus_equipment_list = list()
f = open(BUSID_EQUIPMENTID_TABLE_FILE, 'rt')
while True:
    ss = f.readline()
    ss = ss.strip('\n')
    if ss == '':
        break
    arr = ss.split(',')
    print(arr)
    bus_equipment_list.append(arr)

f.close()


# write CAMERAID_EQUIPMENTID_TABLE_FILE
f = open(CAMERAID_EQUIPMENTID_TABLE_FILE, 'wt')
s = ''
for i in bus_camera_list:
    found = False
    cameraId = i[1]
    busId = i[0]
    for j in bus_equipment_list:
        busId2 = j[1]
        equipmentId = j[3]
        if busId2 == busId:
            found = True
            print(busId, cameraId, equipmentId)
            s += cameraId + ',' + equipmentId + '\n'
            break
    if found == False:
        print('bus id not found', busId)

s = s.strip('\n')
f.write(s)
f.close()
