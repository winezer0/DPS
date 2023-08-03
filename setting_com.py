#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import pathlib
import time

from libs.lib_args.input_const import *
from libs.lib_file_operate.file_utils import auto_make_dir


def init_common(config):
    """
    初始化本程序的通用参数
    :param config:
    :return:
    """
    ##################################################################
    # 获取setting.py脚本所在路径作为的基本路径
    config[GB_BASE_DIR] = pathlib.Path(__file__).parent.resolve()
    ##################################################################
    # 程序开始运行时间
    config[GB_RUN_TIME] = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    ##################################################################
    # 版本号配置
    config[GB_VERSION] = "Ver 0.2.3 2023-8-03 15:30"
    ##################################################################
    # 是否显示DEBUG级别信息,默认False
    config[GB_DEBUG_FLAG] = False
    ##################################################################
    # 设置日志输出文件路径 #目录不存在会自动创建
    config[GB_LOG_INFO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_info.log").as_posix()
    config[GB_LOG_DEBUG_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_debug.log").as_posix()
    config[GB_LOG_ERROR_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_error.log").as_posix()
    ##################################################################
    # 设置输出结果文件目录
    config[GB_IGNORE_FORMAT] = config[GB_BASE_DIR].joinpath("result", "{mark}.ignore.csv").as_posix()
    config[GB_RESULT_FORMAT] = config[GB_BASE_DIR].joinpath("result", "{mark}.result.csv").as_posix()
    # 记录扫描已完成的URL 针对每个目标生成不同的记录文件
    config[GB_HISTORY_FORMAT] = config[GB_BASE_DIR].joinpath("result", '{mark}.history.log').as_posix()
    # 每个HOST扫描URL的过滤,建议开启
    config[GB_EXCLUDE_HISTORY] = True
    # # 每个域名的URL结果独立保存
    # config[GB_SINGLE_STORAGE] = True
    ##################################################################
    # 写入端口命中结果，记录常见web端口
    config[GB_SAVE_HIT_RESULT] = True
    config[GB_HIT_PORT_FILE] = config[GB_BASE_DIR].joinpath('ports.hit')
    #######################################################################


def init_custom(config):
    """
    初始化本程序的自定义参数
    :param config:
    :return:
    """
    ##################################################################
    # 在配置文件中配置默认目标参数  支持文件 或 URL
    config[GB_TARGET] = "target.txt"
    # 默认请求协议
    config[GB_PROTOS] = ["http", "https"]
    # 默认请求端口
    config[GB_PORTS] = [80, 443]  # "ports.txt"
    # 对于URL中的80 443 端口进行隐藏
    config[GB_REMOVE_80_443] = True
    # 对所有输入的目标都一律拆分为 HOST 便于进行端口扫描
    config[GB_ALL_2_HOST] = False
    # 对生成的URL添加默认访问的路径
    config[GB_PATHS] = None  # ["/"]  # "path.txt"
    # 使用绝对路径更新URL
    config[GB_PATH_ABSOLUTE] = False
    ##################################################################
    # 默认线程数
    config[GB_THREADS_COUNT] = 200
    # 每个线程之间的延迟 单位S秒  # 暂时无效
    config[GB_THREAD_SLEEP] = 0
    # 任务分块大小 所有任务会被分为多个列表
    config[GB_TASK_CHUNK_SIZE] = 200
    ##################################################################
