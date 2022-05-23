# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: database.py
@time: 2022/5/20 16:00
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/1908a')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
