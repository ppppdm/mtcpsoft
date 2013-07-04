# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

try:
    import pyodbc
except:
    print('no module pyodbc, should init first!')
import threading
import time

# self module
import myLog
import globalConfig

DB_HOST = '10.20.1.200' # '210.73.152.201'
USER = 'sa'
PWD = 'sa'
DATABASE = 'CDMTCP'

DB_CONNECT_LOCK = threading.Lock()

MAX_DB_CONNECT = 1000
DB_CONNECT_NOT_USE_LIST = list()
DB_CONNECT_USED_LIST = list()


def init_db_connect_list(conn_num = MAX_DB_CONNECT):
    for i in range(conn_num):
        try:
            db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_NOT_USE_LIST.append(db_conn)
            # release lock
            DB_CONNECT_LOCK.release()
        except: # not print db execption yet
            myLog.mylogger.error('init db got an error!')
            print('init db got an error!')
            break
    print('init db conn done! connections :', len(DB_CONNECT_NOT_USE_LIST))
    myLog.mylogger.debug('init db conn done!')
    return

def get_one_db_connect():
    db_conn = None
    try:
        # lock
        DB_CONNECT_LOCK.acquire()
        db_conn = DB_CONNECT_NOT_USE_LIST.pop()
        DB_CONNECT_USED_LIST.append(db_conn)
        # release lock
        DB_CONNECT_LOCK.release()
        
    except ValueError:
        print('not enough db_conn!')
        myLog.mylogger.error('not enough db_conn!')
    except Exception as e:
        print(e)
        myLog.mylogger.error(e)
    return db_conn

def close_one_db_connect(conn):
    if conn:
        # if the conn is usable
        try:
            conn.commit()
        except : # not print db except  yet
            print('connect can not used')
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_USED_LIST.remove(conn)
            # release lock
            DB_CONNECT_LOCK.release()
            return
        
        try:
            # lock
            DB_CONNECT_LOCK.acquire()
            DB_CONNECT_USED_LIST.remove(conn)
            DB_CONNECT_NOT_USE_LIST.append(conn)
            # release lock
            DB_CONNECT_LOCK.release()
        except Exception as e:
            print(e)
            myLog.mylogger.error(e)
    return

def get_db_connect():
    db_conn = None
    try:
        db_conn = pyodbc.connect('DRIVER={SQL Server}', host = DB_HOST, user = USER, password = PWD, database = DATABASE)
    except: # not print db execption yet
        myLog.mylogger.debug('init db got an error!')
        print('init db got an error!')
    return db_conn

def close_db_connect(db_conn):
    if db_conn:
        db_conn.close()

DB_REPAIR_TIME = 3600 # sec


def db_connect_server():
    # check the useable db connect number in the db connect list every one hour
    while True:
        time.sleep(DB_REPAIR_TIME)
        # lock
        DB_CONNECT_LOCK.acquire()
        total_conn = len(DB_CONNECT_NOT_USE_LIST) + len(DB_CONNECT_USED_LIST)
        # release lock
        DB_CONNECT_LOCK.release()
        
        print('total db connect :', total_conn)
        if total_conn < (MAX_DB_CONNECT >> 1):
            init_db_connect_list(MAX_DB_CONNECT - total_conn)
    
    return

def init_db():
    # init db args
    global SERVER_PORT, DB_HOST, USER, PWD
    SERVER_PORT = globalConfig.SERVER_PORT
    DB_HOST     = globalConfig.DB_HOST
    USER        = globalConfig.USER
    PWD         = globalConfig.PWD
    
    
    # do two things
    # one to init db connect list(db connect pool)
    t1 = threading.Thread(target=init_db_connect_list)
    t1.start()
    
    # two to start db connect repair service
    t2 = threading.Thread(target=db_connect_server)
    t2.start()
    
    return
