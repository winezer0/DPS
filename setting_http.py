#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件

from libs.lib_args.input_const import *


def init_custom(config):
    """
    初始化本程序的自定义参数
    :param config:
    :return:
    """
    ##################################################################
    # HTTP请求相关配置
    # 默认请求方法
    config[GB_REQ_METHOD] = "GET"
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
    config[GB_TIME_OUT] = 5
    # 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
    config[GB_ALLOW_REDIRECTS] = False
    # 访问没有结果时,自动重试的最大次数
    config[GB_RETRY_TIMES] = 1
    ##################################################################
    # 默认请求头设置
    config[GB_REQ_HEADERS] = {
        # 'Host': 'testphp.vulnweb.com',    # 默认会自动添加请求HOST
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Origin': 'http://www.baidu.com/',   # 默认会自动添加请求URL
        # 'Referer': 'http://www.baidu.com/',  # 默认会自动添加请求URL
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        'Transfer-Encoding': 'identity',      # 多个请求头综合影响响应头CL的获取
        'Connection': 'close',
    }
    # 是否自动根据URL设置动态HOST头
    config[GB_DYNA_REQ_HOST] = True
    # 是否自动根据URL设置动态refer头
    config[GB_DYNA_REQ_REFER] = True
    # 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
    config[GB_RANDOM_UA] = False
    # 是否允许随机X-Forwarded-For  # 支持False|True|str 如 127.0.0.1
    config[GB_RANDOM_XFF] = False
    ##################################################################
    # 排除指定结果
    # 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
    config[GB_EXCLUDE_STATUS] = [502, 400]
    # 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.I 忽略大小写
    config[GB_EXCLUDE_REGEXP] = None  # r"页面不存在|未找到|not[ -]found|403|404|410"
    ##################################################################
