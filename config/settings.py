# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   settings
# @Time:    2019-12-10 13:37:07
# @Desc:    配置文件

import os


# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 服务器调试模式, 值为False时不自动重启服务器
DEBUG = False

# 变更自动重启
AUTORELOAD = False

# cookie secret key
COOKIE_SECRET = '{cookie_secret}'

# 是否开启csrf攻击防范
XSRF_COOKIES = False

# 允许访问的HOST配置
ALLOWED_HOSTS = []

# 模块配置
MODULES = [
    # "swagger",
]

# 命令配置
COMMANDS = []

# 数据库配置
DATABASES = {
    'mongodb': {
        "host": 'localhost',
        "port": 27017
    }
}

# 缓存
CACHES = {}

# 静态文件目录
STATIC = ""

# 模板文件目录
TEMPLATE = ""

# 算法模型目录
DATA = ""

PAGE_SIZE = 10

PAGE_SHOW = 10
