# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: tasks.py
@time: 2022/5/23 15:19
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""
import json
from ronglian_sms_sdk import SmsSDK
from celery_tasks.main import celery_app

accId = '8a216da8802d68fe01804498b48e04a9'
accToken = 'c2ea85311edd470ca6737850b76e9640'
appId = '8a216da8802d68fe01804498b5a804b0'


@celery_app.task(name='send_message')
def send_message(mobile, code, exc_time):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    datas = (code, exc_time)
    resp = sdk.sendMessage(tid, mobile, datas)
    resp_info = json.load(resp).get('statusCode')
    return True if resp_info == '000000' else False
