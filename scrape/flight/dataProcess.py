# -*- coding: utf-8 -*-
# !/usr/bin/env python

from urllib.request import urlopen
import xundaili
import goubanjia
import requests
import pytesseract
from PIL import Image
import json
import re
import time
from urllib.error import HTTPError,URLError

DATALEN = 38

def getXundailiData(url, maxCounts):
    headers,proxy = xundaili.getXundailiIp()
    try:
        r = requests.get(url, headers=headers, proxies=proxy, verify=False,allow_redirects=False,timeout=3)
        result = json.loads(r.content.decode(encoding="utf-8"))
        return result
    except (HTTPError,URLError,AttributeError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError,
        json.decoder.JSONDecodeError) as e:

        print("json.loads ERROR!!!  ",url)
        if maxCounts < 3: getXundailiData(url, ++maxCounts)
        return ""

def getQuanwangData(url, maxCounts):
    proxyip = goubanjia.getProxyip()
    print("proxyip:", proxyip)
    if len(proxyip) == 0: return ""
    try: 
        r = requests.get(url, proxies={'http':'http://' + proxyip}, timeout=3)
        print(r.content)
        result = json.loads(r.content.decode(encoding="utf-8"))
        return result
    except (HTTPError,URLError,AttributeError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError,
        json.decoder.JSONDecodeError) as e:
    
        print("json.loads ERROR!!!  ",url)
        if maxCounts < 3: getQuanwangData(url, ++maxCounts)
        return ""

# 去除空值
def parseJson(data):
    if len(data.keys()) < DATALEN:
        print("data is invaild!")
        return ""
    dataSet = {}
    for k,v in data.items():
        if v != "":
            dataSet[k] = v
    dataSet["fightDate"] = dataSet["FlightDeptimePlanDate"].split(" ")[0]
    return dataSet

def dataProcess(data, url):
    yzmUrl = VeriCodeJudge(data)  
    if yzmUrl is not "":
        Downloads_Pic(yzmUrl)
        yzm = imageToStr()
        if len(yzm) is 0:
            yzm = "111"
        urlData = getXundailiData(url+yzm, 0) #getUrlData
        # urlData = getQuanwangData(url+yzm, 0)
        dataProcess(urlData, url)
    return data

# 判断 是否需要输入验证码
def VeriCodeJudge(data):
    if type(data) is not dict:
        return ""    
    if "error_code" in data.keys():
        return ""
    try:
        return data.get('data').get('limitYzmUrl')
    except Exception as e:    
         return ""

def Downloads_Pic(picUrl):  
    try:
        f = open("VerificationCode.jpg", 'wb') 
        f.write(urlopen(picUrl).read())
        f.close()
    except Exception as e:
        print(picUrl+" error")

def imageToStr():
    image = Image.open("VerificationCode.jpg")
    yzm = pytesseract.image_to_string(image)
    yzm = re.sub('[^a-zA-Z0-9]',"",yzm)
    return yzm

def getUrlData(url):
    print("url",url)
    try:
        html = urlopen(url).read().strip().decode("utf-8")
        return json.loads(html)
    except Exception as e:
        return ""



