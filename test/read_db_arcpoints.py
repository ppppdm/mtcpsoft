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

def select_arcpoints(conn):
    cur = conn.cursor()
    cur.execute("select LATITUDE, LONGITUDE, ARC_ID from t_arcpoints")
    ROAD_GPS_POINT_LIST = cur.fetchall()
    
    print(type(ROAD_GPS_POINT_LIST))
    print(len(ROAD_GPS_POINT_LIST))
    #for i in ROAD_GPS_POINT_LIST:
        #print(i)
        #print(float(i[0]), float(i[1]))
    
    cur.execute("select ID,status,Road_Name,Limit_stime,Limit_etime,backup1 from t_arcinfo")
    ROAD_ARC_INFO_LIST = cur.fetchall()
    #print(ROAD_ARC_INFO_LIST)
    
    for i in ROAD_ARC_INFO_LIST:
        print(i[1] == 0)
    return

if __name__=='__main__':
    print(__file__, 'test')
    conn = get_db_connect()
    if conn:
        select_arcpoints(conn)
    else:
        print('db could not connect')
    close_db_connect(conn)
    
    print('test done')
    
