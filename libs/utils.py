#!/usr/bin/env python
# encoding: utf-8

import itertools
from urllib.parse import urlparse, urljoin

from libs.lib_args.input_const import *
from libs.lib_input_format.format_hosts import extract_host_from_host, extract_host_from_url, \
    classify_hosts
from libs.lib_input_format.format_input import load_targets
from libs.lib_input_format.format_ports import parse_ports, remove_80_443


def initialize_urls(config_dict):
    protos = load_targets(config_dict[GB_PROTOS])

    ports = load_targets(config_dict[GB_PORTS])
    ports = parse_ports(ports)

    targets = load_targets(config_dict[GB_TARGET])
    list_proto_host_port, list_host_port, list_ipv4, list_domain = classify_hosts(targets)
    urls = []
    if config_dict[GB_ALL_2_HOST]:
        hosts = []
        hosts.extend(list_ipv4)
        hosts.extend(list_domain)
        hosts.extend([extract_host_from_host(host_port) for host_port in list_host_port])
        hosts.extend([extract_host_from_url(proto_host_port) for proto_host_port in list_proto_host_port])
        hosts = list(dict.fromkeys(hosts))
        urls = group_proto_host_port(protos=protos, hosts=hosts, ports=ports)
    else:
        urls.extend(group_proto_host_port(protos=protos, hosts=list_ipv4, ports=ports))
        urls.extend(group_proto_host_port(protos=protos, hosts=list_domain, ports=ports))
        urls.extend(group_proto_host(protos=protos, hosts=list_host_port))
        urls.extend(list_proto_host_port)

    # 移除80 443端口后缀
    if config_dict[GB_REMOVE_80_443]:
        urls = [remove_80_443(url) for url in urls]

    # 更新path路径
    paths = load_targets(config_dict[GB_PATHS])
    if urls and paths:
        urls = combine_urls_and_paths(urls, paths, absolute=config_dict[GB_PATH_ABSOLUTE])

    urls = list(dict.fromkeys(urls))
    return urls


def group_proto_host_port(protos, hosts, ports):
    # 组合协议、域名、端口
    urls = []
    if protos and hosts and ports:
        group = list(itertools.product(protos, hosts, ports))
        urls = [f"{proto}://{host}:{port}" for proto, host, port in group]
        urls = list(dict.fromkeys(urls))
    return urls


def group_proto_host(protos, hosts):
    # 组合协议、域名
    urls = []
    if protos and hosts:
        group = list(itertools.product(protos, hosts))
        urls = [f"{proto}://{host}" for proto, host in group]
        urls = list(dict.fromkeys(urls))
    return urls


def combine_urls_and_paths(url_list, path_list, absolute=False):
    # 组合URl和路径
    url_path_tuples = list(itertools.product(url_list, path_list))
    url_path_list = []
    for url, path in url_path_tuples:
        if absolute:
            # 追加到根目录
            url_path_list.append(urljoin(url, f"/{str(path).lstrip('/')}"))
        else:
            # 追加到当前目录
            url_path_list.append(urljoin(url, f"./{str(path).lstrip('/')}"))
    # 去重URL
    url_path_list = list(set(url_path_list))
    return url_path_list


def result_rule_classify(hit_str_list, hit_port_file):
    # 分析扫描结果
    hit_classify = {hit_port_file: []}
    for url in hit_str_list:
        parsed_url = urlparse(url)
        port = parsed_url.port
        if port is None:
            port = 443 if parsed_url.scheme == 'https' else 80
        hit_classify[hit_port_file].append(port)
    return hit_classify
