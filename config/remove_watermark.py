# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   remove_watermark
# @Time:    2019-11-28 11:56:40
# @Desc:    remove_watermark

import subprocess


def cut(file_path, x, y, w, h, save_path):
    subprocess.call(f'ffmpeg -i {file_path} -filter_complex "delogo=x={x}:y={y}:w={w}:h={h}:show=0" {save_path}')


if __name__ == '__main__':
    file_path = r"D:\ObjectCode\data\pic\py.jpg"
    save_path = r"D:\ObjectCode\data\pic\py_cut_01.jpg"
    x = ""
    y = ""
    w = ""
    h = ""
    cut(file_path, x, y, w, h, save_path)
