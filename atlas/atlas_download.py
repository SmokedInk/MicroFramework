# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   demo_07
# @Time:    2019-11-07 10:53:00

import re
import requests
from lxml import etree

from config.proxy_ip import get_proxies

# 18637305329
# cbs86....
item = dict()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}


def repl(title, content):
    new_title = title.replace("&quot;", "'")[1:-1]
    content = content.replace("&quot;", "'")
    content = content.replace("\\u003C", "<")
    content = content.replace("\\u003E", ">")
    content = content.replace("\\u002F", "/")
    content = content.replace("&#x3D;", "=")
    new_content = content.replace("\\", "")[1:-1]
    return new_title, new_content


def touTiao_down():
    url = "https://www.toutiao.com/item/6752768901420941831/"
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
    article_title = re.findall(r"title: '(.*?)'", data)[0]
    article_content = re.findall(r"content: '(.*?)'", data)[0]
    title, content = repl(article_title, article_content)
    content = content.split("</p>")
    text = ""
    for i in content:
        if "img src" in i:
            try:
                i = re.findall("img (.*?) img_width", i)[0]
                text += ("<p>" + "<img {}>".format(i) + "</p>").strip()
            except:
                continue
        else:
            try:
                i = re.sub(r'</?\w+[^>]*>','',i).strip()
                if re.findall(r"[\u4E00-\u9FA5]+", i):
                    text += ("<p>" + i + "</p>")
            except:
                continue
    item['title'] = title
    item['content'] = text
    item['sort'] = "娱乐"   # "星座"
    item['category'] = "美国电影"   # "星座"
    print(item)


def baiJia_down():
    url = r"https://mbd.baidu.com/newspage/data/landingshare?context=%7B%22nid%22%3A%22news_9814050930469143527%22%2C%22sourceFrom%22%3A%22bjh%22%7D"
    try:
        response = requests.get(url, headers=headers, proxies=get_proxies())
        data = response.content.decode()
    except IOError as err:
        data = ""
        print(err)
    text = ""
    try:
        html = etree.HTML(data)
        title = html.xpath("//h1[@class='titleSize']/text()")[0]
        p = html.xpath("//div[@class='mainContent']/*")
        for i in p:
            p_str = etree.tostring(i, encoding='utf-8')
            content = str(p_str, 'utf-8')
            if "contentMedia" in content:
                cont = re.findall("img (.*?) data-index", content)[0]
                cont = cont.replace("&amp;", "&").strip()
                text += ("<p>" + "<img {}>".format(cont) + "</p>")
            else:
                cont = re.sub(r'</?\w+[^>]*>', '', content).strip()
                if re.findall(r"[\u4E00-\u9FA5]+", cont):
                    text += ("<p>" + cont + "</p>")
    except:
        print("11")
    print(text)
    item['title'] = title
    item['content'] = text
    item['sort'] = "娱乐"  # "星座"
    item['category'] = "美国电影"  # "星座"
    print(item)


def yidian_down():
    """
    一点号/一点资讯
    :return:
    """
    url = r"http://www.yidianzixun.com/article/0NjAwRXm"
    # url = r"http://www.yidianzixun.com/article/0NiI34zd"
    try:
        response = requests.get(url, headers=headers, proxies=get_proxies())
        data = response.content.decode()
    except Exception as err:
        data = ""
        print("。。。。。。。。。。", err)
    if data:
        html = etree.HTML(data)
        title = html.xpath("//div[@class='left-wrapper']/h2/text()")[0]
        child_list = html.xpath("//div[@id='imedia-article']/*")
        text = ""
        try:
            for i in child_list:
                p_str = etree.tostring(i, encoding='utf-8')
                content = str(p_str, 'utf-8')
                if content and "a-image" in content:
                    cont = re.findall('img src="(.*?)"/', content)[0]
                    text += ("<p>" + "<img src=http:{}>".format(cont) + "</p>").strip()
                    if re.findall(r"</div>[\u4E00-\u9FA5]+", content):
                        c = re.sub(r'</?\w+[^>]*>', '', content)
                        text += "<p>" + c + "</p>"
                else:
                    cont = content.replace("<br/><br/>", "\n")
                    cont = re.sub(r'</?\w+[^>]*>', '', cont).strip()
                    cont = cont.replace("\n", "</p><p>")
                    text += "<p>" + cont + "</p>"
        except:
            print("ssssssssssss")
        print(text)
        item['title'] = title
        item['content'] = text
        item['sort'] = "娱乐"  # "星座"
        item['category'] = "美国电影"  # "星座"
        print(item)


if __name__ == '__main__':
    touTiao_down()
