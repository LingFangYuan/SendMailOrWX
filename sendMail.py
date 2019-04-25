import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import sys

SMTP_host = "IP:PORT"
from_account = "******@***.com"
from_passwd = "*****"

to_account1 = "********@****.com,*********@*****.com"




def send_email(SMTP_host, from_account, from_passwd, to_account, subject, content, mail_type):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, mail_type, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account.replace(' ', '').split(","), msg.as_string())

    email_client.quit()


def send(subject, content, mail_type, to_account="nan"):
    try:
        if to_account == "nan":
            to_account = to_account1
        send_email(SMTP_host, from_account, from_passwd,
                   to_account, subject, content, mail_type)
    except:
        try:
            exType, exValue, exTrace = sys.exc_info()
            nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file = open(".\log\log.txt", 'a', encoding="utf-8")
            file.write("时间：" + str(nowdate) + "   错误：" + str(exValue) + "\n")
        finally:
            file.close()
