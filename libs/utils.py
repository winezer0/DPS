#!/usr/bin/env python
# encoding: utf-8

import itertools
from urllib.parse import urlparse

from libs.lib_args.input_const import *
from libs.lib_input_format.format_hosts import extract_host_from_host, extract_host_from_url, \
    classify_hosts
from libs.lib_input_format.format_input import load_targets
from libs.lib_input_format.format_ports import parse_ports, remove_80_443


def initialize_urls(config_dict, remove_common_port=True):
    protos = load_targets(config_dict[GB_PROTOS])

    ports = load_targets(config_dict[GB_PORTS])
    ports = parse_ports(ports)

    targets = load_targets(config_dict[GB_TARGET])
    list_proto_host_port, list_host_port, list_ipv4, list_host = classify_hosts(targets)
    urls = []
    if config_dict[GB_ALL_2_HOST]:
        hosts = []
        hosts.extend(list_ipv4)
        hosts.extend(list_host)
        hosts.extend([extract_host_from_host(host_port) for host_port in list_host_port])
        hosts.extend([extract_host_from_url(proto_host_port) for proto_host_port in list_proto_host_port])
        hosts = list(dict.fromkeys(hosts))
        urls = group_proto_host_port(protos=protos, hosts=hosts, ports=ports)
    else:
        urls.extend(group_proto_host_port(protos=protos, hosts=list_ipv4, ports=ports))
        urls.extend(group_proto_host_port(protos=protos, hosts=list_host, ports=ports))
        urls.extend(group_proto_host(protos=protos, hosts=list_host_port))
        urls.extend(list_proto_host_port)

    if remove_common_port:
        urls = [remove_80_443(url) for url in urls]

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
