# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# 与图片文件按照日期进行归类存放在子文件下 协同进行
# 对数据库表Ls_pictures 的字段 picture_name 更新

import os

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

SQL1 = "SELECT id, picture_name FROM LS_pictures WHERE (recieve_picture_nums IS NOT NULL);"
SQL2 = "SELECT id, picture_name FROM LS_pictures WHERE (recieve_picture_nums IS NOT NULL) AND ( id = '597029');"
SQL3 = "SELECT id, picture_name FROM LS_pictures WHERE (recieve_picture_nums IS NOT NULL) AND (data_direction is NULL);"
SQL4 = "SELECT id, picture_name FROM LS_pictures WHERE (recieve_picture_nums IS NOT NULL) AND (data_direction is NULL) AND ( id = '597029');"

# 日期格式化
def formate_date(date_str):
    return date_str[:4] + '-' + date_str[4:6]+ '-' + date_str[6:]

# 通过旧名字获取新名字
def get_new_name(old_name):
    new_name = ''
    old_names = old_name.split(',')
    for name in old_names:
        if '/' not in name and '\\\\' not in name:
            date = name[:8]
            sec_dir = formate_date(date)
            new_name += sec_dir + '/' + name + ','
        else:
            return old_name
    new_name = new_name.strip(',')
    return new_name

def update_picture_name_db(conn, old_list):
    if conn:
        cur = conn.cursor()
        for id, pic_name in old_list:
            new_pic_name = get_new_name(pic_name)
            print('new_pic_name', new_pic_name)
            try:
                cur.execute("UPDATE LS_pictures SET picture_name = ? WHERE (id = ?);", (new_pic_name, id))
                cur.commit()
            except:
                print('DB execute Error!')
    return

def reget_name_and_directory(old_name):
    new_name = ''
    dir = ''
    old_names = old_name.split(',')
    for name in old_names:
        if '/' in name or '\\\\' in name:
            new_name += os.path.basename(name) + ','
            dir += os.path.dirname(name) + ','
        else:
            return old_name, '.'
    new_name = new_name.strip(',')
    dir = dir.strip(',')
    return new_name, dir

def reset_picture_name_and_data_direction(conn, old_list):
    if conn:
        cur = conn.cursor()
        for id, pic_name in old_list:
            new_pic_name, data_direction = reget_name_and_directory(pic_name)
            print('new_pic_name', new_pic_name)
            print('data_direction', data_direction)
            try:
                cur.execute("UPDATE LS_pictures SET picture_name = ?, data_direction = ? WHERE (id = ?);", (new_pic_name, data_direction, id))
                cur.commit()
            except:
                print('DB execute Error!')
    return

if __name__=="__main__":
    old_list = execute_sql(SQL4)
    conn = get_db_connect()
    if conn is None:
        print('get db conn error')
        exit()
    #update_picture_name_db(conn, old_list)
    reset_picture_name_and_data_direction(conn, old_list)
    close_db_connect(conn)
