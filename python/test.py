#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

from config import *

# 打开数据库连接
db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["passwd"], db=config["db"], port=config["port"], charset=config["charset"])

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION();")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

print "Database version : %s " % data

# 关闭数据库连接
db.close()
