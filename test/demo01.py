# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo01
# @Time:    2019-11-02 13:34:27
# @Desc:    测试requests请求

import json

from config.request_packaging import *


url = "https://kunpeng.csdn.net/ad/template/842?positionId=434&queryWord="
headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://kunpeng-sc.csdnimg.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
response = send_get_request(url, headers)
print(json.loads(response.text)['message'])


url1 = "https://recomm.cnblogs.com/api/v2/recomm/blogpost/reco"
headers1 = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "null",
    "Referer": "https://www.cnblogs.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
data = json.dumps({
    "itemId": "9145152",
    "itemTitle": "python3+requests：post请求四种传送正文方式（详解）"
})
response1 = send_data_request(url1, headers1, data)
print(json.loads(response1.text)[0]['title'])


url2 = "http://www.faxin.cn/lib/zyfl/GetNavContent.ashx"
headers2 = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "11",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "ASP.NET_SessionId=4twibqmofmiwr0zfhrq04mqr; Hm_lvt_a317640b4aeca83b20c90d410335b70f=1572666289,1572673941; Hm_lvt_a4967c0c3b39fcfba3a7e03f2e807c06=1572666289,1572673941; Hm_lpvt_a4967c0c3b39fcfba3a7e03f2e807c06=1572673941; Hm_lpvt_a317640b4aeca83b20c90d410335b70f=1572673958",
    "Host": "www.faxin.cn",
    "Origin": "http://www.faxin.cn",
    "Referer": "http://www.faxin.cn/lib/zyfl/zyflcontent.aspx?gid=A283151&libid=010101",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
data1 = {
    "gid": "A283151"
}
response2 = send_data_request(url2, headers2, data1)
print(response2.text)
