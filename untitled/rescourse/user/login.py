# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: login.py
@time: 2022/5/20 15:53
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from util.database import db_session
from celery_tasks.sms.tasks import send_message
from models import User
from flask import request, jsonify, current_app
from datetime import datetime, timedelta
from util.jwt_util import generate_jwt
from redis import Redis
from util import parser


class LoginView(Resource):
    def _generate_token(self, user_id, refresh=False):
        payload = {
            'user_id': user_id,
            'refresh': refresh
        }
        expires = datetime.utcnow() + timedelta(
            hours=current_app.config['JWT_EXPIRY_HOURS'])
        token = generate_jwt(payload, expires)

        if refresh:
            expiry = datetime.utcnow() + timedelta(
                hours=current_app.config['JWT_EXPIRY_DAYS'])
            refresh_token = generate_jwt(payload, expiry)
        else:
            refresh_token = None
        return token, refresh_token

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('mobile', required=True, location='json',
                                 type=parser.mobile)
        json_parser.add_argument('code', required=True, location='json',
                                 type=parser.code)
        args = json_parser.parse_args()
        mobile = args.get('mobile')
        code = args.get('code')
        mobile_code = f'mobile_{mobile}'
        redis_cli = Redis(host='127.0.0.1', port=6379, db=0)
        mobile_code_value = redis_cli.get(mobile_code)
        if not mobile_code_value:
            return {'message': 'code is invalid'}, 400
        if code != mobile_code_value.decode('utf-8') if mobile_code_value else 0:
            return {'message': 'code is invalid'}, 400
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            user = User(mobile=mobile)
            db_session.add(user)
            db_session.commit()
        else:
            if user.status == 0:
                return {'message': 'code is invalid'}, 400
        token, refresh_token = self._generate_token(user.id)
        return {'message': 'ok', 'token': token, 'refresh_token': refresh_token}, 201


class CodeView(Resource):
    def get(self, mobile):
        code = self.my_code()
        exc_time = 5 * 60
        try:
            parser.mobile(mobile_str=mobile)
        except ValueError:
            return {'message': 'mobile is invalid'}, 404

        mobile_code = f'mobile_{mobile}'
        first_code = f'first_{mobile}'
        redis_cli = Redis(host='127.0.0.1', port=6379, db=0)
        first_code_value = redis_cli.get(first_code)
        if first_code_value:
            return {'message': 'cannot be sent frequently'}, 429
        pl = redis_cli.pipeline()
        pl.setex(mobile_code, value=code, time=exc_time)
        pl.setex(first_code, value=1, time=exc_time)
        pl.execute()
        ret = send_message.delay(mobile, code, exc_time)
        if ret:
            return {'message': 'ok', 'mobile': mobile}, 200
        return {'message': 'not ok', 'mobile': mobile}, 429

    @staticmethod
    def my_code():
        import random
        import string
        return ''.join(random.choice(string.digits, k=6))
