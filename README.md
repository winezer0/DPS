# DPS (DomainPortScan)

支持基于HTTP协议的(URL访问|HOST:PORT|IP访问|域名访问|域名端口检测)工具

```
原始目标：
    1、从URL|Domain|IP:PORT|Domain:PORT|等格式提取出 IP|Domain
    2、统一进行http协议端口扫描, 企图发现Cdn下，同域名的其他web端口

衍生功能：
    支持 URL 格式存活检测
    支持 Domain|IP:PORT|Domain:PORT 格式存活检测
    支持 IP C段 IP|IP 范围  格式存活检测  
    支持 自定义PATHS路径 

格式示例： 
    www.baidu.com
    www.baidu.com:8888
    https://www.baidu.com
    1.1.1.1/28 | 1.1.1.1-100 | 1.1.1.1-1.1.1.100
```


### 原理: 
```
CDN下可以开放转发域名的多个端口, 
可以越过一些CDN防御下无法解析真实域名，导致找不到端口资产的问题.

结构设计原因，仅建议用于常见HTTP端口扫描，不建议用于全端口扫描
```
### 实现：
```
1 输入 www.baidu.com 生成多个URL 如 https://www.baidu.com:8080 
2 访问 https://www.baidu.com:8080 可以访问表明端口开放.
```

### 使用：
```
python .\HDPS.py -h
```


