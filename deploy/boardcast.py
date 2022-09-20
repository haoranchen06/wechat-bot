#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/9/13 14:45
# @Author: chenhr33733
# @File: boardcast.py
# @Software: PyCharm
# @Copyright：Copyright(c) 2022 Hundsun.com, Inc.All Rights Reserved


from core import ServePrincess
import schedule
from time import sleep


if __name__ == "__main__":
    serve_princess = ServePrincess()

    # schedule.every().day.at("06:45").do(serve_princess.good_morning)
    # schedule.every().day.at("08:00").do(serve_princess.daily_en_words)
    # schedule.every().day.at("22:30").do(serve_princess.good_night)
    #
    # while True:
    #     schedule.run_pending()
    #     sleep(1)



