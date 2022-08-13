#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/8/13 13:40
# @Author: chenhr33733
# @File: constants.py
# @Software: PyCharm
# @Copyright：Copyright(c) 2021 Hundsun.com,Inc.All Rights Reserved


import configparser


cp = configparser.ConfigParser()
cp.read("config.ini")

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


