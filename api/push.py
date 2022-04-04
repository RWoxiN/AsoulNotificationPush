# -*- coding: utf-8 -*-

import json
import requests


def wx_push(message):
    touser = '@all'
    
    # TODO: 填入自己的配置
    agentid = '应用ID'
    secret = ''
    corpid = '企业ID'

    json_dict = {
        "touser": touser,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }

    response = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}")
    data = json.loads(response.text)
    access_token = data['access_token']

    json_str = json.dumps(json_dict)
    response_send = requests.post(
        f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    return json.loads(response_send.text)['errmsg'] == 'ok'
