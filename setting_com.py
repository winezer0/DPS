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
    config[GB_VERSION] = "Ver 0.1.3 2023-07-29 08:00"
    ##################################################################
    # 是否显示DEBUG级别信息,默认False
    config[GB_DEBUG_FLAG] = False
    ##################################################################
    # 设置日志输出文件路径 #目录不存在会自动创建
    config[GB_LOG_INFO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_info.log").as_posix()
    config[GB_LOG_DEBUG_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_debug.log").as_posix()
    config[GB_LOG_ERROR_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_error.log").as_posix()
    ##################################################################
    # 记录扫描已完成的URL 针对每个目标生成不同的记录文件
    config[GB_HISTORY_FORMAT] = config[GB_BASE_DIR].joinpath("runtime", '{host_port}.history.log').as_posix()
    # # 每个HOST扫描URL的过滤,建议开启
    config[GB_EXCLUDE_HISTORY] = True
    ##################################################################
    # 设置输出结果文件目录
    config[GB_IGNORE_FORMAT] = config[GB_RESULT_DIR].joinpath("result","{host_port}.ignore.csv").as_posix()
    config[GB_RESULT_FORMAT] = config[GB_RESULT_DIR].joinpath("result","{host_port}.result.csv").as_posix()
    ##################################################################


def init_custom(config):
    """
    初始化本程序的自定义参数
    :param config:
    :return:
    """
    ##################################################################
    # 在配置文件中配置默认目标参数  支持文件 或 URL
    config[GB_TARGET] = "target.txt"
    config[GB_PORTS] = "ports.txt"
    ##################################################################
    # 默认线程数
    config[GB_THREADS_COUNT] = 200
    # 每个线程之间的延迟 单位S秒
    config[GB_THREAD_SLEEP] = 0
    # 任务分块大小 所有任务会被分为多个列表
    config[GB_TASK_CHUNK_SIZE] = 200
    ##################################################################
    # 写入命中结果
    config[GB_SAVE_HIT_RESULT] = True
    config[GB_HIT_PORT_FILE] = config[GB_BASE_DIR].joinpath('ports.hit')
    #######################################################################
