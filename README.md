# DPS (DomainPortScan)

基于HTTP协议的域名端口扫描工具

通过组合 Host:Port 进行http请求, 企图发现Cdn下，同域名的其他web端口

### 原理: 
```
CDN下可以开放转发域名的多个端口, 可以越过一些CDN防御下无法解析真实域名，导致找不到端口资产的问题.

结构设计原因，仅建议用于常见HTTP端口扫描

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


