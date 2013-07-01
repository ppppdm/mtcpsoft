# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

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

def insert_ls_picture():
    conn = get_db_connect()
    if conn:
        cur = conn.cursor()
        
        sql = "INSERT INTO LS_pictures (camera_id,picture_name,captrue_serial_num,collect_date1,backup1,create_time) VALUES ('08-00-28-12-dc-d0','1.jpg',1,'2013-7-1 14:22:01.150','2013-7-1','2013-7-1 14:35:01.150')"
        
        try:
            cur.execute(sql)
        except:
            print('db execute error')
        
        try:
            conn.commit()
        except:
            print('db commit error')
        else:
            print('db insert success')
    close_db_connect(conn)

def update_ls_picture():
    conn = get_db_connect()
    if conn:
        cur = conn.cursor()
        
        sql = "UPDATE LS_pictures SET picture_name = picture_name + ',' + '2.jpg' WHERE (camera_id = '08-00-28-12-dc-d0') and (backup1 = '2013-7-1') and (captrue_serial_num = 1) and ('2013-7-1 14:36:44.115' - create_time < '0:1:00.000')"
        
        try:
            cur.execute(sql)
        except:
            print('db execute error')
        
        try:
            conn.commit()
        except:
            print('db commit error')
        else:
            print('db update success')
    
    close_db_connect(conn)

if __name__=='__main__':
    print(__file__, 'test')
