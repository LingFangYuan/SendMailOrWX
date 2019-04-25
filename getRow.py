import cx_Oracle  # 引用模块cx_Oracle
import setHtml
import sendMail

user = '***'
passwd = '****'
db = '*****'

def get_conn():
    conn = cx_Oracle.connect(user + '/' + passwd + '@' + db)  # 连接数据库
    c = conn.cursor()  # 获取cursor
    return conn, c


def close_conn(conn, c):
    c.close()  # 关闭cursor
    conn.close()  # 关闭连接


def getHtml(sql, subject, inx):
    conn, c = get_conn()
    try:
        try:
            x = c.execute(sql)
            rs = x.fetchall()
            content = ""
            for i in rs:
                content = setHtml.setRow(i, content)
            content = setHtml.setH3Table(subject, content, inx)
            return content
        except Exception as e:
            sendMail.send("APP数仓监控程序出错", str(e), 'plain')
    finally:
        close_conn(conn, c)


def getError(sql):
    conn, c = get_conn()
    try:
        try:
            x = c.execute(sql)
            rs = x.fetchall()
            content = None
            for i in rs:
                if content is None:
                    content = i[0] + " " + i[1]
                else:
                    content = content + "\n" + i[0] + " " + i[1]
            return content
        except Exception as e:
            sendMail.send("APP数仓监控程序出错", str(e), 'plain')
    finally:
        close_conn(conn, c)
