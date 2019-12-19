# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   time_calculation
# @Time:    2019-12-18 14:55:18
# @Desc:    time_calculation


select = []


def get_time_reverse_order_select():
    """
    生成时间(倒序生成，24小时)
    :return: 时间列表
    """
    hour = 23
    minute = 59
    while True:
        if hour == 0 and minute < 0:
            break
        if minute < 0:
            minute = 59
            hour -= 1

        if (len(str(hour)) < 2) and (len(str(minute)) < 2):
            start_datetime = "0{hour}:0{minute}:00".format(hour=hour, minute=minute)
        elif len(str(hour)) < 2:
            start_datetime = "0{hour}:{minute}:00".format(hour=hour, minute=minute)
        elif len(str(minute)) < 2:
            start_datetime = "{hour}:0{minute}:00".format(hour=hour, minute=minute)
        else:
            start_datetime = "{hour}:{minute}:00".format(hour=hour, minute=minute)
        select.append(start_datetime)
        minute -= 1
    print(len(select), select)
    return select


def get_time_positive_order_select():
    hour = 0
    minute = 0
    while True:
        if hour == 23 and minute > 59:
            break
        if minute > 59:
            minute = 0
            hour += 1

        if (len(str(hour)) < 2) and (len(str(minute)) < 2):
            time_str = "0{hour}:0{minute}:00".format(hour=hour, minute=minute)
        elif len(str(hour)) < 2:
            time_str = "0{hour}:{minute}:00".format(hour=hour, minute=minute)
        elif len(str(minute)) < 2:
            time_str = "{hour}:0{minute}:00".format(hour=hour, minute=minute)
        else:
            time_str = "{hour}:{minute}:00".format(hour=hour, minute=minute)
        select.append(time_str)
        minute += 1
    print(len(select), select)
    return select


if __name__ == '__main__':
    get_time_positive_order_select()    # 生成时间正序
    # get_time_reverse_order_select()     # 生成时间倒序
