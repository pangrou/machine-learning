# -*- coding: utf-8 -*-
# !/usr/bin/env python

from urllib.request import urlopen
import random


def getProxyip():
    # 这里填写全网代理IP提供的API订单号（请到用户中心获取）
    order = "---------"
    # 获取IP的API接口
    apiUrl = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html"
    # 要抓取的目标网站地址
    # targetUrl = "http://2017.ip138.com/ic.asp"
    
    try:
        # 获取IP列表
        res = urlopen(apiUrl).read().strip()
        # 按照\n分割获取到的IP
        # ips = res.split("\n")
        # 随机选择一个IP
        # proxyip = random.choice(ips)
        # 使用代理IP请求目标网址
        proxyip = res.decode(encoding="utf-8")
        return proxyip
        # html = urllib.urlopen(targetUrl, proxies={'http':'http://' + proxyip})
        # # 输出内容
        # print("使用代理IP " + proxyip + " 获取到如下HTML内容：\n" + unicode(html.read(), "gb2312").encode("utf8"))
    except Exception:  
        return ""















