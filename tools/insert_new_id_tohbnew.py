# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# ------------------------------------------- DB API ----------------------------------------------
import pyodbc

DB_HOST = '10.20.1.129' #'192.168.1.5\\MTCP12' # '210.73.152.201' # 
USER = 'sa'
PWD = 'skcl@2013'
DATABASE = 'CDMTCP'


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

def execute_sql(sql):
    ret = None
    conn = get_db_connect()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
            #cur.commit()
        except:
            print('Error while execute sql :', sql)
        ret = cur.fetchall()
    close_db_connect(conn)
    return ret

# -------------------------------------------------------------------------------------------------

new_id_list = ['08002812E315',
'08002812E313',
'08002812E2BE',
'08002812E32A',
'08002812E2C5',
'08002812E32B',
'08002812E31D',
'08002812E2DF',
'08002812E318',
'08002812E319',
'08002812E317',
'08002812E304',
'08002812E2C7',
'08002812E330',
'08002812E320',
'08002812E311',
'08002812E2C4',
'08002812E346',
'08002812E316',
'08002812E2C6',
'08002812E2BB',
'08002812E2BD',
'08002812E32C',
'08002812E312',
'08002812E30C',
'08002812E314',
'08002812E2CF',
'08002812E32F',
'08002812E309',
'08002812E310',
'08002812E32D',
'08002812E30F',
'08002812E2CD',
'08002812E338',
'08002812E2CB',
'08002812E2EB',
'08002812E2D1',
'08002812E341',
'08002812E2D6',
'08002812E2EE',
'08002812E2F0',
'08002812E345',
'08002812E30D',
'08002812E31F',
'08002812E30A',
'08002812E2F1',
'08002812E2C1',
'08002812E342',
'08002812E2C3',
'08002812E2BA',
'08002812E2B9',
'08002812E2F3',
'08002812E33F',
'08002812E2FB',
'08002812E2E9',
'08002812E2D3',
'08002812E343',
'08002812E323',
'08002812E2F7',
'08002812E334',
'08002812E2FD',
'08002812E2C2',
'08002812E2BF',
'08002812E2CE',
'08002812E2DD',
'08002812E2E4',
'08002812E2CA',
'08002812E326',
'08002812E2BC',
'08002812E306',
'08002812E2ED',
'08002812E2D7',
'08002812E2DE',
'08002812E2DA',
'08002812E2E5',
'08002812E2C0',
'08002812E2EA',
'08002812E2D8',
'08002812E2DC',
'08002812E301',
'08002812E303',
'08002812E2DB',
'08002812E2E1',
'08002812E2E3',
'08002812E31B',
'08002812E2E2',
'08002812E302',
'08002812E31C',
'08002812E322',
'08002812E2FF',
'08002812E2F9',
'08002812E2D9',
'08002812E2E0',
'08002812E321',
'08002812E2CC',
'08002812E327',
'08002812E324',
'08002812E2FA',
'08002812E2FE',
'08002812E325',
'08002812E2F2',
'08002812E2D4',
'08002812E300',
'08002812E307',
'08002812E2EC',
'08002812E2D0',
'08002812E30E',
'08002812E2FC',
'08002812E333',
'08002812E2F5',
'08002812E340',
'08002812E33E',
'08002812E2D5',
'08002812E2E8',
'08002812E308',
'08002812E305',
'08002812E2F6',
'08002812E33C',
'08002812E32E',
'08002812E2F4',
'08002812E2C9',
'08002812E33A',
'08002812E328',
'08002812E2E6',
'08002812E30B',
'08002812E2C8',
'08002812E335',
'08002812E33D',
'08002812E33B',
'08002812E31A',
'08002812E31E',
'08002812E337',
'08002812E329',
'08002812E2E7',
'08002812E2F8',
'08002812E331',
'08002812E2EF',
'08002812E339',
'08002812E332',
'08002812E344',
'08002812E336',
'08002812E2D2'
               ]
def formate_camera_id(id):
    new_id = ''
    for i in range(0, len(id), 2):
        new_id += id[i]+id[i+1]+'-'
    return new_id.strip('-')


def insert_to_hb_new(conn, id_list):
    sql = "insert into tbl_heartbeatinfo_new (id, camera_id) values (newid(),?)"
    if conn:
        cur = conn.cursor()
        try:
            cur.executemany(sql, id_list)
            cur.commit()
            print('DB exectue success')
        except:
            print('DB execute Error!')
        
    return

if __name__ == "__main__":
    conn = get_db_connect()
    if conn is None:
        print('get db conn error')
        exit()
    #update_picture_name_db(conn, old_list)
    formated_id_list = list()
    for i in new_id_list:
        formated_id_list.append([formate_camera_id(i)])
    print(formated_id_list)
    insert_to_hb_new(conn, formated_id_list)
    close_db_connect(conn)
    
