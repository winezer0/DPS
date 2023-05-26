from urllib.parse import urlparse

# 从URL中获取HOST:PORT
def get_host_port(url, replace_symbol=False):
    """
    从URL中获取HOST头部
    output(get_host_port('http://www.baidu.com.cn:8080/111/222/3.aspx?p=123')) #www.baidu.com.cn:8080
    """
    path_obj = urlparse(url)
    host_port = path_obj.netloc
    if replace_symbol:
        host_port = str(host_port).replace(":", "_")
    return host_port
