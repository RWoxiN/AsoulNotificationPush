# -*- coding: utf-8 -*-
from peewee import *

database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class UpUserModel(BaseModel):
    uid = CharField(max_length=20, unique=True)
    uname = CharField(max_length=50)

    room_id = CharField(max_length=20, unique=True)

    is_live = BooleanField(default=False)
    

class DynamicModel(BaseModel):
    owner = ForeignKeyField(UpUserModel, backref='dynamics')

    # 1: 转发
    # 4: 动态
    # 8: 视频
    type = IntegerField()
    dynamic_id = CharField(max_length=50, unique=True)

    unread = BooleanField(default=True)

db_name = 'asoul.db'
db = SqliteDatabase(db_name)

database_proxy.initialize(db)

database_proxy.create_tables([UpUserModel, DynamicModel])