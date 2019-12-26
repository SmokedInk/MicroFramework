# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo_03
# @Time:    2019-11-07 16:04:02
# @Desc:    使用代理下载头条文章

import re
import requests

from config.proxy_ip import get_proxies


item = dict()

"""
&quot;  --->    '
\u003C  --->    <
\u002F  --->    /
\u003E  --->    >
&#x3D;  --->    =
\       --->    
.slice(6, -6)   --->    
"""


def repl(title, content):
    title = title.replace("&quot;", "'")
    new_title = title.replace("\\'", '"')[1:-1]
    content = content.replace("&quot;", "'")
    content = content.replace("\\u003C", "<")
    content = content.replace("\\u003E", ">")
    content = content.replace("\\u002F", "/")
    content = content.replace("&#x3D;", "=")
    new_content = content.replace("\\", "")[1:-1]
    return new_title, new_content


# url = "https://www.toutiao.com/item/6752768901420941831/"
# url = "https://www.toutiao.com/i6754122541146571277/"
url = "https://www.toutiao.com/i6745043734817145347/"
headers = {
    "accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "csrftoken=6574c6c6a1e933c67c2405f122b8936d; tt_webid=6756113976880580110; __tasessionId=dneuohee11573098757329",
    "referer": "https://www.toutiao.com/i6752768901420941831/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, proxies=get_proxies())
    data = response.content.decode()
except Exception as err:
    data = ""
    print("。。。。。。。。。。", err)
# print(data)
article_title = re.findall(r"title: '(.*?)'", data)[0]
article_content = re.findall(r"content: '(.*?)'", data)[0]
title, content = repl(article_title, article_content)
# print([content])
content = content.split("</p>")
text = ""
for i in content:
    # print([i])
    if "img src" in i:
        try:
            i = re.findall("img (.*?) img_width", i)[0]
            text += ("<p>" + "<img {}>".format(i) + "</p>").strip()
        except Exception as err:
            print(err)
            continue
        # print(i)
    else:
        try:
            i = re.sub(r'</?\w+[^>]*>','',i).strip()
            # print(">>>>", [i])
            if re.findall(r"[\u4E00-\u9FA5]+", i):
                text += ("<p>" + i + "</p>")
        except Exception as err:
            print(err)
            continue
    # print("---------------------------------------------------------")
# print(text)
item['title'] = title
item['content'] = text
item['sort'] = "娱乐"   # "星座"
item['category'] = "美国电影"   # "星座"
print(item)
