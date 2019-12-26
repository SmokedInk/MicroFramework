# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   IOCsv
# @Time:    2019-11-07 21:33:59

import csv


def write_csv(file_path, column_headline, data_text, write_mode='w'):
    """
    写入CSV文件数据
    :param file_path: 文件路径
    :param column_headline: 列标题
    :param data_text: 待写入数据
    :param write_mode: 写入模式
    :return: None
    """
    # 创建CSV文件       newline=""此参数不加会出现空行
    csv_file = open(file_path, write_mode, encoding="utf-8", newline="")
    # 创建写入的对象   dialect=""此参数表示的文件的类型
    writer = csv.writer(csv_file)
    # 写入单行用writerow(可用于写入行标题)
    writer.writerow(column_headline)
    # 写入多行用writerows
    writer.writerows(data_text)
    # 关闭文件
    csv_file.close()


def read_csv(file_path, read_mode='r'):
    """
    读取CSV文件数据
    :param file_path: 文件路径
    :param read_mode: 读取模式
    :return: 文件内容
    """
    # 读取CSV文件
    csv_file = open(file_path, read_mode, encoding="utf-8")
    # 获取文件数据
    reader = csv.reader(csv_file)
    csv_values = []
    for csv_val in reader:
        csv_values.append(csv_val)
    return csv_values


if __name__ == '__main__':
    filePath = r"../data/csvTest.csv"
    data_01 = ["index", "a_name", "b_name"]
    data_02 = [[1, "a", "b"], [2, "c", "d"], [3, "e", "f"]]
    # write_csv(filePath, data_01, data_02)
    read_csv(filePath)
