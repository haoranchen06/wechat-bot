# -*- coding: utf-8 -*-

import requests
from functools import lru_cache
from time import time, asctime
import json


class WechatApi(object):
    
    def __init__(self):
        self.app_id = "wxb9ee3f7deaaf1370"
        self.app_secret = "fc7584d7ce6bdc98c4a9df7506abdfef"
    
    @property
    def access_token(self):
        ts_token = time() // (2*60*60)
        return self.get_access_token(ts_token=ts_token)
    
    @lru_cache(maxsize=4)
    def get_access_token(self, ts_token):
        url = "https://api.weixin.qq.com/cgi-bin/token?"
        grant_type = "client_credential"
        appid=self.app_id
        secret=self.app_secret
        params = f"grant_type={grant_type}&appid={appid}&secret={secret}"
        url += params
        rsp = requests.get(url=url)
        access_token = json.loads(rsp.text)["access_token"]
        return access_token
    
    def message_mass_sendall(self):
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={self.access_token}"
        payloads = {"filter": {"is_to_all": True},
                    "msgtype": "text",
                    "text": {"content": "hello from boxer."}}
        data = json.dumps(payloads)
        rsp = requests.post(url=url, data=data)
        raw_text = json.loads(rsp.text)
        return raw_text
    
    def message_mass_send(self):
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={self.access_token}"
        touser = [
            "oiF8y56RQyVg_ohketDv0wyKd7YA",
            "oiF8y5_yg3E5VHqv9wZpfUgWVZ3w",
            ]
        content = f"今天日期是{asctime()}\n我的臭宝宝"
        payloads = dict(
            touser=touser,
            msgtype="text",
            text=dict(content=content),
            )
        # data = json.dumps(payloads, ensure_ascii=False)
        rsp = requests.post(url=url, json=payloads)
        # rsp = requests.request(method="POST", url=url, data=data)
        raw_text = json.loads(rsp.text)
        return raw_text
    
    def message_template_send(self):
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.access_token}"
        touser = "oiF8y5_yg3E5VHqv9wZpfUgWVZ3w"
        template_id = "v1x6EEEepVOip1So8fItcrT9E4k2XSe8_II7jLnjHsI"
        data = {
            "date": {
                "value": asctime(),
                "color": "#173177"
            },
            "weather": {
                "value": "sunny",
                "color": "#173177"
            },
            "together_days": {
                "value": 158,
                "color": "#173177"
            },
            "everyday_quote": {
                "value": "good good study, day day up",
                "color": "#173177"
            },
        }
        payloads = dict(touser=touser, template_id=template_id, data=data)
        rsp = requests.post(url=url, json=payloads)
        raw_text = json.loads(rsp.text)
        return raw_text


if __name__ == "__main__":
    wechat_api = WechatApi()
    # access_token = wechat_api.access_token
    # sendall_res = wechat_api.massage_mass_sendall()
    # mms_res = wechat_api.message_mass_send()
    mts_res = wechat_api.message_template_send()
    