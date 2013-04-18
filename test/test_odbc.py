# -*- coding:utf8 -*-
# auther : pdm
# email : ppppdm@gmail.com

import pyodbc
#help(pyodbc.Cursor)
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.20.1.129;DATABASE=bus2;UID=sa;PWD=sa')
    print(conn)
    cur = conn.cursor()
    cur.execute('sp_helpdb')
    for i in cur.fetchall():
        print(i)
    #cur.execurt('select * from tbl_heartbeatinfo')
    #for i in cur.fetchall():
    #    print(i)
    
    cur.close()
    conn.close()
    print(conn)
except Exception as e:
    print(print(e.args[1]))
