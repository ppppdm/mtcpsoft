# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# 专门处理 update 数据库表的工作线程/进程

import queue
import dbManager
import time


# 用于缓存其他处理线程sql语句的队列
q = queue.Queue()

def update_db_server():
    if_sql = "if not exists( select * from tbl_heartbeatinfo_new where camera_id = ?)"
    insert_sql = "insert into tbl_heartbeatinfo_new (id, camera_id, gpx, gpy, gpstime, roadname, mph, createtime) values ( newid(),?,?,?,?,?,?,?)"
    else_sql = "else update tbl_heartbeatinfo_new set gpx = ?, gpy = ?, gpstime = ?, roadname = ?, mph = ?, createtime = ? where (camera_id = ?)"
    sql = if_sql+insert_sql+else_sql
    conn = dbManager.get_db_connect()
    cur = conn.cursor()
    arg_list = list()
    print('update_db_server running')
    time_wait = 1
    get_num =100
    while True:
        #print('in while update db')
        for i in range(get_num):
            try:
                gpx, gpy, gpstime, roadname, mph, createtime, camera_id = q.get(False)
                q.task_done()
                
                sql_param = (camera_id, camera_id, gpx, gpy, gpstime, roadname, mph, createtime, gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
                arg_list.append(sql_param)
                
            except queue.Empty:
                print('empty')#
                get_num = max(5, len(arg_list))
                break
        
        if get_num == len(arg_list):
            get_num += 10
        
        #print(gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
        #print(arg_list)
        if len(arg_list) != 0:
            #print(arg_list)
            try:
                cur.executemany(sql, arg_list)
                conn.commit()
                print('execute success')
            except:
                print('update db excute error!\n')
            arg_list.clear()
        print('time_wait', time_wait, 'get_num', get_num)
        time.sleep(time_wait)
    
    dbManager.close_db_connect(conn)
    return



