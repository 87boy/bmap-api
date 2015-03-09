#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time

import httplib
import urllib
import urllib2

from config import *

# 打开数据库连接
db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["passwd"], db=config["db"], port=config["port"], charset=config["charset"])

# 使用cursor()方法获取操作游标
cursor = db.cursor()

num = 1
step = 50000
code = 10000000
ak_list = ["gW3cQ4s09L4KYCnxh7VKf26P", "gW3cQ4s09L4KYCnxh7VKf26P","tNHET2neEmHEyo8WLw3FLQGw", "ZDWXrmaGhFNjMo27nzZRooZl", "gW3cQ4s09L4KYCnxh7VKf26P", "hIlimGuvEfHV41Aw885gONzB", "g7ncsSZh5svImST9z2fa0XMb", "8sqYxwSpfij93KzfsOYeiK3H", "rOG0SvFic7DQFme8Ey71wizl", "rOG0SvFic7DQFme8Ey71wizl", "43qLNfw2Mx9xQzemk9X0WbB1", "lkqz7BPQWAVIWzA4lWQCSaoB", "6gpm7mWVHGQcFvsH3wLUEsWg", "Sj11ofN664YGuGgNP1R0iCF1", "8iPBLiCFtTvGiQZIrDFYN1Nl", "nrgFFHHFyjrbXYQWBl56EQZq", "KDdzQZSRLv89h4yrti56L5Gy", "FHqz3mdQDrtB5cHvNiFPwW60", "Y4ToKdFKFdWxeLqEBVLVR46T", "WQhNjVVcGorsc2FT8SeGWLXz", "vtoMAnyjb5rUDSvY4VHIWS1G", "aoIHPLcgMRSYPR9tirgrB2jY", "tXQFzeszwKK3H4sKlie5463h", "rOG0SvFic7DQFme8Ey71wizl", "rOG0SvFic7DQFme8Ey71wizl"]
ak = ak_list[num]
i = 1 + step * ( num - 1 )
max = 1 + step * num
poi_id = code * num

points_table = "temp_20150115top1000_points"
geocoding_poi_table = "temp_20150115top1000_geocoding_poi_" + str(num)

coordtype = "wgs84ll"

logfile = "./baidu_poi_" + str(num) + ".log"
log = open(logfile, "a")
current_time = time.strftime( '%Y-%m-%d %X', time.localtime() )

sql = "SELECT * FROM " + geocoding_poi_table +  " ORDER BY id DESC LIMIT 1"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取一条记录
    poi_max = cursor.fetchone()
except:
    # print "Error: first query geocoding_poi fail"
    log.write(current_time + "\tError: first query geocoding_poi fail\n")
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取一条记录
        poi_max = cursor.fetchone()
    except:
        # print "Error: second query geocoding_poi fail"
        log.write(current_time + "\tError: first query geocoding_poi fail\n")
        # 关闭数据库连接
        db.close()
        # 关闭日志文件
        log.close()
        exit()

if (poi_max):
    poi_id = int(poi_max[0])

while (i < max):
    # print i
    current_time = time.strftime( '%Y-%m-%d %X', time.localtime() )
    log.write(current_time + "\t" + str(i) + "\n")
    # sql = "SELECT * FROM points WHERE id ='%s'" % (i)
    sql = "SELECT * FROM " + points_table + " WHERE id ='%s'" % (i)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        point = cursor.fetchone()
        # print point[0]
    except:
        # print "Error: first query point fail"
        log.write(current_time + "\tError: first query point fail\n")
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            point = cursor.fetchone()
            # print point[0]
        except:
            # print "Error: second query point fail"
            log.write(current_time + "\tError: second query point fail\n")
            break

    # 当address为None或空字符串，blatitude和blongitude存在时执行
    if (not point[5]) and point[1] and point[2]:
        # http://api.map.baidu.com/geocoder/v2/?ak=gW3cQ4s09L4KYCnxh7VKf26P&coordtype=wgs84ll&location=39.983424,116.322987&output=json&pois=1
        url = "http://api.map.baidu.com/geocoder/v2/?ak=" + ak + "&coordtype=" + coordtype + "&location=" + str(point[2]) + "," + str(point[1]) + "&output=json&pois=1"
        try:
            response = urllib2.urlopen(url, timeout=10)
            data = response.read()
            # print type(data)
            data_dict = eval(data)
            # print type(data_dict)
            result = data_dict["result"]
            # print result
            pois = result["pois"]
            # print len(pois)
        except:
            # print "Error: first urlopen fail"
            log.write(current_time + "\tError: first urlopen fail\n")
            try:
                response = urllib2.urlopen(url, timeout=10)
                data = response.read()
                # print type(data)
                data_dict = eval(data)
                # print type(data_dict)
                result = data_dict["result"]
                # print result
                pois = result["pois"]
                # print len(pois)
            except:
                # print "Error: second urlopen fail"
                log.write(current_time + "\tError: second urlopen fail\n")
                try:
                    response = urllib2.urlopen(url, timeout=10)
                    data = response.read()
                    # print type(data)
                    data_dict = eval(data)
                    # print type(data_dict)
                    result = data_dict["result"]
                    # print result
                    pois = result["pois"]
                    # print len(pois)
                except:
                    # print "Error: third urlopen fail"
                    log.write(current_time + "\tError: third urlopen fail\n")
                    log.write(url)
                    break

        id_list = ""
        uid_list = ""
        title_list = ""
        tag_list = ""
        for idx in range(len(pois)):
            poi_id += 1;
            poi = pois[idx]
            if (idx == len(pois)-1):
                id_list += str(poi_id)
                uid_list += poi["uid"]
                title_list += poi["name"]
                tag_list += poi["poiType"]
            else:
                id_list += str(poi_id) + ","
                uid_list += poi["uid"] + ","
                title_list += poi["name"] + ","
                tag_list += poi["poiType"] + ","

            sql = "INSERT INTO " + geocoding_poi_table + "(id, uid, name, address, longitude, latitude, telephone, postcode, poi_type, data_source, direction, distance) VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (poi_id, poi["uid"], poi["name"].replace("'","''"), poi["addr"].replace("'","''"), poi["point"]["x"], poi["point"]["y"], poi["tel"], poi["zip"], poi["poiType"], poi["cp"], poi["direction"], poi["distance"])
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
                # print "Error: first insert geocoding_poi fail"
                log.write(current_time + "\tError: first insert geocoding_poi fail\n")
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
                    # print "Error: second insert geocoding_poi fail"
                    log.write(current_time + "\tError: second insert geocoding_poi fail\n")
                    log.write(url)
                    # 关闭数据库连接
                    db.close()
                    # 关闭日志文件
                    log.close()
                    exit()

        # print uid_list
        # print title_list
        # print tag_list
        sql = "UPDATE " + points_table + " SET address = '%s', business = '%s', id_list = '%s', uid_list = '%s', title_list = '%s', tag_list = '%s' WHERE id = '%s'" % (result["formatted_address"], result["business"], id_list, uid_list, title_list.replace("'","''"), tag_list.replace("'","''"), i)

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            # print "Error: first update points fail"
            log.write(current_time + "\tError: first update points fail\n")
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()
                # print "Error: second update points fail"
                log.write(current_time + "\tError: second update points fail\n")
                log.write(url)
                break

    i += 1

# 关闭数据库连接
db.close()
# 关闭日志文件
log.close()
