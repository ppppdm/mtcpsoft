# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

# 专门处理 update 数据库表的工作线程/进程

import queue
import dbManager


# 用于缓存其他处理线程sql语句的队列
q = queue.Queue()

def update_db_server():
    conn = dbManager.get_db_connect()
    cur = conn.cursor()
    while True:
        sql, gpx, gpy, gpstime, roadname, mph, createtime, camera_id = q.get()
        q.task_done()
        print(gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
        try:
            cur.execute(sql, gpx, gpy, gpstime, roadname, mph, createtime, camera_id)
        except:
             print('update db excute error!\n')
    
    dbManager.close_db_connect(conn)
    return



