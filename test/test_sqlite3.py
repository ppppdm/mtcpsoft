# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com


import sqlite3

conn = sqlite3.connect(':memory:')

cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, vv INTEGER)')

print(cur.execute('SELECT count(*) FROM test').fetchall()) # 0
cur.execute('INSERT INTO test VALUES (NULL,1001)')
print(cur.execute('SELECT count(*) FROM test').fetchall()) # 1
