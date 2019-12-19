# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   date_calculation
# @Time:    2019-12-18 14:50:15
# @Desc:    date_calculation

import re


def get_select(start_date, date_num):
    """
    生成日期(顺序生成)
    :param start_date: 起始日期
    :param date_num: 生成日期数量
    :return: 日期列表
    """
    select = list()

    def combination_date(year, mon, day):
        """
        拼接日期
        :param year: 年
        :param mon: 月
        :param day: 日
        :return: None
        """
        if len(str(mon)) == 1 and len(str(day)) == 1:
            date = f'{year}-0{mon}-0{day}'
        elif len(str(mon)) == 1:
            date = f'{year}-0{mon}-{day}'
        elif len(str(day)) == 1:
            date = f'{year}-{mon}-0{day}'
        else:
            date = f'{year}-{mon}-{day}'
        select.append(date)

    mon_01 = [1, 3, 5, 7, 8, 10, 12]
    mon_02 = [4, 6, 9, 11]
    year = int(re.findall(r'^(\d+)-', start_date)[0])
    mon = int(re.findall(r'-(\d+)-', start_date)[0])  # 2
    day = int(re.findall(r'-(\d+)$', start_date)[0])  # 14
    for i in range(date_num):
        if mon in mon_01:
            combination_date(year, mon, day)
            if day == 31:
                mon += 1
                day = 0
            day += 1
        elif mon in mon_02:
            combination_date(year, mon, day)
            if day == 30:
                mon += 1
                day = 0
            day += 1
        else:
            combination_date(year, mon, day)
            if day == 28 and year % 4 != 0:
                mon += 1
                day = 0
            elif day == 29 and year % 4 == 0:
                mon += 1
                day = 0
            day += 1
        if mon == 12 and day == 31:
            combination_date(year, mon, day)
            year += 1
            mon = 1
            day = 1
    print(select)
    return select


if __name__ == '__main__':
    start_date = '2019-05-01'
    date_num = 260
    get_select(start_date, date_num)
