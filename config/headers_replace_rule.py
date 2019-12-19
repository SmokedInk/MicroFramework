# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   headers规则转换
# @Time:    2019-11-22 14:20:11
# @Desc:    headers Web格式 -> .py请求格式

import re


headers = """
ev_type: ajax
ax_status: 200
ax_type: put
ax_request_header: Authorization: BLZ40F8TCN3JNCL5MVY5:TDyv69nZ7307lEcQNkfUnGLxAaI=:ZGVhZGxpbmU6IDE1NzUxNjY2Mzk=
Content-CRC32: 45989f2f
X-Storage-U: 259127382384055
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="undefined"
ax_duration: 308
ax_size: 0
ax_response_header: content-type: application/octet-stream
ax_protocol: https
ax_domain: tos-cu-hl.snssdk.com
ax_path: /tos-cn-v-0000/32b7b415f8984402a7ce4796bb998458
ax_url: https://tos-cu-hl.snssdk.com/tos-cn-v-0000/32b7b415f8984402a7ce4796bb998458
version: 2.1.8
hostname: mp.toutiao.com
protocol: https
url: https://mp.toutiao.com/profile_v3/xigua
slardar_session_id: 79f067d9-6711-4945-9ada-76b166311a47
sample_rate: 0.5
pid: index_new
report_domain: i.snssdk.com
screen_resolution: 1920x1080
network_type: 4g
bid: toutiao_mp
context: {}
slardar_web_id: 1650142068003843
timestamp: 1575080241029
"""

# new_headers = re.sub(r"(.*?):\s(.*)", headers)
items = re.findall(r"(.*?):\s(.*)", headers)
new_headers = dict()
for item in items:
    new_headers[item[0]] = item[1]

print(new_headers)
