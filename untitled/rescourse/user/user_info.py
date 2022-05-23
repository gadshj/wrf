# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: user_info.py
@time: 2022/5/20 15:54
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from flask_restful import Resource
from flask import jsonify


class UserInfo(Resource):
    def get(self):
        return jsonify({'code': 1, 'msg': '11'})
