import pandas as pd
import sys
import datetime

path = ".\conf\config.xlsx"


def get_config_df():
    try:
        df = pd.read_excel(path, sheet_name="配置")
        return df
    except:
        try:
            exType, exValue, exTrace = sys.exc_info()
            nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file = open(".\log\log.txt", 'a', encoding="utf-8")
            file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
        finally:
            file.close()
