#!/usr/bin/env python
# encoding: utf-8

import os

import setting_com
import setting_http
from libs.lib_args.input_const import *
from libs.lib_args.input_parse import args_parser, args_dict_handle, config_dict_handle
from libs.lib_args.input_basic import config_dict_add_args
from libs.lib_attribdict.config import CONFIG
from libs.lib_file_operate.file_path import auto_make_dir
from libs.lib_file_operate.file_write import write_path_list_to_frequency_file
from libs.lib_log_print.logger_printer import output, LOG_INFO, set_logger, LOG_ERROR
from libs.lib_requests.requests_const import HTTP_REQ_URL
from libs.lib_requests.requests_thread import multi_thread_requests_url
from libs.lib_requests.requests_tools import access_result_handle
from libs.utils import result_rule_classify, gen_url_list, \
    exclude_history_record, init_input_domain, init_input_ports, init_input_proto


# 进行爆破任务
def actions_controller(config_dict):
    # 对输入的目标数量进行处理
    domain_list = init_input_domain(config_dict[GB_TARGET])
    port_list = init_input_ports(config_dict[GB_PORTS])
    proto_list = init_input_proto(config_dict[GB_PROTOS])

    # 对输入的目标数量进行判断
    if not domain_list or not port_list or not proto_list:
        output("[-] 未输入有效目标...TARGET:{GB_TARGET} PORTS:{GB_PORTS} PROTOS:{GB_PROTOS}", level=LOG_ERROR)
        exit()

    for domain_index, domain in enumerate(domain_list):
        output(f"[+] 任务进度 {domain_index + 1}/{len(domain_list)} {domain}", level=LOG_INFO)

        # 相关文件路径
        cur_history_file = config_dict[GB_HISTORY_FORMAT].format(host_port=domain)
        cur_result_file = config_dict[GB_RESULT_FORMAT].format(host_port=domain)
        cur_ignore_file = config_dict[GB_IGNORE_FORMAT].format(host_port=domain)

        # 组合扫描URL
        url_list = gen_url_list(proto_list, [domain], port_list)

        # 进行URL排除操作
        if config_dict[GB_EXCLUDE_HISTORY]:
            url_list = exclude_history_record(url_list, cur_history_file)
            if not len(url_list):
                continue

        # 将任务列表拆分为多个任务列表 再逐步进行爆破,便于统一处理结果
        task_size = config_dict[GB_TASK_CHUNK_SIZE]
        brute_task_list = [url_list[i:i + task_size] for i in range(0, len(url_list), task_size)]
        output(f"[*] 任务拆分 SIZE:[{task_size}] * NUM:[{len(brute_task_list)}]", level=LOG_INFO)

        # 循环多线程请求操作
        for sub_task_index, sub_task_list in enumerate(brute_task_list):
            output(f"[*] 任务进度 {sub_task_index + 1}/{len(brute_task_list)}", level=LOG_INFO)
            result_dict_list = multi_thread_requests_url(task_list=sub_task_list,
                                                         threads_count=config_dict[GB_THREADS_COUNT],
                                                         thread_sleep=config_dict[GB_THREAD_SLEEP],
                                                         # req_url,
                                                         req_method=config_dict[GB_REQ_METHOD],
                                                         req_headers=config_dict[GB_REQ_HEADERS],
                                                         req_data=config_dict[GB_REQ_BODY],
                                                         req_proxies=config_dict[GB_PROXIES],
                                                         req_timeout=config_dict[GB_TIME_OUT],
                                                         verify_ssl=config_dict[GB_SSL_VERIFY],
                                                         req_allow_redirects=config_dict[GB_ALLOW_REDIRECTS],
                                                         req_stream=config_dict[GB_STREAM_MODE],
                                                         retry_times=config_dict[GB_RETRY_TIMES],
                                                         const_sign=domain,
                                                         add_host_header=config_dict[GB_DYNA_REQ_HOST],
                                                         add_refer_header=config_dict[GB_DYNA_REQ_REFER],
                                                         ignore_encode_error=True
                                                         )

            # 处理响应结果
            stop_run, hit_result_list = access_result_handle(result_dict_list=result_dict_list,
                                                             dynamic_exclude_dict=None,
                                                             ignore_file=cur_ignore_file,
                                                             result_file=cur_result_file,
                                                             history_file=cur_history_file,
                                                             access_fail_count=0,
                                                             exclude_status_list=config_dict[GB_EXCLUDE_STATUS],
                                                             exclude_title_regexp=config_dict[GB_EXCLUDE_REGEXP],
                                                             max_error_num=None,
                                                             hit_saving_field=HTTP_REQ_URL,
                                                             history_field=HTTP_REQ_URL, )
            # 记录已命中的端口号
            if config_dict[GB_SAVE_HIT_RESULT] and hit_result_list:
                # 分析命中的结果
                hit_classify_dict = result_rule_classify(hit_str_list=hit_result_list,
                                                         hit_port_file=config_dict[GB_HIT_PORT_FILE])
                # 将命中的结果分别写到不同的频率文件中
                for file_name, path_list in hit_classify_dict.items():
                    auto_make_dir(os.path.dirname(file_name))
                    write_path_list_to_frequency_file(file_path=file_name, path_list=path_list)
                output(f"[*] 记录命中结果规则: {len(hit_result_list)}", level=LOG_INFO)
    output(f"[+] 所有URL测试完毕...", level=LOG_INFO)


if __name__ == "__main__":
    # 加载初始设置参数
    setting_com.init_common(CONFIG)
    setting_com.init_custom(CONFIG)
    setting_http.init_custom(CONFIG)

    # 设置默认debug参数日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], True)

    # 输入参数解析
    args = args_parser(CONFIG)
    output(f"[*] 输入参数信息: {args}")

    # 处理输入参数
    updates = args_dict_handle(args)
    output(f"[*] 输入参数更新: {updates}")

    # 将输入参数加入到全局CONFIG
    config_dict_add_args(CONFIG, args)

    # 更新全局CONFIG
    updates = config_dict_handle(CONFIG)
    output(f"[*] 配置参数更新: {updates}")

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], CONFIG[GB_DEBUG_FLAG])

    # 输出所有参数信息
    output(f"[*] 最终配置信息: {CONFIG}", level=LOG_INFO)

    # 进行扫描任务
    actions_controller(CONFIG)
