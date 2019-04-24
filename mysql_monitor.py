import mysql_exec
from get_sqltext import get_sql


# sql_path = ".\sql\异常单据监控.sql"


def formattext(data, desc):
    content = None
    for i in range(len(desc)):
        content = (content if content is not None else "") \
                  + desc[i][0] + ("\n" if i == len(desc) - 1 else ",")
    for i in data:
        for j in range(len(i)):
            content = content + str(i[j]) \
                      + ("" if j == len(i) - 1 else ",")
        content = content + "\n"
    return content


def get_text(subject, path):
    sql = get_sql(path)
    data, desc = mysql_exec.exec(sql)
    text = None
    if data:
        text = formattext(data, desc)
        text = subject + "\n" + text + '<a href="https://mail.gialen.com:8443/coremail/">查看详情</a>'
    return text
