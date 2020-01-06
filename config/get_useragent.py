# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   get_useragent
# @Time:    2019-05-09 17:50:10

from fake_useragent import UserAgent


def get_useragent():
    """
    获取单条useragent
    :return: user_agent
    """
    useragent = UserAgent(use_cache_server=False, cache=True, verify_ssl=False).random
    return useragent


if __name__ == '__main__':
    user_agent = get_useragent()
    print(user_agent)
