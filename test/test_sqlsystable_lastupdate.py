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


def get_last_update_db(conn):
    luu = datetime.datetime(1, 1, 1)
    if conn:
        cur = conn.cursor()
        sql = "SELECT last_user_update FROM sys.dm_db_index_usage_stats WHERE object_id=object_id('t_arcinfo') and database_id = db_id('CDMTCP')"
        cur.execute(sql)
        rec = cur.fetchone()
        t_arcinfo_luu  = rec[0]
        print('t_arcinfo_luu', t_arcinfo_luu)
        
        sql = "SELECT last_user_update FROM sys.dm_db_index_usage_stats WHERE object_id=object_id('t_arcpoints') and database_id = db_id('CDMTCP')"
        cur.execute(sql)
        rec = cur.fetchone()
        t_arcpoints_luu = rec[0]
        print('t_arcpoints_luu', t_arcpoints_luu)
        
        if t_arcinfo_luu > t_arcpoints_luu:
            luu = t_arcinfo_luu
        else:
            luu = t_arcpoints_luu
        
    return luu

if __name__=='__main__':
    print(__file__, 'test')
    conn = get_db_connect()
    print(get_last_update_db(conn))
    close_db_connect(conn)
