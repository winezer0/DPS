def check_dict_update_eq(old_dict, new_dict):
    """
    通过循环相等判断 检查新旧字典的相同键的值更新
    :param old_dict:
    :param new_dict:
    :return:
    """
    update_dict = {}
    for same_key, old_value in old_dict.items():
        if same_key in new_dict:
            new_value = new_dict[same_key]
            if old_value != new_value:
                # print(f"Key: {same_key} | value: {old_value} --> {new_value}")
                update_dict[same_key] = new_value
    return update_dict


def check_dict_update_zip(old_dict, new_dict):
    """
    使用字典推导式和 zip() 函数找到相同键但不同值的项
    :param old_dict:
    :param new_dict:
    :return:
    """
    update_dict = {}
    different_values = {
        same_key: (old_value, new_value)
        for same_key, old_value, new_value in zip(old_dict.keys(), old_dict.values(), new_dict.values())
        if old_value != new_value
    }

    # 输出相同键但不同值的项
    for same_key, (old_value, new_value) in different_values.items():
        # print(f"Key: {same_key} | value: {old_value} --> {new_value}")
        update_dict[same_key] = new_value
    return update_dict


def check_keys_in_list(params_dict, allowed_keys):
    """
    查找参数字典中是否存在非预期的参数
    :param params_dict: 参数字典
    :param allowed_keys: 运行的参数
    :return:
    """
    unexpected = [key for key in params_dict.keys() if key not in set(allowed_keys)]
    return unexpected


if __name__ == '__main__':
    dict1 = {'AAA': 1, 'BBB': 2, 'CCC': 3}
    dict2 = {'AAA': 1, 'BBB': 4, 'CCC': 3}
    check_dict_update_eq(dict1, dict2)
    check_dict_update_zip(dict1, dict2)
