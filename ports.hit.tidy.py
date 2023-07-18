from libs.lib_file_operate.file_write import write_path_list_to_frequency_file

if __name__ == '__main__':
    # 手动整理命令端口文件
    file_path = r"C:\Users\WINDOWS\GithubProject\DPS\ports.hit"
    write_path_list_to_frequency_file(file_path=file_path,
                                      path_list=[],
                                      encoding='utf-8',
                                      frequency_symbol="<-->",
                                      annotation_symbol="###",
                                      hit_over_write=True)
