# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: jwt_util.py
@time: 2022/5/20 16:00
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

import jwt
from datetime import datetime, timedelta


def generate_jwt(payload, expiry, secret=None):
    _payload = {'exp': expiry}

    _payload.update(payload)

    if not secret:
        pass
    token = jwt.encode(payload=_payload, key=secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):
    if not secret:
        pass
    try:
        payload = jwt.decode(token, secret, algorithm='HS256')
    except jwt.PyJWTError:
        payload = None
    return payload


if __name__ == '__main__':
    payload = {
        'user_id': 1,
        'username': 'wrf'
    }
    expiry = datetime.utcnow() + timedelta(hours=1)
    secert = 'TPmiahjsdkasdjkgajsd45asdUUdahdhasdAXA'
    token = generate_jwt(payload, expiry, secret=secert)
    print(token)
