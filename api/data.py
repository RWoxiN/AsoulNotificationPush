# -*- coding: utf-8 -*-
import requests, json
from .logger import logging
from .model import *

class asoul_data():
    url_info = 'https://api.bilibili.com/x/space/acc/info'
    url_dynamic = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'

    def __init__(self, uid):
        self.uid = uid
        self.live_notification = False

    def fetch_data(self):
        if self.fetch_user_info() is None:
            return None
        if self.fetch_space_history() is None:
            return None
        return True

    def fetch_user_info(self):
        url = self.url_info + '?mid=' + self.uid
        r = requests.get(url)
        if r.status_code != 200:
            log_str = 'UID：{}, status_code: {}, content: {}'.format(self.uid, r.status_code, r.content)
            logging.error(log_str)
            return None
        user_info_json = json.loads(r.content)
        user_info_code = user_info_json.get('code')
        user_info_data = user_info_json.get('data')
        
        user_info_mid = user_info_data.get('mid')
        user_info_name = user_info_data.get('name')

        user_info_live_room = user_info_data.get('live_room')
        user_info_live_status = user_info_live_room.get('liveStatus')
        user_info_live_room_id = user_info_live_room.get('roomid')

        upuser = UpUserModel.get_or_create(
            uid=user_info_mid, 
            defaults={
                'uname': user_info_name, 
                'room_id': user_info_live_room_id
            }
        )[0]
        
        if not upuser.is_live:
            if bool(user_info_live_status):
                # 数据库记录上次未开播，实际开播
                self.live_notification = True
                upuser.is_live = True
        else:
            if not bool(user_info_live_status):
                # 数据库记录上次开播，实际未开播
                upuser.is_live = False

        upuser.save()

        self.upuser = upuser

        log_str = 'UID：{}，昵称：{}，{}开播'.format(
            upuser.uid, 
            upuser.uname, 
            '' if upuser.is_live else '未'
        )
        logging.info(log_str)
        return True

    def fetch_space_history(self):
        url = self.url_dynamic + '?host_uid=' + self.uid
        r = requests.get(url)
        if r.status_code != 200:
            log_str = 'status_code: {}, content: {}'.format(r.status_code, r.content)
            logging.error(log_str)
            return None
        space_history_json = json.loads(r.content)
        space_history_code = space_history_json.get('code')
        space_history_data = space_history_json.get('data')
        space_history_data_cards = space_history_data.get('cards')

        unread_flag = False if self.upuser.dynamics.count() == 0 else True

        for card in space_history_data_cards:
            desc = card.get('desc')
            card_type = desc.get('type')
            card_dynamic_id = desc.get('dynamic_id_str')

            dynamic, create_flag = DynamicModel.get_or_create(
                dynamic_id=card_dynamic_id,
                defaults={
                    'owner': self.upuser,
                    'type': card_type,
                    'unread': unread_flag
                }
            )

            if create_flag:
                log_str = '动态消息卡片：类型：{}，动态ID：{}，{}'.format(
                    dynamic.type, dynamic.dynamic_id, '未读' if dynamic.unread else '已读'
                )
                logging.info(log_str)
        return True
            
    def get_push_data(self):
        push_data = []
        if self.live_notification:
            push_body = {
                "title": "成员直播提醒",
                "data": "{}正在直播".format(self.upuser.uname),
                "url_data": "前往直播间",
                "url": "https://live.bilibili.com/{}".format(self.upuser.room_id)
            }
            push_data.append(push_body)
        unread_dynamics = self.upuser.dynamics.where(DynamicModel.unread==True)
        for unread_dynamic in unread_dynamics:
            push_body = {
                "title": "成员动态提醒",
                "data": "{}{}".format(
                    self.upuser.uname, 
                    "投稿了新视频" if unread_dynamic.type == 8 else "有了新动态"
                ),
                "url_data": "前往动态",
                "url": "https://t.bilibili.com/{}".format(unread_dynamic.dynamic_id)
            }
            push_data.append(push_body)
            unread_dynamic.unread = False
            unread_dynamic.save()
        logging.info(push_data)
        return push_data
