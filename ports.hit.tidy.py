from libs.lib_file_operate.rw_freq_file import write_list_to_freq_file

if __name__ == '__main__':
    # 手动整理命令端口文件
    file_path = r"ports.hit"
    write_list_to_freq_file(file_path=file_path,
                            path_list=[],
                            encoding='utf-8',
                            freq_symbol="<-->",
                            anno_symbol="###")
