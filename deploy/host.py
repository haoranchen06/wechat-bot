#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/9/14 19:25
# @Author: chenhr33733
# @File: host.py
# @Software: PyCharm
# @Copyright：Copyright(c) 2022 Hundsun.com, Inc.All Rights Reserved


import flask
from flask import Flask
from flask_cors import CORS


app = Flask('guard_host')
CORS(app, supports_credentials=True)
app.secret_key = 'chenhr33733'


@app.route("/get", methods=["GET"])
def get():
    args = flask.request.args
    form = flask.request.form
    headers = flask.request.headers
    json_data = flask.request.json
    print(args, form, headers, json_data)
    return "OK"


if __name__ == "__main__":
    app_host = '0.0.0.0'
    app_port = '7353'
    app.run(host=app_host, port=app_port, threaded=False)
    # server = pywsgi.WSGIServer((app_host, app_port), app)
    # server.start()


