# -*- coding: utf-8 -*-
import os, json
class anp_config():

    version = 'v1.0.0'
    config = {
        "version": "{}".format(version),
        "push": {
            "wx_config": {
                "agentid": "",
                "secret": "",
                "corpid": ""
            }
        },
        "members": [
            {
                "uid": "672346917",
                "nickname": "向晚"
            },
            {
                "uid": "672353429",
                "nickname": "贝拉"
            },
            {
                "uid": "351609538",
                "nickname": "珈乐"
            },
            {
                "uid": "672328094",
                "nickname": "嘉然"
            },
            {
                "uid": "672342685",
                "nickname": "乃琳"
            },
            {
                "uid": "703007996",
                "nickname": "asoul"
            }
        ]
    }

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        if not os.path.exists(self.config_file):
            self.update_config()
            print('初始化 {} 完成，请前往完成相关配置！'.format(self.config_file))
            exit(1)
        else:
            self.check_version()
            self.load_config()

    def update_config_version(self, local_config):
        # if local_config.get('version') == 'v1.0.0':
        #     local_config['version'] = 'v1.0.1'
        self.config = local_config
        self.update_config()

    def check_version(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            local_config = json.load(json_file)
        if not local_config.get('version') == self.version:
            self.update_config_version(local_config)

    def load_config(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            self.config = json.load(json_file)
        return self.config

    def update_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.config, json_file, indent=4, ensure_ascii=False)
