# -*- coding:utf8 -*-
# auther : pdm
# email : ppppdm@gmail.com

import pyodbc

HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'

try:
    conn = pyodbc.connect('DRIVER={SQL Server}', host = HOST, user = USER, password = PWD, database = DATABASE)
   
    print(conn)
    cur = conn.cursor()
    cur.execute('sp_help tbl_heartbeatinfo')
    
    for i in cur.fetchall():
        print(i)
    
    conn.commit()
    cur.execute('select count(*) from tbl_heartbeatinfo')
    for i in cur.fetchall():
        print(i)

    conn.close()
    print(conn)
except Exception as e:
    print(e)
