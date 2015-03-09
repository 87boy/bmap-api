#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import httplib
import urllib
import urllib2

from config import *

# 打开数据库连接
db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["passwd"], db=config["db"], port=config["port"], charset=config["charset"])

# 使用cursor()方法获取操作游标
cursor = db.cursor()

f_points = open("./points.txt","w")
f_poi = open("./geocoding_poi.txt","w")

# SQL 查询语句
id = 1
while (id < 1000):
    print id
    # sql = "SELECT * FROM points WHERE id ='%s'" % (id)
    sql = "SELECT * FROM temp_points_bd WHERE id ='%s'" % (id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        point = cursor.fetchone()
        # print point[0]
    except:
        print "Error: unable to fetch point"
        break

    # 当address为None或空字符串，blatitude和blongitude存在时执行
    #if (not point[5]) and point[3] and point[4]:
    if point[3] and point[4]:
        # http://api.map.baidu.com/geocoder/v2/?ak=gW3cQ4s09L4KYCnxh7VKf26P&location=39.983424,116.322987&output=json&pois=1
        ak = "gW3cQ4s09L4KYCnxh7VKf26P"
        url = "http://api.map.baidu.com/geocoder/v2/?ak=" + ak + "&location=" + str(point[4]) + "," + str(point[3]) + "&output=json&pois=1"
        response = urllib2.urlopen(url)

        data = response.read()
        # print type(data)
        data_dict = eval(data)
        # print type(data_dict)
        result = data_dict["result"]
        # print result
        pois = result["pois"]
        # print len(pois)
        uid_list = ""
        title_list = ""
        tag_list = ""
        for idx in range(len(pois)):
            poi = pois[idx]
            if (idx == len(pois)-1):
                uid_list += poi["uid"]
                title_list += poi["name"]
                tag_list += poi["poiType"]
            else:
                uid_list += poi["uid"] + ","
                title_list += poi["name"] + ","
                tag_list += poi["poiType"] + ","

            #sql = "INSERT INTO geocoding_poi(uid, name, address, longitude, latitude, telephone, postcode, poi_type, data_source, direction, distance) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (poi["uid"], poi["name"], poi["addr"], poi["point"]["x"], poi["point"]["y"], poi["tel"], poi["zip"], poi["poiType"], poi["cp"], poi["direction"], poi["distance"])
            #try:
            #   # 执行sql语句
            #   cursor.execute(sql)
            #   # 提交到数据库执行
            #   db.commit()
            #except:
            #   # Rollback in case there is any error
            #   db.rollback()
            #   print "Error: unable to insert geocoding_poi"
            f_poi.write(poi["uid"] + "\t" + poi["name"] + "\t" + poi["addr"] + "\t" + str(poi["point"]["x"]) + "\t" + str(poi["point"]["y"]) + "\t" + poi["tel"] + "\t" + poi["zip"] + "\t" + poi["poiType"] + "\t" + poi["cp"] + "\t" + poi["direction"] + "\t" + poi["distance"] + "\n")

        # print uid_list
        # print title_list
        # print tag_list
        # sql = "UPDATE points SET address = '%s', business = '%s', uid_list = '%s', title_list = '%s', tag_list = '%s' WHERE id = '%s'" % (result["formatted_address"], result["business"], uid_list, title_list, tag_list, id)
        #sql = "UPDATE temp_points_bd SET address = '%s', business = '%s', uid_list = '%s', title_list = '%s', tag_list = '%s' WHERE id = '%s'" % (result["formatted_address"], result["business"], uid_list, title_list, tag_list, id)

        #try:
        #   # 执行SQL语句
        #   cursor.execute(sql)
        #   # 提交到数据库执行
        #   db.commit()
        #except:
        #   # 发生错误时回滚
        #   db.rollback()
        #   print "Error: unable to update points"
        f_points.write(str(id) + "\t" + str(point[1]) + "\t" + str(point[2]) + "\t" + str(point[3]) + "\t" + str(point[4]) + "\t" + result["formatted_address"] + "\t" + result["business"] + "\t" + uid_list + "\t" + title_list + "\t" + tag_list + "\n")

    id += 1

# 关闭数据库连接
db.close()

f_points.close()
f_poi.close()

