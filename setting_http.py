#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件

from libs.input_const import *


def init_custom(config):
    """
    初始化本程序的自定义参数
    :param config:
    :return:
    """
    ##################################################################
    # HTTP请求相关配置
    # 默认请求协议
    config[GB_PROTOS] = ["http"] # ["http", "https"]
    # 默认请求方法
    config[GB_REQ_METHOD] = "get"
    # 默认请求数据
    config[GB_REQ_BODY] = None
    # 对外请求代理
    config[GB_PROXIES] = {
        # "http": "http://127.0.0.1:8080",
        # "https": "http://127.0.0.1:8080",
        # "http": "http://user:pass@10.10.1.10:3128/",
        # "https": "https://192.168.88.1:8080",
        # "http": "socks5://192.168.88.1:1080",
    }

    # 采用流模式访问 流模式能够解决大文件读取问题
    config[GB_STREAM_MODE] = False
    # 是否开启https服务器的证书校验
    config[GB_SSL_VERIFY] = False
    # 超时时间 # URL重定向会严重影响程序的运行时间
    config[GB_TIME_OUT] = 10
    # 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
    config[GB_ALLOW_REDIRECTS] = False
    # 访问没有结果时,自动重试的最大次数
    config[GB_RETRY_TIMES] = 0
    ##################################################################
    # 默认请求头设置
    config[GB_REQ_HEADERS] = {}
    # 是否自动根据URL设置动态HOST头
    config[GB_DYNA_REQ_HOST] = True
    # 是否自动根据URL设置动态refer头
    config[GB_DYNA_REQ_REFER] = True
    # 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
    config[GB_RANDOM_UA] = False
    # 是否允许随机X-Forwarded-For
    config[GB_RANDOM_XFF] = False
    ##################################################################
    # 排除指定结果
    # 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
    config[GB_EXCLUDE_STATUS] = []
    # 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
    config[GB_EXCLUDE_REGEXP] = None  # r"页面不存在|未找到|not[ -]found|403|404|410"
