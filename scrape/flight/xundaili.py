# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import time
import hashlib
import requests
from lxml import etree

_version = sys.version_info
is_python3 = (_version[0] == 3)

ip = "forward.xdaili.cn"
port = "80"

orderno = ""---------""
secret = ""---------""

def getAuth():
    timestamp = str(int(time.time()))                # 计算时间戳
    # string = ""
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    if is_python3:                          
        string = string.encode()
    sign = hashlib.md5(string).hexdigest().upper()                 # 计算sign   
    # sign = md5_string                        # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    return auth

def getXundailiIp():
    ip_port = ip + ":" + port
    auth = getAuth()
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": auth}
    return headers,proxy
    


















