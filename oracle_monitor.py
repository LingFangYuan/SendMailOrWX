import oracle_exec
from mysql_monitor import formattext
from get_sqltext import get_sql


def get_data(path):
    """
    获取数据
    :return:
    """
    sql = get_sql(path)
    return oracle_exec.exec(sql)


def set_table(subject, path):
    re, de = get_data(path)

    content = "<strong>" + subject + "</strong><table border='1' cellpadding='5' cellspacing='0'>" \
              + '<caption><strong></strong></caption>'
    content = content + set_heads(de)
    content = content + set_rows(re)
    content = content + "</table>"
    return content


def set_heads(de):
    content = "<tr>"
    for i in range(len(de) - 1):
        content = content + "<td>" + de[i][0] + "</td>"
    content = content + "</tr>"
    return content


def set_rows(re):
    content = ''
    l = len(re[0])
    for i in re:
        content = content + ('<tr style="color:red">' if i[l - 1] == 1 else "<tr>")
        for j in range(l - 1):
            content = content + "<td>" + (oracle_exec.datetime.datetime.strftime(i[j], '%Y-%m-%d') \
                                              if isinstance(i[j], oracle_exec.datetime.datetime) else str(
                i[j])) + "</td>"
        content = content + "</tr>"
    return content


def get_html(subject, path):
    return set_table(subject, path)


def get_text(subject, path):
    re, de = get_data(path)
    text = None
    if re:
        text = formattext(re, de)
        text = subject + "\n" + text + '<a href="https://mail.qq.com/cgi-bin/loginpage">查看详情</a>'
    return text
