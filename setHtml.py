import datetime

heads = [["执行日期", "模块", "过程数", "模块最早开始时间", "模块最晚结束时间", "模块完成耗时", "完成状态"],
         ["执行日期", "存储过程名称", "模块", "完成状态"]]


def setRow(rows, content):
    temp = ''
    l = len(rows)
    for i in range(l):
        if i == 0:
            temp = temp + "<td>" + datetime.datetime.strftime(rows[i], '%Y-%m-%d') + "</td>"
        else:
            temp = temp + "<td>" + str(rows[i]) + "</td>"
    else:
        temp = content + ('<tr style="color:red">' if (rows[l - 1] == 'E' or rows[l - 1].find("失败") >= 0) \
                              else "<tr>") + temp + "</tr>"
    return temp


def setHeads(content, inx):
    temp = ''
    head = heads[inx]
    for i in head:
        temp = temp + "<td>" + str(i) + "</td>"
    else:
        temp = "<tr>" + temp + "</tr>" + content
    return temp


def setH3Table(subject, content, inx):
    content = setHeads(content, inx)
    content = "<h3>" + subject + "<table border='1' cellpadding='5' cellspacing='0'>" \
              + content + "</table><h3>"
    return content
