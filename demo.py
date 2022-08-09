# -*- coding: utf-8 -*-

import requests
from functools import lru_cache
from time import time, asctime, strftime, strptime
import json
import copy
import urllib
# import urllib3
import hashlib


class Var(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color


class DataTemplate0(object):
    def __init__(self, date, tianchang_weather, hangzhou_weather, together_days, love_declaration, everyday_quote):
        self.date = date
        self.tianchang_weather = tianchang_weather
        self.hangzhou_weather = hangzhou_weather
        self.together_days = together_days
        self.love_declaration = love_declaration
        self.everyday_quote = everyday_quote


def obj2dict(obj):
    obj = copy.deepcopy(obj)
    if obj is None:
        return None
    elif isinstance(obj, (list, tuple)):
        for index, inner_obj in enumerate(obj):
            obj[index] = obj2dict(inner_obj)
        return obj
    elif isinstance(obj, (str, int, float)):
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = obj2dict(v)
        return obj
    else:
        for k in obj.__dict__.keys():
            attr = obj.__getattribute__(k)
            obj.__setattr__(k, obj2dict(attr))
        return obj.__dict__


class BaiduApi(object):
    def __init__(self):
        self.ak = "PmzkUFQ7R0ru0fcKexpFCbrh8W2HeP4E"
        self.sk = "zLeDXejBo6VAaZYe9yOx1uv0NA4doXu7"
        self.prefix = "https://"
        self.host = "api.map.baidu.com"

    def generate_sn(self, query_str):
        # query_str = '/geocoder/v2/?address=百度大厦&output=json&ak=yourak'
        encoded_str = urllib.parse.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
        raw_str = encoded_str + self.sk
        sn = hashlib.md5(urllib.parse.quote_plus(raw_str).encode("utf-8")).hexdigest()
        return sn

    def weather_v1(self, district_id, data_type):
        address = "/weather/v1"
        query_str = address + f"/?district_id={district_id}&data_type={data_type}&ak={self.ak}"
        sn = self.generate_sn(query_str=query_str)
        final_query = f"{query_str}&sn={sn}"
        url = self.prefix + self.host + final_query
        rsp = requests.get(url=url)
        raw_text = json.loads(rsp.text)
        return raw_text


class WechatApi(object):
    def __init__(self, app_id="wxb9ee3f7deaaf1370", app_secret="fc7584d7ce6bdc98c4a9df7506abdfef"):
        self.app_id = app_id
        self.app_secret = app_secret

    @property
    def princess_open_id(self):
        princess_open_id = "oiF8y5_yg3E5VHqv9wZpfUgWVZ3w"
        return princess_open_id

    @property
    def guard_open_id(self):
        guard_open_id = "oiF8y56RQyVg_ohketDv0wyKd7YA"
        return guard_open_id
    
    @property
    def access_token(self):
        ts_token = time() // (2*60*60)
        return self.get_access_token(ts_token=ts_token)
    
    @lru_cache(maxsize=4)
    def get_access_token(self, ts_token):
        assert ts_token
        url = "https://api.weixin.qq.com/cgi-bin/token?"
        grant_type = "client_credential"
        params = f"grant_type={grant_type}&appid={self.app_id}&secret={self.app_secret}"
        url += params
        rsp = requests.get(url=url)
        access_token = json.loads(rsp.text)["access_token"]
        return access_token
    
    def message_mass_sendall(self, **kwargs):
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={self.access_token}"
        payloads = kwargs
        rsp = requests.post(url=url, json=payloads)
        raw_text = json.loads(rsp.text)
        return raw_text
    
    def message_mass_send(self, **kwargs):
        url = f"https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={self.access_token}"
        payloads = kwargs
        # data = json.dumps(payloads, ensure_ascii=False)
        rsp = requests.post(url=url, json=payloads)
        raw_text = json.loads(rsp.text)
        return raw_text
    
    def message_template_send(self, touser, template_id, data):
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.access_token}"
        payloads = dict(touser=touser, template_id=template_id, data=data)
        rsp = requests.post(url=url, json=payloads)
        raw_text = json.loads(rsp.text)
        return raw_text

    def general_request(self, url, method="POST", **kwargs):
        raise NotImplementedError


class ServePrincess(object):
    def __init__(self):
        self.baidu_api = BaiduApi()
        self.wechat_api = WechatApi()
        self.together_date = "2022-03-04"

    def send_template_0(self):
        touser = self.wechat_api.guard_open_id
        template_id = "BiDrA8aekM8xa_X9fDeeQghGAujdi4heNiO7VYRhhYs"
        date = Var(value=strftime("%Y-%m-%d %A %H:%M"), color="#173177")
        tianchang_weather = baidu_api.weather_v1(district_id=341181, data_type="all")
        tc_w = f"最高温度{tianchang_weather['result']['forecasts'][0]['high']}度，最低温度{tianchang_weather['result']['forecasts'][0]['low']}度"
        hangzhou_weather = baidu_api.weather_v1(district_id=330100, data_type="all")
        hz_w = f"最高温度{hangzhou_weather['result']['forecasts'][0]['high']}度，最低温度{hangzhou_weather['result']['forecasts'][0]['low']}度"
        tianchang_weather = Var(value=tc_w, color="#173177")
        hangzhou_weather = Var(value=hz_w, color="#173177")
        together_days = Var(value=159, color="#173177")
        love_declaration = Var(value="恋爱宣言", color="#173177")
        everyday_quote = Var(value="每日金句", color="#173177")
        data_template_0 = DataTemplate0(
            date=date,
            tianchang_weather=tianchang_weather,
            hangzhou_weather=hangzhou_weather,
            together_days=together_days,
            love_declaration=love_declaration,
            everyday_quote=everyday_quote
        )
        data = obj2dict(data_template_0)
        raw_text = self.wechat_api.message_template_send(touser=touser, template_id=template_id, data=data)
        return raw_text


if __name__ == "__main__":
    wechat_api = WechatApi()
    # access_token = wechat_api.access_token
    # tpl_0_res = wechat_api.send_template_0()

    baidu_api = BaiduApi()
    serve_princess = ServePrincess()
    serve_res = serve_princess.send_template_0()


