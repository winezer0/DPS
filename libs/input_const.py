import inspect

######################################################
# 默认参数相关
GB_BASE_DIR = ""
GB_RUN_TIME = ""
GB_VERSION = ""
GB_DEBUG_FLAG = ""

# 日志路径相关
GB_LOG_INFO_FILE = ""
GB_LOG_DEBUG_FILE = ""
GB_LOG_ERROR_FILE = ""

# 历史记录
GB_HISTORY_FORMAT = ""
GB_EXCLUDE_HISTORY = ""

# 结果文件
GB_RESULT_DIR = ""
GB_IGNORE_FORMAT = ""
GB_RESULT_FORMAT = ""

# 命中文件
GB_SAVE_HIT_RESULT = ""
GB_HIT_PORT_FILE = ""
######################################################
# 自定义输入参数相关
GB_TARGET = ""
GB_PORTS = ""
GB_PROTOS = ""
######################################################
GB_THREADS_COUNT = ""
GB_THREAD_SLEEP = ""
GB_TASK_CHUNK_SIZE = ""
######################################################
# 请求头设置
GB_REQ_HEADERS = ""
GB_DYNA_REQ_HOST = ""
GB_DYNA_REQ_REFER = ""
GB_RANDOM_UA = ""
GB_RANDOM_XFF = ""

GB_REQ_METHOD = ""
GB_PROXIES = ""
GB_REQ_BODY = ""
GB_STREAM_MODE = ""
GB_SSL_VERIFY = ""
GB_TIME_OUT = ""
GB_ALLOW_REDIRECTS = ""
GB_RETRY_TIMES = ""

# 排除状态码
GB_EXCLUDE_STATUS = ""
GB_EXCLUDE_REGEXP = ""
######################################################


# 实现自动更新全局变量名和对应值
def update_global_vars(startswith="GB_", require_blank=True, debug=False):
    # 修改所有全局变量名的值为变量名字符串
    # 当前本函数必须放置到本目录内才行

    def get_var_string(variable):
        # 自动根据输入的变量,获取变量名的字符串
        # 获取全局变量字典
        global_vars = globals()

        # 遍历全局变量字典
        for name, value in global_vars.items():
            if value is variable:
                # print(f"[*] global_vars <--> {variable} <--> {name} <--> {value}")
                return name

        # 获取局部变量字典
        local_vars = locals()
        # 遍历局部变量字典
        for name, value in local_vars.items():
            if value is variable:
                # print(f"[*] local_vars <--> {variable} <--> {name} <--> {value}")
                return name

        return None  # 如果未找到对应的变量名，则返回 None

    def get_global_var_names():
        # 获取本文件所有全局变量名称, 排除函数名等
        global_var_names = list(globals().keys())
        # 获取当前文件中定义的所有函数列表
        current_module = inspect.getmodule(inspect.currentframe())
        functions = inspect.getmembers(current_module, inspect.isfunction)
        function_names = [f[0] for f in functions]
        # 在本文件所有全局变量排除函数列表
        global_var_names = [name for name in global_var_names
                            if name not in function_names  # 排除内置函数名
                            and name.count("__") < 2  # 排除内置__name__等变量
                            and name != "inspect"  # 排除内置inspect包的变量
                            ]

        # 仅处理以 startswith 开头的变量
        if startswith:
            global_var_names = [name for name in global_var_names if name.startswith(startswith)]

        return global_var_names

    for variable_name in get_global_var_names():
        # 仅处理空变量
        if require_blank and globals()[variable_name]:
            if debug:
                print(f"跳过 Name:{variable_name} <--> Value: {globals()[variable_name]}")
            continue

        globals()[variable_name] = "NONE"
        globals()[variable_name] = get_var_string(globals()[variable_name])
        if debug:
            print(f"更新 Name:{variable_name} <--> Value: {globals()[variable_name]}")


# 自动更新变量的值为变量名字符串 # 必须放在末尾
update_global_vars(startswith="GB_", require_blank=True, debug=False)
