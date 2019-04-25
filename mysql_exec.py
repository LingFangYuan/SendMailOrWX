import pymysql
import sys
import datetime
import pandas as pd

host = '****'
port = 3306
user = '******'
passwd = '*******'
database = '******'


def get_db():
    """
    获取mysql db连接和cursor游标
    :return: db,cursor
    """
    db = pymysql.connect(host=host, port=port, user=user, password=passwd, db=database)
    cursor = db.cursor()
    return db, cursor


def close_db(db):
    """
    关闭mysql db数据连接
    :return:
    """
    db.close()


def exec_sql(cursor, sql):
    """
    执行sql脚本
    :param cursor: 访问游标
    :param sql: 执行的sql脚本
    :return:
    """
    cursor.execute(sql)
    return cursor.fetchall()


def exec(sql):
    """
    连接、执行、关闭
    :param sql: 需要执行的sql脚本
    :return:
    """
    try:
        db, cursor = get_db()
        try:
            return exec_sql(cursor, sql), cursor.description
        except:
            try:
                exType, exValue, exTrace = sys.exc_info()
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file = open(".\log\log.txt", 'a', encoding="utf-8")
                file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
            finally:
                file.close()
    finally:
        close_db(db)


def get_DataFrame(sql, idx):
    """"
    连接、执行、关闭
    :param
    sql: 需要执行的sql脚本
    :return: pandas 数据帧
    """
    try:
        db, cursor = get_db()
        try:
            return pd.read_sql(sql, db, index_col=idx)
        except:
            try:
                exType, exValue, exTrace = sys.exc_info()
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file = open(".\log\log.txt", 'a', encoding="utf-8")
                file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
            finally:
                file.close()
    finally:
        close_db(db)
