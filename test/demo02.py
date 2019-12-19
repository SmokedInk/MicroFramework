# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo02
# @Time:    2019-11-02 14:30:33

from request_packaging import *
from proxy_ip import get_proxies


proxies = get_proxies()
url = "https://www.google.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
rsp = send_get_request(url, headers, proxies)
print(rsp.status_code)
