import itertools
import sys

from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_log_print.logger_printer import output, LOG_ERROR, LOG_INFO
from urllib.parse import urlparse


def result_rule_classify(hit_str_list, hit_port_file):
    # 分析扫描结果
    hit_classify = {hit_port_file: []}
    for url in hit_str_list:
        port = urlparse(url).port
        hit_classify[hit_port_file].append(port)
    return hit_classify


def init_input_domain(input_target):
    # 读取用户输入的URL和目标文件参数
    if isinstance(input_target, str):
        input_target = [input_target]

    targets = []
    if isinstance(input_target, list):
        for target in input_target:
            if file_is_exist(target):
                targets = read_file_to_list(file_path=target, de_strip=True, de_weight=True, de_unprintable=True)
            else:
                targets.append(target)

    # 如果用户输入的是url,就进行host提取
    targets = [extract_host(target) if is_valid_url(target) else target for target in targets]

    # 检查提取过后的域名格式是否正确
    for target in targets:
        if "\\" in target or "/" in target:
            print(f"[*] 域名 [{target}] 输入错误或目标文件路径不存在!!!")
            exit()

    #  去重输入目标
    targets = list(dict.fromkeys(targets))

    return targets


def init_input_proto(input_proto):
    # 解析请求协议参数
    if isinstance(input_proto, str):
        input_proto = [input_proto]
    #  去重协议参数
    input_proto = list(dict.fromkeys(input_proto))
    return input_proto


def init_input_ports(input_ports):
    # 初始化输入端口
    ports = []

    def parse_input_ports(port_str_list):
        # 解析输入的端口字符串列表
        port_list = []
        for port_str in port_str_list:
            if file_is_exist(port_str):
                lists = read_file_to_list(file_path=port_str, de_strip=True, de_weight=True, de_unprintable=True)
                port_list.extend(lists)
            else:
                if ',' in str(port_str):
                    output(f"[!] 错误输入{port_str} Ports不支持逗号,请使用[空格]和[-]限定范围! 如:8080 80-443", level=LOG_ERROR)
                    exit()
                elif '-' in str(port_str):
                    port_start = int(port_str.split("-")[0].strip())
                    port_end = int(port_str.split("-")[1].strip())
                    if port_end < port_start:
                        output(f'[!] 端口 {port_str} 范围格式输入错误,后部范围小于前部范围!!!', level=LOG_ERROR)
                        print('')
                        sys.exit()
                    else:
                        for gen_port in range(port_start, port_end + 1):
                            port_list.append(gen_port)
                else:
                    port_list.append(port_str)
        return port_list

    if isinstance(input_ports, str):
        input_ports = [input_ports]

    if isinstance(input_ports, list):
        parse_ports = parse_input_ports(input_ports)
        ports.extend(parse_ports)

    # 去重输入端口
    ports = list(dict.fromkeys(ports))
    return ports


def gen_url_list(proto_list, domain_list, port_list):
    # 组合协议、域名、端口
    gen_urls = []
    combinations = list(itertools.product(proto_list, domain_list, port_list))
    for proto_, domain_, port_ in combinations:
        url = f"{proto_}://{domain_}:{port_}"
        gen_urls.append(url)

    #  去重URL结果参数
    gen_urls = list(dict.fromkeys(gen_urls))
    return gen_urls


def exclude_history_record(target_list, history_file):
    # 排除历史扫描记录
    if file_is_exist(history_file):
        output(f"[*] 输入目标URL: {len(target_list)}个", level=LOG_INFO)
        accessed_url_list = read_file_to_list(file_path=history_file, de_weight=True, de_unprintable=False)
        target_list = list(set(target_list) - set(accessed_url_list))
        output(f"[*] 历史访问URL: {len(accessed_url_list)}个", level=LOG_INFO)
        output(f"[*] 剔除剩余URL: {len(target_list)}个", level=LOG_INFO)
    return target_list


def extract_host(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    return host


def is_valid_url(target):
    parsed_url = urlparse(target)
    return parsed_url.scheme != '' and parsed_url.netloc != ''
