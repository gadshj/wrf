# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: main.py
@time: 2022/5/23 15:19
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from celery import Celery

celery_app = Celery()
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks(['celery_tasks.sms.tasks'])
