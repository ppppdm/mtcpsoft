# get eID camera_id camera_code sBusID from table equipment

import pyodbc

# global variabls
DB_HOST = '10.20.1.129' #'192.168.1.5\\MTCP12' # '210.73.152.201'
USER = 'sa'
PWD = 'skcl@2013' #'sa'
DATABASE = 'CDMTCP'


def get_db_connect():
    db_conn = None
    try:
        db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    except: # not print db execption yet
        #logger.debug('init db got an error!')
        print('init db got an error!')
    return db_conn

def close_db_connect(db_conn):
    if db_conn:
        db_conn.close()

def get_table_equipment(db_conn):
    if db_conn:
        cur = db_conn.cursor()
        sql = "select eID, camera_id, camera_code, sBusID from equipment order by sBusID"
        
        try:
            cur.execute(sql)
        except:
            print('db execute error')
        
    return cur.fetchall()

def write_to_file(res):
    f = open('busId_cameraId_table.txt', 'wt')
    # the file formate is [busId, cameraId]
    s = ''
    for i in res:
        busId = i[3]
        cameraId = i[1]
        s += busId + ',' + cameraId + '\n'
    
    s = s.strip('\n')
    f.write(s)
    f.close()

if __name__=='__main__':
    print(__file__, 'test')
    db_conn = get_db_connect()
    res = get_table_equipment(db_conn)
    print(res)
    
    write_to_file(res)
    close_db_connect(db_conn)
