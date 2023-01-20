# A-SOUL Notification Push

该脚本获取 A-SOUL 成员新动态以及直播状态，并推送到企业微信中。

2023.01.20: 因为B站api改动等原因大概已经用不了了，懒得排查改了，就这样吧

https://github.com/RWoxiN/AsoulNotificationPush

# 图示

![image-20220410145431263](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101454394.png)

# 使用

## 安装

### 手动安装

1. 在需要放置脚本的目录 `git clone https://github.com/RWoxiN/AsoulNotificationPush.git`，服务器无法连接 github 的话可使用同步 gitee 库 `git clone https://gitee.com/RWoxiN/AsoulNotificationPush.git `。
2. 自行配置 python3 环境，此处建议使用 python3.10，如使用 python3.7 需在配置文件中将 `low_version_python_compatible` 置为 `true`。在目录下运行 `python -m venv venv` 创建虚拟环境，`source /venv/bin/activate` 使用进入虚拟环境，而后运行 `pip install -r requirements.txt` 安装依赖。
3. 运行 `python main.py`。初次使用会生成 config.json 文件后结束程序，完成配置后再次运行即可正常使用。
4. 在配置文件完成修改后运行 `python main.py` 即可获取一次动态、直播数据。
5. 通过 crontab 定时运行该程序，如设置每隔五分钟运行一次，即意味着每隔五分钟检查一次动态、直播状态，如有新动态或开播就会推送。时间间隔建议使用五分钟，间隔过短 B（叔）站（叔）会限制访问，需要一两个小时后才会恢复正常。

## 通过 shell 脚本定时执行

按照上述安装步骤安装脚本，使得脚本能够正常运行。此节详细展示了手动安装中第五步 crontab 定时执行程序的具体步骤。

### 通过宝塔配置（推荐）

在宝塔界面中添加计划任务。任务类型选择 Shell 脚本，执行周期选择 5 分钟，脚本内容如下：

```bash
#!/bin/bash
varpath="/home/rian/asoul/AsoulNotificationPush"
cd ${varpath}
source ./venv/bin/activate
python ./main.py
```

![image-20220410151636193](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101516243.png)

### 通过 crontab 命令手动配置

1. 确保程序可以通过虚拟环境中 `python main.py` 正常执行后，创建 `start.sh` 脚本。内容如下：

   ```bash
   #!/bin/bash
   vardate=$(date +%c)
   varpath="/home/rian/asoul/AsoulNotificationPush"
   cd ${varpath}
   source ./venv/bin/activate
   python ./main.py
   echo "${vardate}: runing succeed!" >> ./start.log 2>&1
   ```

2. 给 `start.sh` 脚本添加权限。`chmod u+x start.sh`

3. 执行 `sh start.sh` 测试运行。

4. 设置定时任务 `crontab -e`：

   ```
   */5 * * * * /home/rian/asoul/AsoulNotificationPush/start.sh >> /home/rian/asoul/AsoulNotificationPush/start.log 2>&1
   ```

## 配置文件

首次运行时会在本地目录自动生成 config.json。需手动修改配置文件后方可正常运行程序。

在版本更新后，程序会自动更新配置文件，将旧版本迁移到新版本，配置文件中新增的功能如要使用还需手动配置。

### 推送配置

目前仅支持企业微信推送，企业微信配送内容获取详见下文。

```json
"push": {
    "wx_config": {
        "agentid": "",
        "secret": "",
        "corpid": ""
    }
}
```

### 推送成员配置

默认为 A-SOUL 五位成员以及 A-SOUL_Official，无特殊需求无需修改。uid 为该用户 B 站 uid，nickname 仅作配置文件区分用。该配置同样可以新增其他 up 主项来推送。

```json
"members": [
    {
        "uid": "672346917",
        "nickname": "向晚"
    }
]
```

### 其他配置

`low_version_python_compatible`：该项为低版本 python 兼容项，如日志模块无法正常运行，可将该项置为 `True`。

# 企业微信推送配置

## 注册企业微信

在[企业微信官网](https://work.weixin.qq.com/)注册一个企业微信，如已拥有，可忽略此步。

![image-20220410153654472](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101536551.png)



## 创建应用

进入企业微信后台，选择【应用管理】-【应用】-【自建】-【创建应用】。

![image-20220410153941651](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101539753.png)

填入应用名称以及应用 logo 后，可见部门选择需要推送的人或部门，创建应用。

## 获取配置

创建好应用后进入应用管理界面，将【AgentId】和【Secret】记录下来，并填入脚本配置文件的 `agentid` 和 `secret` 中。

![image-20220410154232444](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101542509.png)

进入【我的企业】-【企业信息】中，将【企业ID】记录下来，填入脚本配置文件的 `corpid` 中。

![image-20220410154506878](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101545974.png)

## 配置微信接收企业微信消息

进入【我的企业】-【微信插件】中，关注下方二维码。此时企业微信和微信能够同时收到消息。

![image-20220410154732143](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202204101547291.png)
