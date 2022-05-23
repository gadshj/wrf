# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wangruifeng
@file: models.py
@time: 2022/5/20 15:40
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import relationship
from util.database import Base
from datetime import datetime


class LegalizeLog(Base):
    """
    用户认证申请记录
    """
    __tablename__ = 'user_legalize_log'

    class TYPE:
        REAL_NAME = 1  # 实名认证
        QUALIFICATION = 2  # 资质认证

    class STATUS:
        PROCESSING = 1  # 处理中
        APPROVED = 2 # 通过审核
        REJECT = 3 # 驳回

    id = Column('legalize_id', Integer, primary_key=True, doc='认证申请ID')
    user_id = Column(Integer, ForeignKey('user_basic.user_id'), doc='用户ID')
    user = relationship('User', uselist=False)
    type = Column(Integer, doc='认证类型')
    status = Column(Integer, doc='申请状态')
    reject_reason = Column(String(50), doc='驳回原因')
    qualification_id = Column(Integer, ForeignKey('user_qualification.qualification_id'), doc='资质认证材料ID')
    qualification = relationship('Qualification', uselist=False)
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    utime = Column('update_time', DateTime, default=datetime.now, doc='更新时间')


class Qualification(Base):
    """
    用户资质认证材料
    """
    __tablename__ = 'user_qualification'

    id = Column('qualification_id', Integer, primary_key=True, doc='资质认证材料ID')
    user_id = Column(Integer, doc='用户ID')
    name = Column(String(50), doc='姓名',)
    id_number = Column(String(50), doc='身份证号')
    industry = Column(String(50), doc='行业')
    company = Column(String(50), doc='公司')
    position = Column(String(50), doc='职位')
    add_info = Column(String(50), doc='补充信息')
    id_card_front = Column(String(50), doc='身份证正面')
    id_card_back = Column(String(50), doc='身份证背面')
    id_card_handheld = Column(String(50), doc='手持身份证')
    qualification_img = Column(String(50), doc='证明资料')
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    utime = Column('update_time', DateTime, default=datetime.now, doc='更新时间')


class User(Base):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = Column('user_id', Integer, primary_key=True, doc='用户ID')
    mobile = Column(String(50), doc='手机号')
    password = Column(String(50), doc='密码')
    name = Column('user_name', String(50), doc='昵称')
    profile_photo = Column(String(50), doc='头像')
    last_login = Column(DateTime, doc='最后登录时间')
    is_media = Column(Boolean, default=False, doc='是否是自媒体')
    is_verified = Column(Boolean, default=False, doc='是否实名认证')
    introduction = Column(String(50), doc='简介')
    certificate = Column(String(50), doc='认证')
    article_count = Column(Integer, default=0, doc='发帖数')
    following_count = Column(Integer, default=0, doc='关注的人数')
    fans_count = Column(Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = Column(Integer, default=0, doc='累计点赞人数')
    read_count = Column(Integer, default=0, doc='累计阅读人数')

    account = Column(String(50), doc='账号')
    email = Column(String(50), doc='邮箱')
    status = Column(Integer, default=1, doc='状态，是否可用')

    # 两种方法都可以
    # followings = relationship('Relation', primaryjoin='User.id==Relation.user_id')
    followings = relationship('Relation', foreign_keys='Relation.user_id')


class UserProfile(Base):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = Column('user_id', Integer, primary_key=True, doc='用户ID')
    gender = Column(Integer, default=0, doc='性别')
    birthday = Column(Date, doc='生日')
    real_name = Column(String(50), doc='真实姓名')
    id_number = Column(String(50), doc='身份证号')
    id_card_front = Column(String(50), doc='身份证正面')
    id_card_back = Column(String(50), doc='身份证背面')
    id_card_handheld = Column(String(50), doc='手持身份证')
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    utime = Column('update_time', DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = Column(DateTime, doc='注册自媒体时间')

    area = Column(String(50), doc='地区')
    company = Column(String(50), doc='公司')
    career = Column(String(50), doc='职业')

    followings = relationship('Relation', foreign_keys='Relation.user_id')


class Relation(Base):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = Column('relation_id', Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, ForeignKey('user_basic.user_id'), ForeignKey('user_profile.user_id'), doc='用户ID')
    target_user_id = Column(Integer, ForeignKey('user_basic.user_id'), doc='目标用户ID')
    relation = Column(Integer, doc='关系')
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    utime = Column('update_time', DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class Search(Base):
    """
    用户搜索记录表
    ******************已废弃****************
    """
    __tablename__ = 'user_search'

    id = Column('search_id', Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, doc='用户ID')
    keyword = Column(String(50), doc='关键词')
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    is_deleted = Column(Boolean, default=False, doc='是否删除')
    utime = Column('update_time', DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class Material(Base):
    """
    素材表
    """
    __tablename__ = 'user_material'

    class TYPE:
        IMAGE = 0
        VIDEO = 1
        AUDIO = 2

    class STATUS:
        UNREVIEWED = 0  # 待审核
        APPROVED = 1  # 审核通过
        FAILED = 2  # 审核失败
        DELETED = 3  # 已删除

    id = Column('material_id', Integer, primary_key=True, doc='素材ID')
    user_id = Column(Integer, doc='用户ID')
    type = Column(Integer, default=0, doc='素材类型')
    hash = Column(String(50), doc='素材指纹')
    url = Column(String(50), doc='素材链接地址')
    ctime = Column('create_time', DateTime, default=datetime.now, doc='创建时间')
    status = Column(Integer, default=0, doc='状态')
    reviewer_id = Column(Integer, doc='审核人员ID')
    review_time = Column(DateTime, doc='审核时间')
    is_collected = Column(Boolean, default=False, doc='是否收藏')
    utime = Column('update_time', DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')



