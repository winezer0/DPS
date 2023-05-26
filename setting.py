#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import pathlib
import sys
import time

from libs.lib_file_operate.file_path import auto_make_dir

sys.dont_write_bytecode = True  # 设置不生成pyc文件
##################################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
##################################################################
# 程序开始运行时间
GB_RUN_TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
##################################################################
# 版本号配置
GB_VERSION = "Ver 0.0.2 2023-05-27 04:30"
##################################################################
# 是否显示DEBUG级别信息,默认False
GB_DEBUG_FLAG = False
##################################################################
# 在配置文件中配置默认目标参数  支持文件 或 域名
GB_TARGET = "target.txt"
GB_PORTS = [80, 443, 8080, 8443, 8000, 9000]
GB_PROTOS = ["http", "https"]
##################################################################
# HTTP请求相关配置
# 默认线程数
GB_THREADS_COUNT = 100
# 每个线程之间的延迟 单位S秒
GB_THREAD_SLEEP = 0
# 任务分块大小 所有任务会被分为多个列表
GB_TASK_CHUNK_SIZE = GB_THREADS_COUNT
########################
# 默认请求方法
GB_REQ_METHOD = "get"
# 默认请求数据
GB_REQ_BODY = None
# 对外请求代理
GB_PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080",
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "https://192.168.88.1:8080",
    # "http": "socks5://192.168.88.1:1080",
}

# 采用流模式访问 流模式能够解决大文件读取问题
GB_STREAM_MODE = False
# 是否开启https服务器的证书校验
GB_SSL_VERIFY = False
# 超时时间 # URL重定向会严重影响程序的运行时间
GB_TIMEOUT = 10
# 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
GB_ALLOW_REDIRECTS = False
# 访问没有结果时,自动重试的最大次数
GB_RETRY_TIMES = 1
# 是否自动根据URL设置动态HOST头
GB_ADD_DYNAMIC_HOST = True
# 是否自动根据URL设置动态refer头
GB_ADD_DYNAMIC_REFER = True
# 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
GB_RANDOM_USERAGENT = False
# 是否允许随机X-Forwarded-For
GB_RANDOM_XFF = False
########################扩展的调用函数###################################
# 排除指定结果
# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
GB_EXCLUDE_STATUS = None
# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
GB_EXCLUDE_REGEXP = None  # r"页面不存在|未找到|not[ -]found|403|404|410"
##################################################################
# 设置日志输出文件路径 #目录不存在会自动创建
GB_LOG_FILE_FORMAT = str(GB_BASE_DIR.joinpath("runtime", "runtime_module.log"))
GB_INFO_LOG_STR = GB_LOG_FILE_FORMAT.replace('module', 'info')
GB_DEBUG_LOG_STR = GB_LOG_FILE_FORMAT.replace('module', 'debug')
GB_ERROR_LOG_STR = GB_LOG_FILE_FORMAT.replace('module', 'error')

# # 记录扫描已完成的URL 针对每个目标生成不同的记录文件
GB_HISTORY_FILE = GB_LOG_FILE_FORMAT.replace('module', 'history')
# # 每个HOST扫描URL的过滤,建议开启
GB_HISTORY_EXCLUDE = True
##################################################################
# 设置输出结果文件目录
GB_RESULT_DIR = GB_BASE_DIR.joinpath("result")
# GB_IGNORE_FILE_PATH = GB_RESULT_DIR.joinpath(f"ignore.{GB_RUN_TIME}.csv")
# GB_RESULT_FILE_PATH = GB_RESULT_DIR.joinpath(f"result.{GB_RUN_TIME}.csv")
GB_IGNORE_FILE_PATH = GB_RESULT_DIR.joinpath(f"ignore.csv")
GB_RESULT_FILE_PATH = GB_RESULT_DIR.joinpath(f"result.csv")
#######################################################################
auto_make_dir(GB_RESULT_DIR)
########################扩展的调用函数###################################
