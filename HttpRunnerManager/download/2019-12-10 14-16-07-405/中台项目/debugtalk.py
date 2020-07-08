# debugtalk.py
import pymysql
import requests
def select(table,id):
    conn = pymysql.connect(host="127.0.0.1", user="root",password="admin",db="httprunner",port=3306)
    cursor = conn.cursor()
    sql ="select * from %s where id = %s order by id desc "%(table,id)
    cursor.execute(sql)
    results = cursor.fetchall()

    print(results[0][4])
    cursor.close()
    conn.close()
    return results[0][4]
def get_file(filePath="D:\\dss.jpg"):
    return open(filePath, "rb")
