import pymysql

def bdd_login():
    conn = pymysql.connect(host='192.168.0.26', port=3308, user='root', passwd='', db='projet')
    cur = conn.cursor()
    return cur
