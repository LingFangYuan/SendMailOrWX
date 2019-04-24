import getRow
import sendMail
import mysql_monitor
import sendWX
import oracle_monitor
import pandas_plot
import config

sql1 = """
SELECT DT 执行日期,
       MOD 模块,
       COUNT(1)  过程数,
       MIN(BEGINTIME)  模块最早开始时间,
       MAX(ENDTIME)  模块内最晚结束时间,
       ROUND((MAX(ENDTIME) - MIN(BEGINTIME)) * 24 * 60, 2)||'分钟' 模块完成耗时,
       SUCCESS_FLAG 完成状态
  FROM SYS_PROC_RUN_LOG
 WHERE DT = TRUNC(SYSDATE)
 GROUP BY DT, MOD, SUCCESS_FLAG
UNION ALL
SELECT TRUNC(BEGINDATE),
       'ODS',
       COUNT(*),
       MIN(BEGINDATE) ,
       MAX(ENDDATE) ,
       ROUND((MAX(ENDDATE) - MIN(BEGINDATE)) * 24 * 60, 2) ||'分钟',
       STATE
  FROM ODS_ETL_LOG
 WHERE TYPE = 'ODS'
   --AND STATE LIKE '%成功%'
   AND TRUNC(BEGINDATE) = TRUNC(SYSDATE)
 GROUP BY TRUNC(BEGINDATE), STATE
 ORDER BY 模块最早开始时间,模块
"""
sql2 = """
SELECT DT 执行时间, SP_NAME 存储过程名称, MOD 模块, SUCCESS_FLAG 完成状态
  FROM SYS_PROC_RUN_LOG
 WHERE DT = TRUNC(SYSDATE)
   AND SUCCESS_FLAG <> 'S'

UNION ALL

SELECT TRUNC(BEGINDATE),NAME , 'ODS' MOD, STATE
  FROM ODS_ETL_LOG
 WHERE TYPE = 'ODS'
       AND STATE  LIKE '%失败%'
   AND TRUNC(BEGINDATE) = TRUNC(SYSDATE)
"""
sql3 = """
SELECT DISTINCT SP_NAME NAME,  SUCCESS_FLAG STATE
  FROM SYS_PROC_RUN_LOG
 WHERE DT = TRUNC(SYSDATE)
   AND SUCCESS_FLAG <> 'S'
   UNION ALL
SELECT DISTINCT NAME, STATE
  FROM ODS_ETL_LOG
 WHERE TYPE = 'ODS'
       AND STATE  LIKE '%失败%'
   AND TRUNC(BEGINDATE) = TRUNC(SYSDATE)
   """


def get_content():
    df = config.get_config_df()
    for i in range(len(df)):
        if df.loc[i, "状态"] == "启用":
            if df.loc[i, "发送方式"] == "微信" and df.loc[i, "发送类型"] == "文本" and df.loc[i, "数据库"].upper() == "MYSQL":
                temp = mysql_monitor.get_text(df.loc[i, "主题"], df.loc[i, "SQL路径"])
                if temp is not None:
                    wx_contents.append([temp, df.loc[i, "接收人"]])
            elif df.loc[i, "发送方式"] == "微信" and df.loc[i, "发送类型"] == "文本" and df.loc[i, "数据库"].upper() == "ORACLE":
                temp = oracle_monitor.get_text(df.loc[i, "主题"], df.loc[i, "SQL路径"])
                if temp is not None:
                    wx_contents.append([temp, df.loc[i, "接收人"]])
            elif df.loc[i, "发送方式"] == "邮件" and df.loc[i, "发送类型"] == "表格" and df.loc[i, "数据库"].upper() == "ORACLE":
                temp = oracle_monitor.get_html(df.loc[i, "主题"], df.loc[i, "SQL路径"])
                if temp is not None:
                    mail_contents.append(temp)
                    if len(mail_to_account) == 0:
                        mail_to_account.append(df.loc[i, "接收人"])
            elif df.loc[i, "发送类型"] == "图片":
                temp = pandas_plot.get_html(df.loc[i, "主题"], df.loc[i, "SQL路径"], \
                                            df.loc[i, "索引字段"], df.loc[i, "数据库"])
                if temp is not None:
                    mail_contents.append(temp)


if __name__ == "__main__":
    mail_contents = []
    wx_contents = []
    mail_to_account = []
    content1 = getRow.getHtml(sql1, 'APP数仓模块运行日志', 0)
    mail_contents.append(content1)
    content2 = getRow.getHtml(sql2, 'APP数仓模块错误日志', 1)
    mail_contents.append(content2)
    get_content()

    # 发送邮件
    if len(mail_contents) > 0:
        sendMail.send("APP数仓监控", ''.join(mail_contents), 'html', str(mail_to_account[0]))
    # 发送微信消息
    for i in wx_contents:
        sendWX.send_wx(i[0], 'text', str(i[1]))

    # 改为从配置文件获取发送相关信息
    # # content3 = getRow.getError(sql3)
    #
    # content4 = mysql_monitor.get_text("异常单据", ".\sql\异常单据监控.sql")
    # content5 = oracle_monitor.get_html("流量日志监控(红色仅表示可疑数据，不一定是错误!)", ".\sql\流量日志监控.sql")
    # content6 = oracle_monitor.get_text("流量日志异常", ".\sql\流量日志异常数据.sql")
    # content7 = pandas_plot.get_html("流量及销售趋势图", ".\sql\流量及销售趋势.sql", "DT", "ORACLE")
    # if content1 is not None or content2 is not None or content5 is not None or content7 is not None:
    #     content = content1 + content2 + content5 + content7
    #     sendMail.send("APP数仓监控", content, 'html')
    # if content4 is not None:
    #     sendWX.send_wx(content4, 'text')
    # if content6 is not None:
    #     sendWX.send_wx(content6, 'text')
