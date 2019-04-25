import cx_Oracle  # 引用模块cx_Oracle
import sys
import datetime
import pandas as pd

username = '***'
password = '*****'
datebase = '*****'

class myoracle:

    def __init__(self, user=username, passwd=password, db=datebase):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.get_conn()

    def __del__(self):
        self.close_conn()

    def get_conn(self):
        """
        获取连接和游标
        :return:
        """
        self.conn = cx_Oracle.connect(user + '/' + passwd + '@' + db)  # 连接数据库
        self.c = self.conn.cursor()  # 获取cursor

    def close_conn(self):
        """
        关闭连接和游标
        :return:
        """
        self.c.close()  # 关闭cursor
        self.conn.close()  # 关闭连接

    def exec_sql(self, sql):
        """
        执行sql脚本
        :param cursor: 访问游标
        :param sql: 执行的sql脚本
        :return:
        """
        self.c.execute(sql)
        return self.c.fetchall(), self.c.description


def exec(sql):
    """
    连接、执行、关闭
    :param sql: 需要执行的sql脚本
    :return:
    """
    try:
        oracle = myoracle()
        try:
            return oracle.exec_sql(sql)
        except:
            try:
                exType, exValue, exTrace = sys.exc_info()
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file = open(".\log\log.txt", 'a', encoding="utf-8")
                file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
            finally:
                file.close()
    finally:
        del oracle


def get_DataFrame(sql, idx):
    """"
    连接、执行、关闭
    :param
    sql: 需要执行的sql脚本
    :return: pandas 数据帧
    """
    try:
        oracle = myoracle()
        try:
            return pd.read_sql(sql, oracle.conn, index_col=idx)
        except:
            try:
                exType, exValue, exTrace = sys.exc_info()
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file = open(".\log\log.txt", 'a', encoding="utf-8")
                file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
            finally:
                file.close()
    finally:
        del oracle
