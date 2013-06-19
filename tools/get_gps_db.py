import pyodbc

# global variabls
DB_HOST = '10.20.1.129' #'192.168.1.5\\MTCP12' # '210.73.152.201' # 
USER = 'sa'
PWD = 'skcl@2013'
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


def get_table_heartbeatinfo(db_conn):
    res = list()
    if db_conn:
        cur = db_conn.cursor()
        sql = "select camera_id,gpx,gpy,gpstime from tbl_heartbeatinfo where gpstime > '2013-06-17 12:00:00.000' order by gpstime"
        cur.execute(sql)
        
        res = cur.fetchall()
    
    return res

def write_to_file(res):
    f = open('gps_db.txt', 'wt')
    
    for i in res:
        s = ''
        print(i)
        s += i[0]+'\t'+i[1]+'\t'+i[2]+'\t'+i[3].strftime('%Y-%m-%d %H:%M:%S')+'\t'
        print(s)
        s+='\n'
        f.write(s)
    f.close()
    return

if __name__=='__main__':
    print(__file__, 'test')
    db_conn = get_db_connect()
    res= get_table_heartbeatinfo(db_conn)
    write_to_file(res)
    close_db_connect(db_conn)
