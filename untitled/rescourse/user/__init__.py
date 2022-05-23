# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: __init__.py.py
@time: 2022/5/20 15:40
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from flask import Blueprint

from flask_restful import Api

from . import login, user_info

user_bp = Blueprint("user_bp", __name__, )

user_api = Api(user_bp)

user_api.add_resource(login.LoginView, '/app/v1_0/authorizations')

user_api.add_resource(login.CodeView, '/app/v1_0/sms/codes/<string:mobile>')

