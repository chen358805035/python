#导入mysql驱动
import mysql.connector

#连接数据库
#.ibd是MySQL数据文件、索引文件
#.frm是表结构文件
conn = mysql.connector.connect(user='root', password='', database='test')

#创建cursor
cursor = conn.cursor()

#创建user表：
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

#插入一条记录：
cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'chen'])

#提交事务
conn.commit()

#关闭cursor
cursor.close()

#运行查询：
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()

print(values)

cursor.close()
conn.close()
