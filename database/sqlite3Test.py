# -*- coding: utf-8 -*-
import os, sqlite3
#os.path 模块主要用于获取文件的属性。
#os.path.dirname(path):返回文件路径
#os.path.join(path1[, path2[, ...]]):把目录和文件名合成一个路径
db_file = os.path.jion(os.path.dirname(__file__),'test.db')
#os.path.isfile(path):判断路径是否为文件
if os.path.isfile(db_file):
	#os.remove() 方法用于删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。
	os.remove(db_file)
#初始化数据：

conn = sqlite3.conect(db_file)