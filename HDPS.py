#!/usr/bin/env python
# encoding: utf-8

import argparse
import os

from pyfiglet import Figlet

from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_path_list_to_frequency_file
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR, set_logger
from libs.lib_requests.requests_const import HTTP_REQ_URL, HTTP_USER_AGENTS
from libs.lib_requests.requests_thread import multi_thread_requests_url
from libs.lib_requests.requests_tools import access_result_handle, random_useragent, random_x_forwarded_for
from libs.utils import result_rule_classify, init_input_target
from setting import *


# 进行爆破任务
def domain_port_scan(urls):
    # 将任务列表拆分为多个任务列表 再逐步进行爆破,便于统一处理结果
    task_size = GB_TASK_CHUNK_SIZE
    brute_task_list = [urls[i:i + task_size] for i in range(0, len(urls), task_size)]
    output(f"[*] 任务拆分 SIZE:[{task_size}] * NUM:[{len(brute_task_list)}]", level=LOG_INFO)

    # 循环多线程请求操作
    for sub_task_index, sub_task_list in enumerate(brute_task_list):
        output(f"[*] 任务进度 {sub_task_index + 1}/{len(brute_task_list)}", level=LOG_INFO)
        result_dict_list = multi_thread_requests_url(task_list=sub_task_list,
                                                     threads_count=GB_THREADS_COUNT,
                                                     thread_sleep=GB_THREAD_SLEEP,
                                                     # req_url,
                                                     req_method=GB_REQ_METHOD,
                                                     req_headers=REQ_HEADERS,
                                                     req_data=GB_REQ_BODY,
                                                     req_proxies=GB_PROXIES,
                                                     req_timeout=GB_TIMEOUT,
                                                     verify_ssl=GB_SSL_VERIFY,
                                                     req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                     req_stream=GB_STREAM_MODE,
                                                     retry_times=GB_RETRY_TIMES,
                                                     const_sign=None,
                                                     add_host_header=GB_ADD_DYNAMIC_HOST,
                                                     add_refer_header=GB_ADD_DYNAMIC_REFER,
                                                     ignore_encode_error=True
                                                     )

        # 处理响应结果
        stop_run, hit_result_list = access_result_handle(result_dict_list=result_dict_list,
                                                         dynamic_exclude_dict=None,
                                                         ignore_file=GB_IGNORE_FILE_PATH,
                                                         result_file=GB_RESULT_FILE_PATH,
                                                         history_file=GB_HISTORY_FILE,
                                                         access_fail_count=0,
                                                         exclude_status_list=GB_EXCLUDE_STATUS,
                                                         exclude_title_regexp=GB_EXCLUDE_REGEXP,
                                                         max_error_num=None,
                                                         hit_saving_field=HTTP_REQ_URL,
                                                         history_field=HTTP_REQ_URL, )
        # 记录已命中的端口号
        if GB_SAVE_HIT_RESULT and hit_result_list:
            # 分析命中的结果
            hit_classify_dict = result_rule_classify(hit_str_list=hit_result_list,
                                                     hit_port_file=GB_HIT_PORT_FILE)
            # 将命中的结果分别写到不同的频率文件中
            for file_name, path_list in hit_classify_dict.items():
                auto_make_dir(os.path.dirname(file_name))
                write_path_list_to_frequency_file(file_path=file_name, path_list=path_list)
            output(f"[*] 记录命中结果规则: {len(hit_result_list)}", level=LOG_INFO)
    output(f"[+] 所有URL测试完毕...", level=LOG_INFO)


def parse_input():
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("HDPS")

    # 指定扫描URL或文件
    argument_parser.add_argument("-u", "--target", default=GB_TARGET, nargs="+",
                                 help=f"Specify the target URLs or Target File, Default is [{GB_TARGET}]")
    # 指定扫描的端口号
    argument_parser.add_argument("-p", "--ports", default=GB_PORTS, nargs="+",
                                 help=f"Specify the ports list or ports File, Default is [{GB_PORTS}]")
    # 指定扫描的协议类型
    argument_parser.add_argument("-P", "--protos", default=GB_PROTOS, nargs="+",
                                 help=f"Specify the proto list or proto string, Default is [{GB_PROTOS}]")
    # 指定请求代理服务
    argument_parser.add_argument("-x", dest="proxies", default=GB_PROXIES,
                                 help=f"Specifies http|https|socks5 proxies, Default is [{GB_PROXIES}]")

    # 指定请求线程数量
    argument_parser.add_argument("-t", "--threads_count", default=GB_THREADS_COUNT, type=int,
                                 help=f"Specifies request threads, Default is [{GB_THREADS_COUNT}]")
    # 开启调试功能
    argument_parser.add_argument("-d", "--debug_flag", default=GB_DEBUG_FLAG, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is [{GB_DEBUG_FLAG}]", )

    # 开启随机UA
    argument_parser.add_argument("-ru", "--random_useragent", default=GB_RANDOM_USERAGENT, action="store_true",
                                 help=f"Specifies Start Random useragent, Default is [{GB_RANDOM_USERAGENT}]", )
    # 开启随机XFF
    argument_parser.add_argument("-rx", "--random_xff", default=GB_RANDOM_XFF, action="store_true",
                                 help=f"Specifies Start Random XFF Header, Default is [{GB_RANDOM_XFF}]", )
    # 关闭流模式扫描
    argument_parser.add_argument("-ss", "--stream_mode", default=GB_STREAM_MODE, action="store_false",
                                 help=f"Shutdown Request Stream Mode, Default is [{GB_STREAM_MODE}]", )
    # 关闭历史扫描URL过滤
    argument_parser.add_argument("-sh", "--history_exclude", default=GB_HISTORY_EXCLUDE, action="store_false",
                                 help=f"Shutdown Exclude Request History, Default is [{GB_HISTORY_EXCLUDE}]", )

    # 排除匹配指定的状态码的响应结果
    argument_parser.add_argument("-es", dest="exclude_status", default=GB_EXCLUDE_STATUS, nargs='+', type=int,
                                 help=f"Specified Response Status List Which Exclude, Default is {GB_EXCLUDE_STATUS}")
    # 排除匹配指定正则的响应结果
    argument_parser.add_argument("-er", dest="exclude_regexp", default=GB_EXCLUDE_REGEXP,
                                 help=f"Specified RE String When response matches the Str Excluded, Default is [{GB_EXCLUDE_REGEXP}]")

    # 指定默认请求方法
    argument_parser.add_argument("-rm", "--req_method", default=GB_REQ_METHOD,
                                 help=f"Specifies request method, Default is [{GB_REQ_METHOD}]")
    # 指定请求超时时间
    argument_parser.add_argument("-tt", "--timeout", default=GB_TIMEOUT, type=int,
                                 help=f"Specifies request timeout, Default is [{GB_TIMEOUT}]")
    # 指定自动错误重试次数
    argument_parser.add_argument("-rt", "--retry_times", default=GB_RETRY_TIMES, type=int,
                                 help=f"Specifies request retry times, Default is [{GB_RETRY_TIMES}]")

    example = """Examples:
             \r  批量扫描 target.txt
             \r  python3 {shell_name} -u target.txt
             \r  指定扫描 baidu.com
             \r  python3 {shell_name} -u www.baidu.com
             \r  
             \r  其他控制细节参数可通过setting.py进行配置
             \r  T00L Version: {version}
             \r  """

    argument_parser.epilog = example.format(shell_name=argument_parser.prog, version=GB_VERSION)

    return argument_parser


if __name__ == "__main__":
    # 输入参数解析
    parser = parse_input()

    # 输出所有参数
    args = parser.parse_args()
    output(f"[*] 所有输入参数信息: {args}")
    time.sleep(0.1)

    # 使用字典解压将参数直接赋值给相应的全局变量
    for param_name, param_value in vars(args).items():
        globals_var_name = f"GB_{param_name.upper()}"
        try:
            globals()[globals_var_name] = param_value
            # output(f"[*] INPUT:{globals_var_name} -> {param_value}", level=LOG_DEBUG)
        except Exception as error:
            output(f"[!] 输入参数信息: {param_name} {param_value} 未对应其全局变量!!!", level=LOG_ERROR)
            exit()

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_STR, GB_ERROR_LOG_STR, GB_DEBUG_LOG_STR, GB_DEBUG_FLAG)

    # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    if GB_PROXIES and isinstance(GB_PROXIES, str):
        if "socks" in GB_PROXIES or "http" in GB_PROXIES:
            GB_PROXIES = {'http': GB_PROXIES.replace('https://', 'http://'),
                          'https': GB_PROXIES.replace('http://', 'https://')}
        else:
            output(f"[!] 输入的代理地址[{GB_PROXIES}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)

    # HTTP 头设置
    REQ_HEADERS = {
        'User-Agent': random_useragent(HTTP_USER_AGENTS, GB_RANDOM_USERAGENT),
        'X_FORWARDED_FOR': random_x_forwarded_for(GB_RANDOM_XFF),
        'Accept-Encoding': ''
    }

    # 对输入的目标数量进行处理
    target_list = init_input_target(GB_TARGET, GB_PORTS, GB_PROTOS)

    # 排除历史扫描记录
    if GB_HISTORY_EXCLUDE:
        if file_is_exist(GB_HISTORY_FILE):
            accessed_url_list = read_file_to_list(file_path=GB_HISTORY_FILE, de_strip=True, de_weight=True,
                                                  de_unprintable=False)
            target_list = list(set(target_list) - set(accessed_url_list))
            output(f"[*] 历史访问URL {len(accessed_url_list)}个", level=LOG_INFO)
            output(f"[*] 剔除历史URL 剩余URL:{len(target_list)}个", level=LOG_INFO)

    # 对输入的目标数量进行判断
    if len(target_list) == 0:
        output("[-] 未输入任何有效目标或字典...", level=LOG_ERROR)
        exit()

    # 进行扫描任务
    domain_port_scan(target_list)
