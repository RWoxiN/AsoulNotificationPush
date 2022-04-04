# -*- coding: utf-8 -*-

from .config import *
from .data import * 
from .logger import logging
from .push import wx_push

class anp_api():
    def __init__(self):
        self.members = config.members

    def start(self):
        logging.info("----------Start----------")
        for member in self.members:
            uid = member.get('uid')

            a_data = asoul_data(uid)
            if a_data.fetch_data() is None:
                push_str = 'ERROR\n数据获取出错，请尽快查看日志进行排查。'
                wx_push(push_str)
                continue
            push_data = a_data.get_push_data()

            for push_body in push_data:
                push_str = "{}\n{}\n<a href=\"{}\">{}</a>".format(
                    push_body.get('title'), 
                    push_body.get('data'), 
                    push_body.get('url'),
                    push_body.get('url_data'))
                wx_push(push_str)
        logging.info("-----------End-----------")
