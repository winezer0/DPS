# HttpDomainPortScan
 基于HTTP协议的域名端口扫描工具

通过组合URL进行http请求, 企图发现Cdn下，同域名的其他web端口


```
原理: 
0 CDN下可以开放转发域名的多个端口
1 输入 www.baidu.com 生成多个URL 如 https://www.baidu.com:8080 
2 访问  https://www.baidu.com:8080  可以访问表明端口开放.

python .\HDPS.py -h
usage: HDPS.py [-h] [-u TARGET [TARGET ...]] [-p PORTS [PORTS ...]] [-P PROTOS [PROTOS ...]] [-x PROXIES] [-t THREADS_COUNT] [-d] [-ru] [-rx] [-ss] [-sh]
               [-es EXCLUDE_STATUS [EXCLUDE_STATUS ...]] [-er EXCLUDE_REGEXP] [-rm REQ_METHOD] [-tt TIMEOUT] [-rt RETRY_TIMES]

_   _ ____  ____  ____

| | | |  _ \|  _ \/ ___| 
| |_| | | | | |_) \___ \
|  _  | |_| |  __/ ___) |
|_| |_|____/|_|   |____/


optional arguments:
  -h, --help            show this help message and exit
  -u TARGET [TARGET ...], --target TARGET [TARGET ...]
                        Specify the target URLs or Target File, Default is [target.txt]
  -p PORTS [PORTS ...], --ports PORTS [PORTS ...]
                        Specify the ports list or ports File, Default is [ports.txt]
  -P PROTOS [PROTOS ...], --protos PROTOS [PROTOS ...]
                        Specify the proto list or proto string, Default is [['http', 'https']]
  -x PROXIES            Specifies http|https|socks5 proxies, Default is [{}]
  -t THREADS_COUNT, --threads_count THREADS_COUNT
                        Specifies request threads, Default is [100]
  -d, --debug_flag      Specifies Display Debug Info, Default is [False]
  -ru, --random_useragent
                        Specifies Start Random useragent, Default is [False]
  -rx, --random_xff     Specifies Start Random XFF Header, Default is [False]
  -ss, --stream_mode    Shutdown Request Stream Mode, Default is [False]
  -sh, --history_exclude
                        Shutdown Exclude Request History, Default is [True]
  -es EXCLUDE_STATUS [EXCLUDE_STATUS ...]
                        Specified Response Status List Which Exclude, Default is [502, 400]
  -er EXCLUDE_REGEXP    Specified RE String When response matches the Str Excluded, Default is [None]
  -rm REQ_METHOD, --req_method REQ_METHOD
                        Specifies request method, Default is [get]
  -tt TIMEOUT, --timeout TIMEOUT
                        Specifies request timeout, Default is [10]
  -rt RETRY_TIMES, --retry_times RETRY_TIMES
                        Specifies request retry times, Default is [0]

Examples:
  批量扫描 target.txt
  python3 HDPS.py -u target.txt
  指定扫描 baidu.com
  python3 HDPS.py -u www.baidu.com

  其他控制细节参数可通过setting.py进行配置
  T00L Version: Ver 0.0.4 2023-05-27 04:44
```


