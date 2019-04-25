import json
import sendMail
import requests

v_corpid = "******"
v_secret = "***************"


class WeChatPub:
    s = requests.session()
    token = None

    def __init__(self):
        self.token = self.get_token(v_corpid, v_secret)
        # print("token is " + self.token)

    def get_token(self, corpid, secret):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corpid, secret)
        rep = self.s.get(url)
        if rep.status_code == 200:
            return json.loads(rep.content)['access_token']
        else:
            print("request failed.")
            return None

    def send_msg_textcard(self, content, cradurl, to_account):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": to_account,
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002,
            "textcard": {
                "title": "APP商城数仓异常通知",
                "description": content,
                "url": cradurl,
                "btntxt": "详情"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            return json.loads(rep.content)
        else:
            print("request failed.")
            return None

    def send_msg_text(self, content, to_account):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": to_account,
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": content
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            return json.loads(rep.content)
        else:
            print("request failed.")
            return None


def send_wx(content, type, to_account):
    try:
        if to_account == "nan":
            to_account = "@all"
        to_account = to_account.replace(' ', '').replace(',', '|')
        wechat = WeChatPub()
        if type == "textcard":
            wechat.send_msg_textcard(content, "https://mail.qq.com/cgi-bin/loginpage", to_account)
        elif type == "text":
            wechat.send_msg_text(content, to_account)
    except Exception as e:
        sendMail.send("APP数仓监控程序出错", str(e), 'plain')
