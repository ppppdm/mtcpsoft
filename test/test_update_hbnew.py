# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# global variabls
DB_HOST = '10.20.1.129' # '210.73.152.201'
USER = 'sa'
PWD = 'skcl@2013'
DATABASE = 'CDMTCP'

import datetime
import time
import threading

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

def insert_hbnew(camera_id):
    conn = get_db_connect()
    #print('autocommit :', conn.autocommit)
    if conn:
        cur = conn.cursor()
        gpx = 110.253
        gpy = 31.021
        gpstime = datetime.datetime.now()
        roadname = ''
        mph = 0
        createtime = datetime.datetime.now()
        
        sql = "insert into tbl_heartbeatinfo_new (ID, camera_id, gpx, gpy, gpstime, roadname, mph, createtime) VALUES (newid(), ?, ?, ?, ?, ?, ?, ?)"
        try:
            cur.execute(sql, camera_id, gpx, gpy, gpstime, roadname, mph, createtime)
        except:
            print('db execute error')
        
        try:
            conn.commit()
        except:
            print('db commit error')
        else:
            print('db insert success')
        
        
    
    close_db_connect(conn)
    return

def update_hbnew(camera_id):
    conn = get_db_connect()
    #print('autocommit :', conn.autocommit)
    if conn:
        cur = conn.cursor()
        gpx = 110.253
        gpy = 31.021
        gpstime = datetime.datetime.now()
        roadname = ''
        mph = 0
        createtime = datetime.datetime.now()
        
        sql = "update tbl_heartbeatinfo_new set gpx = ?, gpy = ?, gpstime = ?, roadname = ?, mph = ?, createtime = ? where (camera_id = ?)"
        try:
            cur.execute(sql, gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
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

def run_update(id, times):
    for i in range(times):
        update_hbnew('id')
        time.sleep(5)

if __name__=='__main__':
    print(__file__, 'test')
    total_client = 1000
    for i in range(total_client):
        insert_hbnew(i)
    
    for i in range(total_client):
        new_t = threading.Thread(target=run_update, args=(i, 10))
        new_t.start()
        time.sleep(0.01)
   
    
    
    
