# -*- coding: utf-8 -*-
#导入SQLite驱动：
import sqlite3,time

#连接到sqlite数据库
#数据库文件test.db
#如果文件不存在，自动在当前目录创建
conn = sqlite3.connect('testEX.db')

#创建一个Cursor(游标)
cursor = conn.cursor()

#执行一条SQL语句，创建user表
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

#继续执行一条SQL语句， 插入一条记录：
cursor.execute('insert into user (id, name) values (\'1\', \'Chen\')')
cursor.execute('insert into user (id, name) values (\'2\', \'Xiao\')')
cursor.execute('insert into user (id, name) values (\'3\', \'Feng\')')
#通过rowcount获得插入的行数:
# 为什么输出总是1？？
print(cursor.rowcount)
#关闭cursor
cursor.close()

#提交事务
conn.commit()
#关闭connection
conn.close()



#延时查询记录
time.sleep(1)
#连接数据库
conn = sqlite3.connect('testEX.db')
#创建游标
cursor = conn.cursor()
#执行查询语句：
i = 1
while i<4:
	cursor.execute('select * from user where id=? ', (i,))
	i += 1
	#获得查询结果集：
	values= cursor.fetchall()

	print(values)

cursor.close()

conn.close
