#!/usr/bin/env python
# encoding: utf-8
import re
from urllib.parse import urlparse


def is_http_url(string):
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, string) is not None


def is_valid_url(target):
    parsed_url = urlparse(target)
    return parsed_url.scheme != '' and parsed_url.netloc != ''


def is_host_port(string):
    pattern = r'^[a-zA-Z0-9.-]+:\d+$'
    return re.match(pattern, string) is not None


def is_ipv4(string):
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(domain_pattern, string) is not None


def is_domain(string):
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(domain_pattern, string) is not None


def extract_host_from_url(url):
    # 提取URL中的HOST部分,不包含端口号
    parsed_url = urlparse(url)
    # parsed_url.hostname 返回的结果不包含端口号。只返回URL中的主机名部分。
    host = parsed_url.hostname
    return host


def extract_host_from_host(host):
    # 提取host中的HOST部分,不包含端口号
    # parsed_url.hostname 返回的结果不包含端口号。只返回URL中的主机名部分。
    if ":" in host:
        host = str(host).split(":", 1)[0]
    return host


def classify_hosts(hosts):
    # 将目标分类为  HOST, HOST_PORT, PROTO_HOST_PORT
    list_host = []
    list_ipv4 = []
    list_host_port = []
    list_proto_host_port = []
    # list_error = []
    for host in hosts:
        if is_http_url(host):
            list_proto_host_port.append(host)
        elif is_host_port(host):
            list_host_port.append(host)
        elif is_ipv4(host):
            list_ipv4.append(host)
        elif is_domain(host):
            list_host.append(host)
        else:
            # list_error.append(target)
            print(f"[-] 发现错误格式的输入数据:{host}")

    # 去重输入目标
    list_proto_host_port = list(dict.fromkeys(list_proto_host_port))
    list_host_port = list(dict.fromkeys(list_host_port))
    list_host = list(dict.fromkeys(list_host))
    list_ipv4 = list(dict.fromkeys(list_ipv4))
    return list_proto_host_port, list_host_port, list_ipv4, list_host


def remove_80_443(url):
    parsed_url = urlparse(url)
    if parsed_url.port in [80,443]:
        return f"{parsed_url.scheme}://{parsed_url.hostname}"
    return url
