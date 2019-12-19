# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   setup
# @Time:    2019-11-07 16:56:15


from distutils.core import setup
setup(name="crawlProject", version="0.0.1", description="Crawler function pack", author="SmokedInk", py_modules=['config.get_useragent','config.proxy_ip', 'config.request_packaging', 'config.sqllite3_operation',
                                                                                                                 'IOFile.IOExcel', 'IOFile.IOCsv'])
