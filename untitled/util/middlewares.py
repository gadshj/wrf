# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: middlewares.py
@time: 2022/5/20 16:00
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from flask import request, current_app, g, abort
from util.jwt_util import verify_jwt


def jwt_authentication():
    if not request.path.startswith('/app/v1_0/sms/codes/') or \
            not request.path.startswith('/app/v1_0/authorizations'):
        token = request.headers.get('Authorization', '')
        if not token:
            abort(403)
        if not token.startswith('Bearer'):
            abort(403)
        token = token.split('Bearer')
        payload = verify_jwt(token=token, secret=current_app.config['JWT_SECRET'])
        if not payload:
            abort(403)
        g.user_id = payload.get('user_id')
