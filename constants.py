#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/8/13 13:40
# @Author: chenhr33733
# @File: constants.py
# @Software: PyCharm
# @Copyright：Copyright(c) 2021 Hundsun.com,Inc.All Rights Reserved


import configparser


wechat_default_blue = "#173177"
white = "#FFFFFF"
black = "#000000"
red = "#FF3300"
dark_red = "#B22222"
light_red = "#FF4500"
pink = "#FF3366"
purple = "#A020F0"
blue = "#0066FF"
light_blue = "#00CCFF"
dark_blue = "#000099"
yellow = "#FFFF66"
orange_yellow = "#FFCC00"
rose = "#FF3300"
orange = "#FF9900"
orange_red = "#FF6600"
green = "#00FF00"
dark_green = "#228B22"
grey = "#D3D3D3"
dark_grey = "#A9A9A9"

cp = configparser.ConfigParser()
cp.read("configs/config.ini")

bd_ak = cp["BAIDU_API"]["ak"]
bd_sk = cp["BAIDU_API"]["sk"]
bd_prefix = cp["BAIDU_API"]["prefix"]
bd_host = cp["BAIDU_API"]["host"]

tian_APIKEY = cp["TIAN_API"]["APIKEY"]

wc_app_id = cp["WECHAT_API"]["app_id"]
wc_app_secret = cp["WECHAT_API"]["app_secret"]
wc_princess_open_id = cp["WECHAT_API"]["princess_open_id"]
wc_guard_open_id = cp["WECHAT_API"]["guard_open_id"]
wc_good_morning_tpl_id = cp["WECHAT_API"]["good_morning_tpl_id"]
wc_good_night_tpl_id = cp["WECHAT_API"]["good_night_tpl_id"]
wc_daily_en_words_tpl_id = cp["WECHAT_API"]["daily_en_words_tpl_id"]


