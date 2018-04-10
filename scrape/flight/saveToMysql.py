# -*- coding: utf-8 -*-
# !/usr/bin/env python

import MySQLdb
import sys
import time

def db_con_save():
    db = MySQLdb.connect("127.0.0.1",""---------"",""---------"",""---------"")
    cursor = db.cursor()
    return db,cursor

def closeSaveDb(db):
    db.close()

def save(dict, db, cursor):
    if len(dict) == 0:
        return
    sql = "SELECT * FROM fightInfo WHERE FlightNo='%s' AND fightDate='%s'" % (dict["FlightNo"],dict["fightDate"])
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            sql = updateData(dict, db)
        else:
            sql = insertData(dict, db)    
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print("SQL ERROR!!! : ", sys.exc_info()[0])

def insertData(dict, db):
    dict["creatTime"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cols = ', '.join(dict.keys())
    values = ', '.join(('\''+str(e)+'\'') for e in dict.values())
    sql = "INSERT INTO fightInfo (%s) VALUES (%s)" % (cols, values)
    return sql

def updateData(dict, db):
    dict["updateTime"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    data = ""
    for k,v in dict.items():
        data += k + "='" + str(v) + "\',"
    sql = "UPDATE fightInfo SET " + str(data[0:len(data)-1]) 
    sql += " WHERE FlightNo='%s' and fightDate='%s' " % (dict["FlightNo"],dict["fightDate"])
    return sql







