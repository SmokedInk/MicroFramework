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
    "http://httpbin.org/get",
    "http://www.89ip.cn/check.html",
    "http://icanhazip.com/"
]
headers = {
    "User-Agent": get_useragent()
}

random_num = random.random()

ZDY_cookie = 'acw_tc=76b20f7215770022478591548e14600a8c98c3a192bfaf540f3125c01eac0b; __51cke__=; Hm_lvt_80f407a85cf0bc32ab5f9cc91c15f88b=1577002249; acw_sc__v2=5dff255b43eea97064d05582bcdb249f33e2595e; ASPSESSIONIDSEQRCRBQ=BKFPCPIDOBCEOCPFPGDBAGOM; __tins__16949115=%7B%22sid%22%3A%201577002248841%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201577004146820%7D; __51laig__=2; acw_sc__v3=5dff256bae9a58773595b64fb69a699efb40c66b; Hm_lpvt_80f407a85cf0bc32ab5f9cc91c15f88b=1577002347'

# 检测通道ID
CHANNEL_ID = 1

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
    ip_list = list()
    ip_url = f"http://www.89ip.cn/index_1.html"
    ip_rsp = send_get_request(ip_url, headers).content.decode()
    etree_html = etree.HTML(ip_rsp)
    ips = etree_html.xpath("//table[@class='layui-table']//tr/td[1]/text()")
    ports = etree_html.xpath("//table[@class='layui-table']//tr/td[2]/text()")
    locations = etree_html.xpath("//table[@class='layui-table']//tr/td[3]/text()")
    operators = etree_html.xpath("//table[@class='layui-table']//tr/td[4]/text()")
    for ip, port, location, operator in zip(ips, ports, locations, operators):
        # print(f"{ip.strip()}:{port.strip()}", location.strip(), operator.strip())
        ip_list.append((f"{ip.strip()}:{port.strip()}", location.strip(), operator.strip()))
    return ip_list


def get_kuaidaili_ip_list():
    """
    获取快代理免费IP
    :return: 代理列表
    """
    ip_list = list()
    ip_index_url = f"https://www.kuaidaili.com/free/inha/1/"
    ip_index_rsp = send_get_request(ip_index_url, headers).content.decode()
    etree_obj = etree.HTML(ip_index_rsp)
    ips = etree_obj.xpath("//table/tbody/tr/td[1]/text()")
    ports = etree_obj.xpath("//table/tbody/tr/td[2]/text()")
    places = etree_obj.xpath("//table/tbody/tr/td[5]/text()")
    for ip, port, place in zip(ips, ports, places):
        place_split = place.split(" ")
        location = " ".join(place_split[:-1])
        operator = place_split[-1]
        # print(f"{ip}:{port}", location, operator)
        ip_list.append((f"{ip}:{port}", location, operator))
    return ip_list


def get_zdaye_ip_list():
    """
    获取站大爷免费IP
    :return: 代理列表
    """
    ip_articles_url = "https://www.zdaye.com/dayProxy.html"
    headers['Cookie'] = ZDY_cookie
    ip_articles_rsp = send_get_request(ip_articles_url, headers, verify=False).content.decode()
    etree_text = etree.HTML(ip_articles_rsp)
    ip_article_url = "https://www.zdaye.com" + etree_text.xpath("//div[@class='thread_item'][1]/div/h3/a/@href")[0]
    print(ip_article_url)
    ip_rsp = send_get_request(ip_article_url, headers, verify=False).content.decode()
    rest = etree.HTML(ip_rsp)
    ips = rest.xpath('//div[@class="cont"]/text()')
    ip_list = []
    for ip in ips:
        ip_str = ip.split("@")
        ip = ip_str[0]
        location = re.findall(r"](.*?) ", ip_str[1])[0]
        operator = re.findall(r" (.*?)$", ip_str[1])[0]
        ip_list.append((ip, location, operator))
        print(ip, location, operator)
    return ip_list


def detection_channel_01(host_info):
    proxies = {
        "http": "http://" + host_info[0],
        "https": "https://" + host_info[0],
    }
    try:
        rsp = send_get_request(detection_url_list[0], headers, proxies)
        ip = host_info[0].split(':')[0]
        if rsp.status_code == 200 and ip in rsp.content.decode():
            print("{}-->通过检测，检测状态：{}".format(host_info[0], "连接正常"))
            ip_result = (host_info[0], "连接正常", host_info[1], host_info[2], get_now_time())
            proxy_list.append(ip_result)
            normal_ip_list.append((get_now_time(), host_info[0]))
        else:
            print("{}-->未通过检测，检测状态：{}".format(host_info[0], "无法连接"))
            failure_ip_list.append((get_now_time(), host_info[0]))
    except Exception as err:
        print("{}-->通过检测失败, 错误为: {}".format(host_info[0], err))
        failure_ip_list.append((get_now_time(), host_info[0]))


def detection_channel_02(host_info):
    detection_data = {
        "proxy": host_info[0],
        "type": 1
    }
    detection_rsp = send_data_request(detection_url_list[0], headers, detection_data)
    try:
        if detection_rsp:
            status = re.findall("代理状态：([\u4e00-\u9fa5]+)", detection_rsp.text)[0]
            if "无法连接" not in detection_rsp.text:
                results_str = detection_rsp.text.split("<br>")
                effectiveness = results_str[0].split("：")[1]
                print("{}-->通过检测，检测状态：{}".format(host_info[0], status))
                ip_result = (host_info[0], effectiveness, host_info[1], host_info[2], get_now_time())
                proxy_list.append(ip_result)
                normal_ip_list.append((get_now_time(), host_info[0]))
            else:
                print("{}-->未通过检测，检测状态：{}".format(host_info[0], status))
                failure_ip_list.append((get_now_time(), host_info[0]))
        else:
            print("检测失败")
    except AttributeError as err:
        print(err)


def ip_detection(host_info, channel_id):
    """
    代理IP检测
    :param host_info: 待检测代理IP信息
    :param channel_id: 通道id
    :return: None
    """
    if channel_id == 1:
        detection_channel_01(host_info)
    elif channel_id == 2:
        detection_channel_02(host_info)
    else:
        print("暂未开放")


def new_ip_detection():
    """
    新增代理IP检测
    :return: None
    """
    proxy_list.clear()
    ip_info_list = get_89ip_ip_list()
    threads = []
    for ip_info in ip_info_list:
        ip_detection(ip_info, CHANNEL_ID)
        time.sleep(random_num)
    #     th = threading.Thread(target=ip_detection, args=(ip_info, CHANNEL_ID,))
    #     th.setDaemon(True)
    #     th.start()
    #     threads.append(th)
    # for t in threads:
    #     t.join()
    create_many(proxy_list)


def sql_ip_detection():
    """
    数据库已有IP检测
    :return: None
    """
    ip_list = select_total()
    threads = []
    for ip_info in ip_list:
        ip_detection(ip_info, CHANNEL_ID)
        time.sleep(random_num)
    #     th = threading.Thread(target=ip_detection, args=(ip_info, CHANNEL_ID,))
    #     th.setDaemon(True)
    #     th.start()
    #     threads.append(th)
    # for t in threads:
    #     t.join()
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
        "https": "https://" + host,
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
    # get_89ip_ip_list()
    # get_zdaye_ip_list()
