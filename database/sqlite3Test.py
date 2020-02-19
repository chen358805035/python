# -*- coding: utf-8 -*-
import os, sqlite3
#os.path 模块主要用于获取文件的属性。
#os.path.dirname(path):返回文件路径
#os.path.join(path1[, path2[, ...]]):把目录和文件名合成一个路径
db_file = os.path.join(os.path.dirname(__file__),'test.db')
#os.path.isfile(path):判断路径是否为文件
if os.path.isfile(db_file):
	#os.remove() 方法用于删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。
	os.remove(db_file)
#初始化数据：
#连接数据库
conn = sqlite3.connect(db_file)
#创建cursor
cursor = conn.cursor()
#创建user表
cursor.execute('create table user (id varchasr(20) primary key, name varchar(20),score int)')
#插入记录：
cursor.execute(r"insert into user values ('A-OO1', 'chen', 95)")
cursor.execute(r"insert into user values ('A-002', 'xiao', 62)")
cursor.execute(r"insert into user values ('A-003', 'feng', 78)")
cursor.close()
conn.commit()
conn.close()

def get_score_in(low, high):
#    ' 返回指定分数区间的名字，按分数从低到高排序 '
#刚开始我是想将所有数据提取出来，判断排序；看了评论发现SQL语句中有筛选排序
	conn = sqlite3.connect(db_file)

	cursor = conn.cursor()

	cursor.execute('select id, name, score from user where score between ? and ? order by score', (low,high))

	values = cursor.fetchall()
	result = []
	for i in values:
		result.append(i[1])

	cursor.close()

	conn.close()
	return result

if __name__ == '__main__':
	print(get_score_in(10,99))

