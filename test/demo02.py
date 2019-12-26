# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo02
# @Time:    2019-11-02 14:30:33
# @Desc:    代理IP检测测试

from request_packaging import *
from proxy_ip import get_proxies


# proxies = get_proxies()
# 178.79.24.36:8080
host = "178.79.24.36:8080"
proxies = {
    "http": "http://" + host,
    "https": "http://" + host,
}
url = "http://httpbin.org/get"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
rsp = send_get_request(url, headers, proxies)
print(rsp.status_code)
print(rsp.content.decode())
