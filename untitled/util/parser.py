# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: parser.py
@time: 2022/5/23 15:41
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

import re

def mobile(mobile_str):
    if re.match(r'^1[3-9]\d{9}$',mobile_str):
        return mobile_str
    else:
        raise ValueError(f'{mobile_str} mobile is not valid')


def code(code_str):
    if re.match(r'^\d{6}$',code_str):
        return code_str
    else:
        raise ValueError(f'{code_str} code is not valid')