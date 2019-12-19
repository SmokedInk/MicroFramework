# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   request_packaging
# @Time:    2019-11-02 11:24:01

import requests
from requests.adapters import HTTPAdapter

import urllib3
import socket
urllib3.disable_warnings()
socket.setdefaulttimeout(10)    # 设置socket层的超时时间为10秒


req = requests.Session()
req.mount("http://", HTTPAdapter(max_retries=3))
req.mount("https://", HTTPAdapter(max_retries=3))


def send_get_request(request_url, request_headers, proxies='', **kwargs):
    """
    requests的get请求封装
    :param request_url: 待发送请求的URL
    :param request_headers: 待发送请求的请求头
    :param proxies: 待发送请求的代理
    :return: 请求响应对象
    """
    kwargs.setdefault('allow_redirects', True)
    try:
        if proxies == "":
            response = req.get(url=request_url, headers=request_headers, timeout=(5, 30), **kwargs)
        else:
            response = req.get(url=request_url, headers=request_headers, timeout=(5, 30), proxies=proxies, **kwargs)
        response.close()
        return response
    except requests.exceptions.RequestException as err:
        print(err)
        return ""


def send_data_request(request_url, request_headers, data, proxies='', **kwargs):
    """
    requests的post请求封装(参数为Form Data与Json格式)
    :param request_url: 待发送请求的URL
    :param request_headers: 待发送请求的请求头
    :param data: 待发送请求提交的参数
    :param proxies: 待发送请求的代理
    :return: 请求响应对象
    """
    kwargs.setdefault('allow_redirects', True)
    try:
        if proxies == "":
            response = req.post(url=request_url, headers=request_headers, data=data, timeout=(5, 30), **kwargs)
        else:
            response = req.post(url=request_url, headers=request_headers, data=data, timeout=(5, 30), proxies=proxies, **kwargs)
        response.close()
        return response
    except requests.exceptions.RequestException as err:
        print(err)
        return ""


def send_file_request(request_url, request_headers, files, proxies='', **kwargs):
    """
    requests的post请求封装(参数为File)
    :param request_url: 待发送请求的URL
    :param request_headers: 待发送请求的请求头
    :param files: 待发送请求提交的文件参数
    :param proxies: 待发送请求的代理
    :return: 请求响应对象
    """
    kwargs.setdefault('allow_redirects', True)
    try:
        if proxies == "":
            response = req.post(url=request_url, headers=request_headers, files=files, timeout=(5, 30), **kwargs)
        else:
            response = req.post(url=request_url, headers=request_headers, files=files, timeout=(5, 30), proxies=proxies, **kwargs)
        response.close()
        return response
    except requests.exceptions.RequestException as err:
        print(err)
        return ""
