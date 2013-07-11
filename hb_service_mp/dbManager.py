# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

try:
    import pyodbc
except:
    print('no module pyodbc, should init first!')

# self module
#import myLog

DB_HOST = '10.20.1.129' # '210.73.152.201'
USER = 'sa'
PWD = 'skcl@2013'
DATABASE = 'CDMTCP'

def get_db_connect():
    db_conn = None
    try:
        db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    except: # not print db execption yet
        #myLog.mylogger.debug('init db got an error!')
        print('init db got an error!')
    return db_conn

def close_db_connect(db_conn):
    if db_conn:
        db_conn.close()
