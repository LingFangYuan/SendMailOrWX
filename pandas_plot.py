import oracle_exec
import mysql_exec
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from get_sqltext import get_sql


class pdImage:
    def __init__(self, sql, idx, dbtype="ORACLE"):
        if dbtype.upper() == "ORACLE":
            self.df = oracle_exec.get_DataFrame(sql, idx)
        elif dbtype.upper() == "MYSQL":
            self.df = mysql_exec.get_DataFrame(sql, idx)
        else:
            pass


def get_icode(sql, subject, idx, dbtype):
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时符号-显示为方块的2问题
        pdi = pdImage(sql, idx, dbtype)
        pdi.df.plot(subplots=True, title=subject)
        plt.xlabel("")
        plt.gcf().autofmt_xdate()
        save_file = BytesIO()  # 图片写入内存
        plt.savefig(save_file, format='png')
        save_file_base64 = base64.b64encode(save_file.getvalue()).decode('utf8')  # 转换base64并以utf8格式输出
        return save_file_base64
    finally:
        del pdi


def set_html(icode):
    context = '<div></strong><br/><img src="data:image/png;base64,' \
              + icode + '"></div>'
    return context


def get_html(subject, path, index_col, dbtype):
    sql = get_sql(path)
    code = get_icode(sql, subject, index_col, dbtype)
    html = None
    if code:
        html = set_html(code)
    return html
