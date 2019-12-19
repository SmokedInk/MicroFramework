# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   get_proxies
# @Time:    2019-05-09 18:45:10

import re
import time
import random
import threading
from lxml import etree

from config.request_packaging import *
from config.sqllite3_operation import *
from config.get_useragent import get_useragent

"""
代理网站
    http://www.data5u.com/  无忧
    http://www.89ip.cn/check.html   89ip
    https://www.zdaye.com/dayProxy/ip/{num}.html    站大爷
    
IP验证网站
    http://icanhazip.com/
    http://www.89ip.cn/check.html
    http://httpbin.org/get
"""

# 检测网站URL
detection_url_list = [
    "http://www.89ip.cn/check.html",
    "http://icanhazip.com/",
    "http://httpbin.org/get"
]
detection_url = random.sample(detection_url_list, 1)[0]
headers = {
    "User-Agent": get_useragent()
}

proxy_list = []
failure_ip_list = []
normal_ip_list = []


def get_now_time():
    """
    获取当前时间
    :return: 当前时间字符串
    """
    c_time = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", c_time)
    return now_time


def get_89ip_ip_list():
    """
    获取IP代理
    :return: 代理列表
    """
    ip_url = "http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp="
    ip_rsp = send_get_request(ip_url, headers)
    ip_text = ip_rsp.text.replace("\n", "")

    # 匹配数据
    ips = re.findall(";</script>(.*?)高效", ip_text)[0]
    ip_list = ips.split("<br>")[:-1]
    return ip_list


def get_zdaye_ip_list():
    """
    获取站大爷IP代理
    :return: 代理列表
    """
    ip_articles_url = "https://www.zdaye.com/dayProxy.html"
    ip_articles_rsp = send_get_request(ip_articles_url, headers, verify=False).content.decode()
    etree_text = etree.HTML(ip_articles_rsp)
    ip_article_url = "https://www.zdaye.com" + etree_text.xpath("//div[@class='thread_item'][1]//h3/a/@href")[0]

    ip_rsp = send_get_request(ip_article_url, headers).content.decode()
    print(ip_rsp)
    rest = etree.HTML(ip_rsp)
    ips = rest.xpath('//div[@class="cont"]/text()')
    print(ips)
    ip_list = []
    for ip in ips:
        print(ip)
        ip = ip.split("@")
        ip_list.append(ip)
        print(ip)
    print(ip_list)


def ip_detection(ip):
    """
    代理IP检测
    :param ip: 待检测代理IP
    :return: None
    """
    detection_data = {
        "proxy": ip,
        "type": 1
    }
    detection_rsp = send_data_request(detection_url_list[0], headers, detection_data)
    try:
        if detection_rsp:
            status = re.findall("代理状态：([\u4e00-\u9fa5]+)", detection_rsp.text)[0]
            if "无法连接" not in detection_rsp.text:
                results_str = detection_rsp.text.split("<br>")
                effectiveness = results_str[0].split("：")[1]
                location = results_str[1].split("：")[1]
                operator = results_str[2].split("：")[1]
                print("{}-->通过检测，检测状态：{}".format(ip, status))
                ip_result = (ip, effectiveness, location, operator, get_now_time())
                proxy_list.append(ip_result)
                normal_ip_list.append((get_now_time(), ip))
            else:
                print("{}-->未通过检测，检测状态：{}".format(ip, status))
                failure_ip_list.append((get_now_time(), ip))
        else:
            print("检测失败")
    except AttributeError as err:
        print(err)


def new_ip_detection():
    """
    新增代理IP检测
    :return: None
    """
    ip_list = get_89ip_ip_list()
    threads = []
    for host in ip_list:
        th = threading.Thread(target=ip_detection, args=(host,))
        th.setDaemon(True)
        th.start()
        threads.append(th)
    for t in threads:
        t.join()
    create_many(proxy_list)


def sql_ip_detection():
    """
    数据库已有IP检测
    :return: None
    """
    ip_list = select_total()
    threads = []
    for host in ip_list:
        th = threading.Thread(target=ip_detection, args=(host,))
        th.setDaemon(True)
        th.start()
        threads.append(th)
    for t in threads:
        t.join()
    ip_desc_dict = {
        "normal_ip_list": normal_ip_list,
        "failure_ip_list": failure_ip_list
    }
    update_many(ip_desc_dict)
    count = select_count()
    if count <= 10:
        print("可用IP数量不足，开始补充IP...")
        new_ip_detection()
        print("清理不可用IP...")
        delete_many()


def get_proxies():
    """
    构造请求代理格式
    :return: 构造好的代理
    """
    ip_list = find_query()
    host = random.sample(ip_list, 1)[0]
    print("当前代理IP为：{proxies}".format(proxies=host))
    proxies = {
        "http": "http://" + host,
        "https": "http://" + host,
    }
    return proxies


def automation():
    """
    自动化更新代理池
    :return: None
    """
    count = 0
    while True:
        if count == 20:
            break
        sql_ip_detection()
        count += 1
        time.sleep(5 * 60)


if __name__ == '__main__':
    # automation()
    # new_ip_detection()
    sql_ip_detection()
    # get_zdaye_ip_list()
