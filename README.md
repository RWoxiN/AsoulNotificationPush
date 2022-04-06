# A-SOUL Notification Push

该脚本获取 A-SOUL 新动态以及直播状态，并推送到企业微信中。

# 使用

自行配置 python3 环境，并安装依赖库。

第一次运行会生成 `config.json` 配置文件，在其中配置企业微信相关设置。

而后运行 `python main.py` 即可运行一次。可通过配置 crontab 定时执行。