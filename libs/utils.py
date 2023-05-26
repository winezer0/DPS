import itertools
import sys

from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_log_print.logger_printer import output, LOG_ERROR
from urllib.parse import urlparse

def result_rule_classify(hit_str_list, hit_port_file):
    # 分析扫描结果
    hit_classify = {hit_port_file: []}
    for url in hit_str_list:
        port = urlparse(url).port
        hit_classify[hit_port_file].append(port)
    return hit_classify


def parse_input_ports(input_ports):
    # 检测端口后端小于前端的问题
    ports = []
    for port_string in input_ports:
        if file_is_exist(port_string):
            lists = read_file_to_list(file_path=port_string, de_strip=True, de_weight=True, de_unprintable=True)
            ports.extend(lists)
        else:
            if ',' in str(port_string):
                output(f"[!] 错误输入{port_string} Ports不支持逗号,请使用[空格]和[-]限定范围! 如:8080 80-443", level=LOG_ERROR)
                exit()
            elif '-' in str(port_string):
                port_start = int(port_string.split("-")[0].strip())
                port_end = int(port_string.split("-")[1].strip())
                if port_end < port_start:
                    output(f'[!] 端口 {port_string} 范围格式输入错误,后部范围小于前部范围!!!', level=LOG_ERROR)
                    print('')
                    sys.exit()
                else:
                    for gen_port in range(port_start, port_end + 1):
                        ports.append(gen_port)
            else:
                ports.append(port_string)
    return ports


def init_input_target(input_target, input_ports, input_proto):
    # 读取用户输入的URL和目标文件参数
    if isinstance(input_target, str):
        input_target = [input_target]

    targets = []
    if isinstance(input_target, list):
        for target in input_target:
            if file_is_exist(target):
                targets = read_file_to_list(file_path=target, de_strip=True, de_weight=True, de_unprintable=True)
            else:
                if "://" not in target and ("\\" in target or "/" in target or str(target).endswith(".txt")):
                    output(f"[!] 目标文件路径不存在 {target}", level=LOG_ERROR)
                    exit()
                else:
                    targets.append(target)
    #  去重输入目标
    targets = list(dict.fromkeys(targets))

    # 解析用户输入的端口号参数
    if isinstance(input_ports, str):
        input_ports = [input_ports]
    ports = []
    if isinstance(input_ports, list):
        parse_ports = parse_input_ports(input_ports)
        ports.extend(parse_ports)
    #  去重输入端口
    ports = list(dict.fromkeys(ports))

    # 解析请求协议参数
    if isinstance(input_proto, str):
        input_proto = [input_proto]
    #  去重协议参数
    input_proto = list(dict.fromkeys(input_proto))

    # 组合协议、IP、端口
    gen_urls = []
    combinations = list(itertools.product(input_proto, targets, ports))
    for proto_, domain_, port_ in combinations:
        url = f"{proto_}://{domain_}:{port_}"
        gen_urls.append(url)

    #  去重URL结果参数
    gen_urls = list(dict.fromkeys(gen_urls))
    return gen_urls