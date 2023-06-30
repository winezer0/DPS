#!/usr/bin/env python
# encoding: utf-8

# 获得随机字符串
import copy
import hashlib
import random
import re

from libs.lib_file_operate.file_write import write_line, write_title
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_DEBUG, LOG_ERROR
from libs.lib_requests.requests_const import *


# 判断列表内的元素是否存在有包含在字符串内的
def list_ele_in_str(list_=None, str_=None, default=False):
    if list_ is None:
        list_ = []

    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


# 获得随机字符串
def get_random_str(length=12, has_num=True, has_capital=True, has_symbols=False, has_dot=False, with_slash=False):
    base_str = 'abcdefghigklmnopqrstuvwxyz'
    if has_num:
        base_str += '0123456789'
    if has_capital:
        base_str += 'ABCDEFGHIGKLMNOPQRSTUVWXYZ'
    if has_symbols:
        base_str += '~!@#$%^&*()_+-=><'

    random_str = ''
    for i in range(0, length - 1):
        if has_dot and i == length - 5:
            random_str += '.'
        else:
            random_str += base_str[random.randint(0, len(base_str) - 1)]
    if with_slash:
        random_str = '/' + random_str
    return random_str


# 随机生成User-Agent
def random_useragent(user_agents, condition=False):
    if condition:
        return random.choice(user_agents)
    else:
        return user_agents[0]


# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),
                                random.randint(1, 254),
                                random.randint(1, 254),
                                random.randint(1, 254))
    else:
        return '127.0.0.1'


# 分析 多个 字典列表 的 每个键的值是否相同, 并且不为默认值或空值
def analysis_dict_same_keys(result_dict_list, default_value_dict, filter_ignore_keys):
    same_key_value_dict = {}
    # 对结果字典的每个键做对比
    for key in list(result_dict_list[0].keys()):
        if key not in filter_ignore_keys:
            value_list = [value_dict[key] for value_dict in result_dict_list]
            # all() 是 Python 的内置函数之一，用于判断可迭代对象中的所有元素是否都为 True
            if all(value == value_list[0] for value in value_list):
                value = value_list[0]
                if key in list(default_value_dict.keys()):
                    if value not in default_value_dict[key]:
                        output(f"[*] 所有DICT [{key}] 值 [{value}] 相等 且不为默认或空值 [{default_value_dict[key]}]",
                               level=LOG_DEBUG)
                        same_key_value_dict[key] = value
                    else:
                        output(f"[-] 所有DICT [{key}] 值 [{value}] 相等 但是默认或空值 [{default_value_dict[key]}]",
                               level=LOG_DEBUG)
                else:
                    output(f"[!] 存在未预期的键{key},该键不在默认值字典[{list(default_value_dict.keys())}]内!!!", level=LOG_ERROR)
    return same_key_value_dict


def calc_dict_info_hash(resp_dict):
    # 固化响应结果的hash特征
    # output(f"[*] calc_dict_info_hash: {resp_dict}", level=LOG_ERROR)
    # return str(resp_dict)

    # 对字典的键值对进行排序
    sorted_items = sorted(resp_dict.items())
    # 创建 哈希对象
    hash_object = hashlib.md5()
    # 更新哈希对象的输入数据
    hash_object.update(str(sorted_items).encode())
    # 计算哈希值
    hash_value = hash_object.hexdigest()
    return hash_value


def copy_dict_remove_keys(resp_dict, remove_keys=None):
    # 移除响应字典中和URL相关的选项, 仅保留响应部分
    # {'HTTP_REQ_URL': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_CONST_SIGN': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_RESP_REDIRECT_URL': 'HTTP_RAW_REDIRECT_URL'}   # 可选排除
    # 保留原始dict数据
    copy_resp_dict = copy.copy(resp_dict)
    if remove_keys is None:
        remove_keys = [HTTP_REQ_URL, HTTP_CONST_SIGN]
    for remove_key in remove_keys:
        # copy_resp_dict[remove_key] = ""  # 清空指定键的值
        copy_resp_dict.pop(remove_key, "")  # 删除指定键并返回其对应的值 # 删除不存在的键时，指定默认值，不会引发异常
    # output(f"[*] 新的字典键数量:{len(copy_resp_dict.keys())}, 原始字典键数量:{len(resp_dict.keys())}", level=LOG_DEBUG)
    return copy_resp_dict


# 访问结果处理
def access_result_handle(result_dict_list,
                         dynamic_exclude_dict=None,
                         ignore_file="ignore.csv",
                         result_file="result.csv",
                         history_file="history.csv",
                         access_fail_count=0,
                         exclude_status_list=None,
                         exclude_title_regexp=None,
                         max_error_num=None,
                         history_field=HTTP_CONST_SIGN,
                         hit_saving_field=HTTP_CONST_SIGN,
                         hit_info_exclude=False,
                         hit_info_hash_list=None):
    # 兼容旧版本 记录已命中结果的特征信息,用于过滤已命中的结果
    if hit_info_hash_list is None:
        hit_info_hash_list = []

    # 错误结果超出阈值
    should_stop_run = False

    # 访问失败的结果 # 就是除去URL和SING之外都是默认值
    access_fail_resp_dict = copy_dict_remove_keys(HTTP_DEFAULT_RESP_DICT)

    # 本次扫描的所有命中结果 默认保存的是 请求响应的 CONST_SIGN 属性
    hit_result_list = []

    # 响应结果处理
    for access_resp_dict in result_dict_list:
        # 是否忽略响应结果
        IGNORE_RESP = False

        # 判断请求是否错误（排除url和const_sign）
        # 字典可以直接使用 == 运算符进行比较，要求 字典中的键必须是可哈希的（即不可变类型）
        if not IGNORE_RESP and access_fail_resp_dict == copy_dict_remove_keys(access_resp_dict):
            access_fail_count += 1
            IGNORE_RESP = True

        # 排除状态码被匹配的情况
        resp_status = access_resp_dict[HTTP_RESP_STATUS]
        if not IGNORE_RESP and exclude_status_list and resp_status in exclude_status_list:
            IGNORE_RESP = True

        # 排除标题被匹配的情况
        resp_text_title = access_resp_dict[HTTP_RESP_TEXT_TITLE]
        if not IGNORE_RESP and exclude_title_regexp and re.match(exclude_title_regexp, resp_text_title, re.IGNORECASE):
            IGNORE_RESP = True

        # 排除响应结果被匹配的情况
        if not IGNORE_RESP and dynamic_exclude_dict:
            for filter_key in list(dynamic_exclude_dict.keys()):
                filter_value = dynamic_exclude_dict[filter_key]  # 被排除的值
                access_resp_value = access_resp_dict[filter_key]
                ignore_value_list = HTTP_FILTER_VALUE_DICT[filter_key]
                if access_resp_value != filter_value and access_resp_value not in ignore_value_list:
                    # 存在和排除关键字不同的项, 并且 这个值不是被忽略的值时 写入结果文件
                    break
            else:
                IGNORE_RESP = True

        # 计算结果hash并判断是否是已命中结果
        if hit_info_exclude and not IGNORE_RESP:
            hit_info_hash = calc_dict_info_hash(copy_dict_remove_keys(access_resp_dict))
            if hit_info_hash in hit_info_hash_list:
                output(f"[!] 忽略命中 [{hit_info_hash}] <--> {access_resp_dict[HTTP_REQ_URL]}", level=LOG_ERROR)
                IGNORE_RESP = True
            else:
                # output(f"[!] 保留命中 [{hit_info_hash}]", level=LOG_INFO)
                hit_info_hash_list.append(hit_info_hash)

        # 写入结果格式
        result_format = "\"%s\"," * len(access_resp_dict.keys()) + "\n"
        # 当前需要保存和显示的字段
        saving_field = access_resp_dict[hit_saving_field]
        # 按照指定的顺序获取 dict 的 values
        key_order_list = list(access_resp_dict.keys())
        key_order_list.sort()  # 按字母排序
        access_resp_values = tuple([access_resp_dict[key] for key in key_order_list])

        if IGNORE_RESP:
            # 写入结果表头
            write_title(ignore_file, result_format % tuple(key_order_list), encoding="utf-8", new_line=True, mode="a+")
            write_line(ignore_file, result_format % access_resp_values, encoding="utf-8", new_line=True, mode="a+")
            output(f"[-] 忽略结果 [{saving_field}]", level=LOG_DEBUG)
        else:
            # 写入结果表头
            write_title(result_file, result_format % tuple(key_order_list), encoding="utf-8", new_line=True, mode="a+")
            write_line(result_file, result_format % access_resp_values, encoding="utf-8", new_line=True, mode="a+")
            output(f"[+] 可能存在 [{saving_field}]", level=LOG_INFO)
            # 加入到命中结果列表
            hit_result_list.append(saving_field)

        # 取消继续访问进程 错误太多 或者 已经爆破成功
        if isinstance(max_error_num, int) and access_fail_count >= max_error_num:
            output(f"[*] 错误数量超过阈值 取消访问任务!!!", level=LOG_ERROR)
            should_stop_run = True

        # 写入历史爆破记录文件
        write_line(history_file, f"{access_resp_dict[history_field]}", encoding="utf-8", new_line=True, mode="a+")
    return should_stop_run, hit_result_list
