# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   IOJson
# @Time:    2019-12-18 22:05:23

import json


def write_json(file_path, data, write_mode='w'):
    """
    将数据写入json文件
    :param file_path: 文件路径
    :param data: 待写入数据
    :param write_mode: 写入模式
    :return: None
    """
    # 判断数据类型
    if type(data) is not dict:
        data = data.replace("None", "null").replace("'", "\"")
        data = json.loads(data)
    # 开始写入文件
    with open(file_path, write_mode, encoding='utf-8') as fj:
        # 注：ensure_ascii 禁止ascii编码   sort_keys 使用排序
        json.dump(data, fj, ensure_ascii=False, sort_keys=True, indent=4)


def read_json(file_path, read_mode='r'):
    """
    读取json文件数据
    :param file_path: 文件路径
    :param read_mode: 读取模式
    :return: 文件数据
    """
    with open(file_path, read_mode, encoding='utf-8') as rj:
        json_content = json.load(rj)
    return json_content


if __name__ == '__main__':
    filePath = r'../data/param.json'
    test = "{'code': 2000, 'data': {'access_key': 'BLZ40F8TCN3JNCL5MVY5', 'bucket': 'tos-cn-v-0000', 'delay_upload': 0, 'dns_info': None, 'edge_nodes': [{'access_key': 'DT2GDTBW6QYYT95M50B1', 'bucket': 'tos-cn-v-0000c001', 'dns_info': None, 'extra_param': 'vidc=lf&vts=1577344990181188584&host=tos-cu-hl.snssdk.com&region=CN&province=41&edge_node=hl&upload_mode=serial&file_size=4828943.000000&strategy=long_memory_filter&user_ip=219.155.95.239', 'oid': 'tos-cn-v-0000c001/99b7d8a701dc457d846905dd81cac684', 'token': 'YcsbyKSw:c02f5a45206afdf879a6d20e85427b79a41ea74283d6db760981270a6d766af6', 'tos_headers': {}, 'tos_host': 'tos-cu-hl.snssdk.com', 'tos_sign': 'DT2GDTBW6QYYT95M50B1:QIzh1Au2Lhzz6WD3Q5UpjJgaCds=:ZGVhZGxpbmU6IDE1Nzc0MzEzOTA=', 'tos_up_hosts': [], 'upload_mode': 'serial', 'vid': 'v02004a10000bo25vni0ifkj7ijk7vpg'}], 'extra_param': 'vidc=lf&vts=1577344990181188584&host=tos-hl-x.snssdk.com&region=CN&province=41&edge_node=hl&upload_mode=serial&file_size=4828943.000000&strategy=idc_filter&user_ip=219.155.95.239', 'oid': 'tos-cn-v-0000/022eac018f88482f814265fadff1c9e1', 'token': 'zxqgmGSf:e9fab19339f807bd36a081ee862ba3ca999276414d3e9920adade32802d88753', 'tos_headers': {}, 'tos_host': 'tos-hl-x.snssdk.com', 'tos_sign': 'BLZ40F8TCN3JNCL5MVY5:dOEZC6_-e5Azve7E4jhBQpz4Lj4=:ZGVhZGxpbmU6IDE1Nzc0MzEzOTA=', 'tos_up_hosts': [], 'trace_id': '33883902-0a7f-4ac3-8c40-6650bda7209f', 'upload_id': '18f9e914961d402db59c470dd371991f', 'upload_mode': 'serial', 'vid': 'v02004a10000bo25vni0ifkj7ijk7vpg'}, 'message': 'ok'}"
    write_json(filePath, data=test)
    read_json(filePath)
