# -*- coding: utf-8 -*-

import requests
from functools import lru_cache
from time import time, strftime
import datetime
import json
import copy
import urllib
# import urllib3
import hashlib
from configs.constants import *
import re


good_morning_template = \
    """
    {{date.DATA}}
    
    保安陈和倩公主在一起的第{{together_days.DATA}}天
    
    距离倩公主生日还有{{princess_next_birthday.DATA}}天
    
    杭州今天白天{{hz_day_ww.DATA}}，晚上{{hz_night_ww.DATA}}，最高{{hz_high_temp.DATA}}度，最低{{hz_low_temp.DATA}}度
    
    天长今天白天{{tc_day_ww.DATA}}，晚上{{tc_night_ww.DATA}}，最高{{tc_high_temp.DATA}}度，最低{{tc_low_temp.DATA}}度
    
    脑筋急转弯：{{brain_twists.DATA}}
    
    油王情话：{{love_declaration.DATA}}
    """

good_night_template = \
    """
    {{date.DATA}}
    
    杭州明天白天{{hz_day_ww.DATA}}，晚上{{hz_night_ww.DATA}}，最高{{hz_high_temp.DATA}}度，最低{{hz_low_temp.DATA}}度
    
    天长明天白天{{tc_day_ww.DATA}}，晚上{{tc_night_ww.DATA}}，最高{{tc_high_temp.DATA}}度，最低{{tc_low_temp.DATA}}度
    
    脑筋急转弯答案：{{brain_twists_answer.DATA}}
    
    保安鸡汤：{{everyday_quote.DATA}}
    """


class MTSDataElement(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color


class GoodMorningTemplateData(object):
    def __init__(self, date, together_days, princess_next_birthday, hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp,
                 tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp, brain_twists, love_declaration):
        self.date = date
        self.together_days = together_days
        self.princess_next_birthday = princess_next_birthday
        self.hz_day_ww = hz_day_ww
        self.hz_night_ww = hz_night_ww
        self.hz_high_temp = hz_high_temp
        self.hz_low_temp = hz_low_temp
        self.tc_day_ww = tc_day_ww
        self.tc_night_ww = tc_night_ww
        self.tc_high_temp = tc_high_temp
        self.tc_low_temp = tc_low_temp
        self.brain_twists = brain_twists
        self.love_declaration = love_declaration


class GoodNightTemplateData(object):
    def __init__(self, date, hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp,
                 tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp, brain_twists_answer, everyday_quote):
        self.date = date
        self.hz_day_ww = hz_day_ww
        self.hz_night_ww = hz_night_ww
        self.hz_high_temp = hz_high_temp
        self.hz_low_temp = hz_low_temp
        self.tc_day_ww = tc_day_ww
        self.tc_night_ww = tc_night_ww
        self.tc_high_temp = tc_high_temp
        self.tc_low_temp = tc_low_temp
        self.brain_twists_answer = brain_twists_answer
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


class AttrDictPlus(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDictPlus, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def _set_attr(self, keys, value):
        keys = keys.split('.')
        if len(keys) == 1:
            self.__setattr__(keys[0], value)
        else:
            self.__setattr__(keys[0], AttrDictPlus())
            next_ = self.__getattribute__(keys[0])
            assert isinstance(next_, AttrDictPlus)
            next_._set_attr('.'.join(keys[1:]), value)

    def _get_attr(self, keys):
        keys = keys.split('.')
        if len(keys) == 1:
            return self.__getattribute__(keys[0])
        else:
            next_ = self.__getattribute__(keys[0])
            assert isinstance(next_, AttrDictPlus)
            return next_._get_attr('.'.join(keys[1:]))


def _en_learn_html(func):

    def wrapper(*args, **kwargs):
        word, phone_t, trans_t, ex_t = func(*args, **kwargs)
        word = f"""<p style="font-size: 30px"><strong>{word}</strong></p>"""
        phone = "<span> </span>\n".join(f"<span>{l}</span>\n<span>{p}</span>\n" for l, p in zip(["英", "美"], phone_t[:2]))
        explain = "\n".join(f"<p>{' '.join(pair)}</p>" for pair in trans_t)
        example = "\n".join(f"<p>{' '.join(pair)}</p>" for pair in ex_t)
        return word, phone, explain, example

    return wrapper


@_en_learn_html
def youdao_en2cn(word):
    url = f"https://www.youdao.com/result?word={word}&lang=en"
    data = requests.get(url).text
    pos_pattern = r"<span class=\"pos\".*?>(.*?)</span>"
    phone_pattern = r"<span class=\"phonetic\".*?>(.*?)</span>"
    trans_pattern = r"<span class=\"trans\".*?>(.*?)</span>"
    en_ex_pattern = r"<div class=\"sen-eng\".*?>(.*?)</div>"
    cn_ex_pattern = r"<div class=\"sen-ch\".*?>(.*?)</div>"
    pos = re.findall(pattern=pos_pattern, string=data)
    phone = re.findall(pattern=phone_pattern, string=data)
    trans = re.findall(pattern=trans_pattern, string=data)
    en_ex = re.findall(pattern=en_ex_pattern, string=data)
    cn_ex = re.findall(pattern=cn_ex_pattern, string=data)
    phone_t = phone
    trans_t = []
    for p, t in zip(pos, trans[:len(pos)]):
        pair = (p, t)
        trans_t.append(pair)
    ex_t = []
    for en, cn in zip(en_ex, cn_ex):
        pair = (en, cn)
        ex_t.append(pair)
    return word, phone_t, trans_t, ex_t


class BaiduApi(object):
    def __init__(self):
        self.ak = bd_ak
        self.sk = bd_sk
        self.prefix = bd_prefix
        self.host = bd_host

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
        self.APIKEY = tian_APIKEY

    def caihongpi_index(self):
        url = f"http://api.tianapi.com/caihongpi/index"
        return self._get(url=url)

    def everyday_index(self):
        url = f"http://api.tianapi.com/everyday/index"
        return self._get(url=url)

    def naowan_index(self):
        url = f"http://api.tianapi.com/naowan/index"
        return self._get(url=url, num=1)

    def enwords_index(self, word):
        url = f"http://api.tianapi.com/enwords/index"
        return self._get(url=url, word=word)

    def jiejiari_index(self, date):
        url = f"http://api.tianapi.com/jiejiari/index"
        return self._get(url=url, date=date)

    def robot_index(self, question):
        url = f"http://api.tianapi.com/robot/index"
        return self._get(url=url, question=question)

    def _get(self, url, **kwargs):
        url = f"{url}?key={self.APIKEY}" + "".join(f"&{k}={v}" for k, v in kwargs.items())
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        rsp = requests.get(url, headers=headers)
        raw_text = json.loads(rsp.text)
        return raw_text


class WechatApi(object):
    def __init__(self):
        self.app_id = wc_app_id
        self.app_secret = wc_app_secret
        self.princess_open_id = wc_princess_open_id
        self.guard_open_id = wc_guard_open_id
        self.good_morning_tpl_id = wc_good_morning_tpl_id
        self.good_night_tpl_id = wc_good_night_tpl_id
        self.daily_en_words_tpl_id = wc_daily_en_words_tpl_id

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

    def media_upload(self, file_path, file_cate="image/jpeg", file_type="image"):
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={file_type}"
        files = [
            ('media', (file_path, open(file_path, 'rb'), file_cate))
        ]
        rsp = requests.post(url=url, files=files)
        raw_text = json.loads(rsp.text)
        return raw_text

    def media_upload_news(self, **kwargs):
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token={self.access_token}"
        payloads = kwargs
        rsp = requests.post(url=url, data=bytes(json.dumps(payloads, ensure_ascii=False), encoding="utf-8"))
        raw_text = json.loads(rsp.text)
        return raw_text
    
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
        self.princess_birthday = datetime.date(1998, 3, 21)
        self.hz_district_id = 330100
        self.tc_district_id = 341181
        self.bt_q = serve_bt_q
        self.bt_a = serve_bt_a

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

    @property
    def princess_next_birthday(self):
        m = self.princess_birthday.month
        d = self.princess_birthday.day
        annual_date = datetime.date(int(strftime("%Y")), m, d)
        residual = annual_date - self.cur_date
        if residual.days < 0:
            annual_date = datetime.date(int(strftime("%Y"))+1, m, d)
            residual = annual_date - self.cur_date
        return residual.days

    def temp2color(self, temp):
        temp = max(min(temp, 40), 0)
        red_weight = temp / 40
        green_weight = 1 - abs(temp-20) / 20
        blue_weight = 1 - red_weight
        rgb = (255 * red_weight, 255 * green_weight, 255 * blue_weight)
        color = self.rgb2hex(rgb)
        return color

    @staticmethod
    def rgb2hex(rgb):
        color = '#'
        for i in rgb:
            num = int(i)
            color += str(hex(num))[-2:].replace('x', '0').upper()
        return color

    @staticmethod
    def ww2color(ww):
        mappings = {
            "晴": orange_red,
            "云": dark_grey,
            "阴": dark_grey,
            "雨": blue,
            "雪": light_blue,
            "冰": light_blue,
            "雾": dark_grey,
            "霜": light_blue,
            "": wechat_default_blue,
        }
        for key, color in mappings.items():
            if key in ww:
                return color

    def daily_en_words(self):
        """
        TODO: 更优雅地使用html模板
        """
        cet6_en_vocab = open("daily_en/cet6_en_vocab.txt", "r").read().split('\n')
        en_idx = int(open("daily_en/en_idx.txt", "r").read())
        trans_list = []
        cnt = 0
        try_times = 0
        max_try_times = 100
        while cnt < 5 and try_times < max_try_times:
            try:
                w = cet6_en_vocab[en_idx+try_times]
                cur_trans = youdao_en2cn(word=w)
                trans_list.append(cur_trans)
                cnt += 1
            except Exception:
                pass
            finally:
                try_times += 1
        mu_rsp = self.wechat_api.media_upload(file_path="daily_en/en_pic_1.jpeg", file_type="image")
        with open("daily_en/en_learn_template.html", "r") as r:
            en_learn_template = r.read()
        full_body = ""
        single_tpl = re.search(pattern=r"<body>([\s\S]*)</body>", string=en_learn_template).group(1)
        for word, phone, explain, example in trans_list:
            full_body += single_tpl.format(word=word, phone=phone, explain=explain, example=example)
        full_body = f"<body>\n{full_body}\n</body>"
        en_learn_today = re.sub(pattern=r"<body>[\s\S]*</body>", repl=full_body, string=en_learn_template)
        # print(en_learn_today)
        atc = dict(
            thumb_media_id=mu_rsp["media_id"],
            author="保安陈",
            title="每日单词",
            content=en_learn_today,
            digest="CET-6",
            show_cover_pic=0,
            need_open_comment=1,
            only_fans_can_comment=0
        )
        cur_article = dict(articles=[atc])
        mun_rsp = self.wechat_api.media_upload_news(**cur_article)
        payloads = dict(
            touser=[
                self.wechat_api.guard_open_id,
                self.wechat_api.princess_open_id,
                # "xxx",
            ],
            msgtype="mpnews",
            mpnews=dict(media_id=mun_rsp["media_id"])
        )
        cur_rsp = self.wechat_api.message_mass_send(**payloads)
        print(cur_rsp)
        with open("daily_en/en_idx.txt", "w") as w:
            w.write(str(en_idx+try_times))

    def brain_twists_qa_pair(self):
        raw_text = self.tian_api.naowan_index()
        q = raw_text['newslist'][0]['quest']
        a = raw_text['newslist'][0]['result']
        self.bt_q = q
        self.bt_a = a

    def get_weather(self, district_id=341181, data_type="all", next_days=0):
        raw_text = self.baidu_api.weather_v1(district_id=district_id, data_type=data_type)
        day_ww = raw_text["result"]["forecasts"][next_days]["text_day"]
        night_ww = raw_text["result"]["forecasts"][next_days]["text_night"]
        high_temp = raw_text["result"]["forecasts"][next_days]["high"]
        low_temp = raw_text["result"]["forecasts"][next_days]["low"]
        return day_ww, night_ww, high_temp, low_temp

    def get_struct_date(self):
        value = strftime("%Y-%m-%d")
        raw_text = self.tian_api.jiejiari_index(date=value)
        today_info = raw_text["newslist"][0]
        value += f" {today_info['cnweekday']}"
        if today_info["info"] == "双休日":
            value += f"\n周末快乐呀"
        elif today_info["info"] == "节假日":
            value += f"\n{today_info['name']}假期快乐呀"
        ans = MTSDataElement(value=value, color=light_red)
        return ans

    def get_struct_weather(self, district_id=341181, data_type="all", next_days=0):
        day_ww, night_ww, high_temp, low_temp = self.get_weather(district_id, data_type, next_days)
        day_ww = MTSDataElement(value=day_ww, color=self.ww2color(day_ww))
        night_ww = MTSDataElement(value=night_ww, color=self.ww2color(night_ww))
        high_temp = MTSDataElement(value=high_temp, color=self.temp2color(high_temp))
        low_temp = MTSDataElement(value=low_temp, color=self.temp2color(low_temp))
        return day_ww, night_ww, high_temp, low_temp

    def get_struct_love_declaration(self):
        raw_text = self.tian_api.caihongpi_index()
        raw_text = raw_text["newslist"][0]["content"]
        pattern = r"([Xx]{2,})|(你)"
        ld = re.sub(pattern=pattern, repl=princess_nick_name, string=raw_text)
        love_declaration = MTSDataElement(
            value=ld,
            color=orange_yellow,
        )
        return love_declaration

    def get_struct_everyday_quote(self):
        raw_text = self.tian_api.everyday_index()
        content = raw_text["newslist"][0]["content"]
        note = raw_text["newslist"][0]["note"]
        everyday_quote = MTSDataElement(
            value=f"{content}\n{note}",
            color=orange_yellow,
        )
        return everyday_quote

    def good_morning(self):
        template_id = self.wechat_api.good_morning_tpl_id
        date = self.get_struct_date()
        together_days = MTSDataElement(value=self.together_days, color=pink)
        princess_next_birthday = MTSDataElement(value=self.princess_next_birthday, color=pink)
        hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp = self.get_struct_weather(
            district_id=self.hz_district_id,
            next_days=0
        )
        tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp = self.get_struct_weather(
            district_id=self.tc_district_id,
            next_days=0
        )
        self.brain_twists_qa_pair()
        brain_twists = MTSDataElement(value=self.bt_q, color=orange)
        love_declaration = self.get_struct_love_declaration()
        struct_data = GoodMorningTemplateData(
            date=date,
            together_days=together_days,
            princess_next_birthday=princess_next_birthday,
            hz_day_ww=hz_day_ww,
            hz_night_ww=hz_night_ww,
            hz_high_temp=hz_high_temp,
            hz_low_temp=hz_low_temp,
            tc_day_ww=tc_day_ww,
            tc_night_ww=tc_night_ww,
            tc_high_temp=tc_high_temp,
            tc_low_temp=tc_low_temp,
            brain_twists=brain_twists,
            love_declaration=love_declaration,
        )
        data = obj2dict(struct_data)
        self.wechat_api.message_template_send(touser=self.wechat_api.princess_open_id,
                                              template_id=template_id, data=data)
        self.wechat_api.message_template_send(touser=self.wechat_api.guard_open_id,
                                              template_id=template_id, data=data)

    def good_night(self):
        template_id = self.wechat_api.good_night_tpl_id
        date = MTSDataElement(value=strftime("%Y-%m-%d %A"), color=light_red)
        hz_day_ww, hz_night_ww, hz_high_temp, hz_low_temp = self.get_struct_weather(
            district_id=self.hz_district_id,
            next_days=1
        )
        tc_day_ww, tc_night_ww, tc_high_temp, tc_low_temp = self.get_struct_weather(
            district_id=self.tc_district_id,
            next_days=1
        )
        brain_twists_answer = MTSDataElement(value=self.bt_a, color=orange)
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
            brain_twists_answer=brain_twists_answer,
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

    tian_api = TianAPI()
    chp = tian_api.caihongpi_index()
    ei = tian_api.everyday_index()
    nw = tian_api.naowan_index()
    jjr = tian_api.jiejiari_index(date="2022-9-13")
    ri = tian_api.robot_index(question="今天天气如何")

    a = youdao_en2cn("plan")

    # serve_princess = ServePrincess()
    # serve_princess.good_morning()
    # serve_princess.good_night()
    # serve_princess.daily_en_words()


