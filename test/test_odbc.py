# -*- coding:utf8 -*-
# auther : pdm
# email : ppppdm@gmail.com

import pyodbc
import datetime

HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'




help(pyodbc.Cursor.execute)
try:
    conn = pyodbc.connect('DRIVER={SQL Server}', host = HOST, user = USER, password = PWD, database = DATABASE)
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.20.1.200;DATABASE=CDMTCP;UID=sa;PWD=sa')
    print(conn)
    cur = conn.cursor()
    cur.execute('sp_help tbl_heartbeatinfo')
    # cur.execute('sp_helpdb CDMTCP')
    for i in cur.fetchall():
        print(i)
    
    ID = 'newid()'
    camera_id = 'E2C34D5E992F'
    x = '5678.12345'
    y = '12345.67891'
    gpstime = datetime.datetime.now()
    road = ''
    mph = 25
    
    cur.execute("INSERT INTO tbl_heartbeatinfo( ID, camera_id, gpx, gpy, gpstime, roadname, mph) VALUES (newid(), ?, ?, ?, ?, ?, ?)", 
                (camera_id, x, y, gpstime, road, mph))
    #cur.execute("INSERT INTO tbl_heartbeatinfo( ID ,camera_id, gpx, gpy, gpstime, roadname, mph) VALUES (newid(),'E2C34D5E992F', '5678.12345', '12345.67891', 2013-4-19, '', 25)")
    conn.commit()
    cur.execute('select * from tbl_heartbeatinfo')
    for i in cur.fetchall():
        print(i)
    
    
    
    
    #cur.close()
    conn.close()
    print(conn)
except Exception as e:
    print(e)
    conn.close()
    print(conn)
