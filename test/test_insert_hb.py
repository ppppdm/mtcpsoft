# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import datetime

# global variabls
DB_HOST = '10.20.1.129' # '210.73.152.201'
USER = 'sa'
PWD = 'skcl@2013'
DATABASE = 'CDMTCP'

try:
    import pyodbc
except:
    print('no module pyodbc, should init first!')

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

def insert_hb():
    conn = get_db_connect()
    #print('autocommit :', conn.autocommit)
    if conn:
        cur = conn.cursor()
        camera_id = '08-00-28-12-dc-d0'
        gpx = 110.253
        gpy = 31.021
        gpstime = datetime.datetime.now()
        roadname = ''
        mph = 0
        createtime = datetime.datetime.now()
        direction = 'ws'
        hb_interval = 5
        upload_num = 3
        track_num = 3
        car_distance = '0617'
        compression_factor = 70
        
        sql = "INSERT INTO tbl_heartbeatinfo( ID, camera_id, gpx, gpy, gpstime, roadname, mph, createtime, direction, hb_interval, upload_num, track_num, car_distance, compression_factor) VALUES (newid(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        try:
            cur.execute(sql, camera_id, gpx, gpy, gpstime, roadname, mph, createtime, direction, hb_interval,
                        upload_num, track_num, car_distance, compression_factor)
        except:
            print('db execute error')
        
        try:
            conn.commit()
        except:
            print('db commit error')
        else:
            print('db update success')
        
        
    
    close_db_connect(conn)
    return

if __name__=='__main__':
    print(__file__, 'test')
    insert_hb()
