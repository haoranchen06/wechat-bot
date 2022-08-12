# -*- coding: utf-8 -*-

import requests
from functools import lru_cache
from time import time, asctime, strftime, strptime, sleep
import datetime
import json
import copy
import urllib
# import urllib3
import hashlib
import schedule


wechat_default_blue = "#173177"
white = "#FFFFFF"
black = "#000000"
red = "#FF4500"
dark_red = "#B22222"
light_red = "#FA8072"
pink = "#FFC0CB"
purple = "#A020F0"
blue = "#4169E1"
dark_blue = "#082E54"
yellow = "#FFFF00"
rose = "#FF3300"
orange = "#FF6100"
green = "#00FF00"
dark_green = "#228B22"


good_morning_template = \
    """
    {{date.DATA}}
    
    保安陈和倩公主在一起的第{{together_days.DATA}}天
    
    距离倩公主生日还有{{princess_next_birthday.DATA}}天
    
    杭州今天白天{{hz_day_ww.DATA}}，晚上{{hz_night_ww.DATA}}，最高{{hz_high_temp.DATA}}度，最低{{hz_low_temp.DATA}}度
    
    天长今天白天{{tc_day_ww.DATA}}，晚上{{tc_night_ww.DATA}}，最高{{tc_high_temp.DATA}}度，最低{{tc_low_temp.DATA}}度
    
    油王情话：{{love_declaration.DATA}}
    """

good_night_template = \
    """
    {{date.DATA}}
    
    杭州明天白天{{hz_day_ww.DATA}}，晚上{{hz_night_ww.DATA}}，最高{{hz_high_temp.DATA}}度，最低{{hz_low_temp.DATA}}度

    天长明天白天{{tc_day_ww.DATA}}，晚上{{tc_night_ww.DATA}}，最高{{tc_high_temp.DATA}}度，最低{{tc_low_temp.DATA}}度

    保安鸡汤：{{everyday_quote.DATA}}
    """


class MTSDataElement(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color


class GoodMorningTemplateData(object):
    def __init__(self, date, together_days, hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp,
                 tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp, love_declaration):
        self.date = date
        self.together_days = together_days
        self.hz_day_ww = hz_day_ww
        self.hz_night_ww = hz_night_ww
        self.hz_high_temp = hz_high_temp
        self.hz_low_temp = hz_low_temp
        self.tc_day_ww = tc_day_ww
        self.tc_night_ww = tc_night_ww
        self.tc_high_temp = tc_high_temp
        self.tc_low_temp = tc_low_temp
        self.love_declaration = love_declaration


class GoodNightTemplateData(object):
    def __init__(self, date, hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp,
                 tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp, everyday_quote):
        self.date = date
        self.hz_day_ww = hz_day_ww
        self.hz_night_ww = hz_night_ww
        self.hz_high_temp = hz_high_temp
        self.hz_low_temp = hz_low_temp
        self.tc_day_ww = tc_day_ww
        self.tc_night_ww = tc_night_ww
        self.tc_high_temp = tc_high_temp
        self.tc_low_temp = tc_low_temp
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


class TianAPI(object):
    def __init__(self):
        self.APIKEY = "1fc2c216b359acde5d77390874bc21bc"

    def caihongpi_index(self):
        url = f"http://api.tianapi.com/caihongpi/index?key={self.APIKEY}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        rsp = requests.get(url, headers=headers)
        raw_text = json.loads(rsp.text)
        return raw_text

    def everyday_index(self):
        url = f"http://api.tianapi.com/everyday/index?key={self.APIKEY}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        rsp = requests.get(url, headers=headers)
        raw_text = json.loads(rsp.text)
        return raw_text


class WechatApi(object):
    def __init__(self):
        self.app_id = "wxb9ee3f7deaaf1370"
        self.app_secret = "fc7584d7ce6bdc98c4a9df7506abdfef"
        self.princess_open_id = "oiF8y5_yg3E5VHqv9wZpfUgWVZ3w"
        self.guard_open_id = "oiF8y56RQyVg_ohketDv0wyKd7YA"
        self.good_morning_tpl_id = "lkef1PfVikUcODKmpOR-UXzlyLIUSYe8-kOlrnAM0o0"
        self.good_night_tpl_id = "zCMzTf4IpGqsct68DgPPrxreNfA5Rt_dgMt9caI7xAs"

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
        self.tian_api = TianAPI()
        self.wechat_api = WechatApi()
        self.together_date = datetime.date(2022, 3, 4)
        self.hz_district_id = 330100
        self.tc_district_id = 341181

    @property
    def cur_date(self):
        year = int(strftime("%Y"))
        month = int(strftime("%m"))
        day = int(strftime("%d"))
        cur_date = datetime.date(year, month, day)
        return cur_date

    @property
    def together_days(self):
        residual = self.cur_date - self.together_date
        return residual.days + 1

    def temp2color(self):
        raise NotImplementedError

    def ww2color(self):
        raise NotImplementedError

    def daily_en_words(self):
        raise NotImplementedError

    def brain_twists(self):
        raise NotImplementedError

    def get_weather(self, district_id=341181, data_type="all", next_days=0):
        raw_text = self.baidu_api.weather_v1(district_id=district_id, data_type=data_type)
        day_ww = raw_text["result"]["forecasts"][next_days]["text_day"]
        night_ww = raw_text["result"]["forecasts"][next_days]["text_night"]
        high_temp = raw_text["result"]["forecasts"][next_days]["high"]
        low_temp = raw_text["result"]["forecasts"][next_days]["low"]
        return day_ww, night_ww, high_temp, low_temp

    def get_struct_weather(self, district_id=341181, data_type="all", next_days=0):
        day_ww, night_ww, high_temp, low_temp = self.get_weather(district_id, data_type, next_days)
        day_ww = MTSDataElement(value=day_ww, color=light_red)
        night_ww = MTSDataElement(value=night_ww, color=light_red)
        high_temp = MTSDataElement(value=high_temp, color=light_red)
        low_temp = MTSDataElement(value=low_temp, color=light_red)
        return day_ww, night_ww, high_temp, low_temp

    def get_struct_love_declaration(self):
        raw_text = self.tian_api.caihongpi_index()
        love_declaration = MTSDataElement(
            value=raw_text["newslist"][0]["content"],
            color=light_red,
        )
        return love_declaration

    def get_struct_everyday_quote(self):
        raw_text = self.tian_api.everyday_index()
        content = raw_text["newslist"][0]["content"]
        note = raw_text["newslist"][0]["note"]
        everyday_quote = MTSDataElement(
            value=f"{content}\n{note}",
            color=light_red,
        )
        return everyday_quote

    def good_morning(self):
        template_id = self.wechat_api.good_morning_tpl_id
        date = MTSDataElement(value=strftime("%Y-%m-%d %A %H:%M"), color=light_red)
        together_days = MTSDataElement(value=self.together_days, color=light_red)
        hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp = self.get_struct_weather(
            district_id=self.hz_district_id,
            next_days=0
        )
        tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp = self.get_struct_weather(
            district_id=self.tc_district_id,
            next_days=0
        )
        love_declaration = self.get_struct_love_declaration()
        struct_data = GoodMorningTemplateData(
            date=date,
            together_days=together_days,
            hz_day_ww=hz_day_ww,
            hz_night_ww=hz_night_ww,
            hz_high_temp=hz_high_temp,
            hz_low_temp=hz_low_temp,
            tc_day_ww=tc_day_ww,
            tc_night_ww=tc_night_ww,
            tc_high_temp=tc_high_temp,
            tc_low_temp=tc_low_temp,
            love_declaration=love_declaration,
        )
        data = obj2dict(struct_data)
        self.wechat_api.message_template_send(touser=self.wechat_api.princess_open_id,
                                              template_id=template_id, data=data)
        self.wechat_api.message_template_send(touser=self.wechat_api.guard_open_id,
                                              template_id=template_id, data=data)

    def good_night(self):
        template_id = self.wechat_api.good_night_tpl_id
        date = MTSDataElement(value=strftime("%Y-%m-%d %A %H:%M"), color=light_red)
        hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp = self.get_struct_weather(
            district_id=self.hz_district_id,
            next_days=1
        )
        tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp = self.get_struct_weather(
            district_id=self.tc_district_id,
            next_days=1
        )
        everyday_quote = self.get_struct_everyday_quote()
        struct_data = GoodNightTemplateData(
            date=date,
            hz_day_ww=hz_day_ww,
            hz_night_ww=hz_night_ww,
            hz_high_temp=hz_high_temp,
            hz_low_temp=hz_low_temp,
            tc_day_ww=tc_day_ww,
            tc_night_ww=tc_night_ww,
            tc_high_temp=tc_high_temp,
            tc_low_temp=tc_low_temp,
            everyday_quote=everyday_quote,
        )
        data = obj2dict(struct_data)
        self.wechat_api.message_template_send(touser=self.wechat_api.princess_open_id,
                                              template_id=template_id, data=data)
        self.wechat_api.message_template_send(touser=self.wechat_api.guard_open_id,
                                              template_id=template_id, data=data)


if __name__ == "__main__":
    # wechat_api = WechatApi()
    # access_token = wechat_api.access_token

    # baidu_api = BaiduApi()
    # tc_w = baidu_api.weather_v1(district_id=341181, data_type="all")
    #
    # tian_api = TianAPI()
    # chp = tian_api.caihongpi_index()
    # ei = tian_api.everyday_index()

    serve_princess = ServePrincess()
    # serve_princess.good_morning()
    # serve_princess.good_night()

    schedule.every().day.at("06:45").do(serve_princess.good_morning)
    schedule.every().day.at("22:30").do(serve_princess.good_night)

    while True:
        schedule.run_pending()
        sleep(1)




