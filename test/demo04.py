# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo04
# @Time:    2019-11-27 13:06:43
# @Desc:    demo04

import requests

"""

"""


url = "https://www.zdaye.com/dayProxy.html"
# url = "https://www.zdaye.com/dayProxy/ip/317177.html"
headers = {
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # 'Host':'www.zdaye.com',
    # 'Referer':'https://www.zdaye.com/',
    # 'Cookie':'acw_tc=781bad2915748179800455431e287ec01eddfb1fd4c599bba81b0ce5946941; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1574817982; acw_sc__v3=5dddd0c11ab13fa1fa7b4895d0c589961e85ea7e; acw_sc__v2=5dddd2682d2a4a3310426a7ffea0a47bb5fcd4ca; ASPSESSIONIDCUSAQBDS=BHDKPBOCOMNEFINCCLOPLKAI; __tins__16949115=%7B%22sid%22%3A%201574817982327%2C%20%22vd%22%3A%206%2C%20%22expires%22%3A%201574820302057%7D; __51laig__=6; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1574818502'
}
rsp = requests.get(url, headers=headers, verify=False).content.decode()
print(rsp)
