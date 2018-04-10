# -*- coding: utf-8 -*-
# !/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup 
from urllib.error import HTTPError,URLError
import re
import sys
import datetime
import time
import pytesseract
from PIL import Image

flightStru = ["FlightNo","FlightCompany",
"FlightDeptimePlanDate","FlightDeptimeDate",
"FlightHTerminal","FlightArrtimePlanDate",
"FlightArrtimeDate","FlightState"]

def getUrlData(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html.read())
        return bsObj   
    except (HTTPError,URLError,AttributeError) as e:
        return ""

def getCitys(bsObjStr):
    flag = True
    data = bsObjStr
    findStr = "temp.push"
    dataList = []
    while flag: 
        try:
            firstIndex = data.index(findStr) + len(findStr) + 2
            nextIndex = firstIndex + data[firstIndex:].index("\");") 
            dataList.append(data[firstIndex:nextIndex])
            data = data[firstIndex:]
        except Exception as e:
            flag = False
    return dataList

def citysData(bsObj):
    flight = []
    dataList = getCitys(str(bsObj))

    for i in range(len(dataList)):
        flightinfo = {}
        bs = BeautifulSoup(dataList[i])

        flightnoList = bs.findAll("a")
        for i in range(len(flightnoList)):
            flightinfo[flightStru[i]] = flightnoList[i].get_text()
        
        spanList = bs.findAll("span")
        for i in range(1, len(spanList) - 1):
            text = spanList[i].get_text()
            if len(text) == 0: continue
            if "\"" in text:
                textList = text.split("\"")
                text = textList[len(textList) - 1]
            flightinfo[flightStru[i + 1]] = text.replace(" ","")
        if "/" in flightinfo["FlightHTerminal"]:
            flightinfo["FlightTerminal"] = flightinfo["FlightHTerminal"].split("/")[1]
            flightinfo["FlightHTerminal"] = flightinfo["FlightHTerminal"].split("/")[0]
        flight.append(flightinfo)
    for f in flight:
        print(f,len(flight))
    return flight,len(flight)


def dataProcess(bsObj):
    htmlList = bsObj.findAll("div",{"class","fly_box"})
    flight = []
    for html in htmlList:
        flightinfo = {}
        for d in html.findAll("div"):
            if 'class' not in d.attrs.keys():
                continue
            if d.attrs["class"][0] == "f_tit":  
                flightinfo["date"] = d.find("span").get_text()
                flightinfo["msg"] = d.h2.attrs["title"]
                if d.div is not None:
                    flightinfo["refer"] = d.div.get_text()
            elif d.attrs["class"][0] == "time":
                flightinfo[d.dd.get_text()] = urlToStr(d.dt.img.attrs["src"])
                flightinfo[d.findAll("dd")[1].get_text()] = urlToStr(d.findAll("dt")[1].img.attrs["src"])
            elif d.attrs["class"][0] == "con":   
                ontime = d.find("p",{"class":"red"}).get_text() + "准点率"
                flightinfo[ontime] = urlToStr(d.span.img.attrs["src"])
            elif d.attrs["class"][0] == "f_r":
                flightinfo["temper"] = d.p.get_text().strip().split("\r")[0]
        flight.append(flightinfo)
    print("flight:", flight)
    return flight

def urlToStr(img):
    url = img.replace("amp;", "")
    Downloads_Pic(url)
    return imageToStr()

def Downloads_Pic(picUrl):  
    try:
        f = open("unmetripVerificationCode.jpg", 'wb') 
        f.write(urlopen(picUrl).read())
        f.close()
    except Exception as e:
        print(picUrl+" error")

def imageToStr():
    image = Image.open("unmetripVerificationCode.jpg")
    yzm = pytesseract.image_to_string(image)
    return yzm

# 根据航班号+日期查询
def getFNoData(fNo, fData):
    url = 'http://www.umetrip.com/mskyweb/fs/fc.do?' \
    'flightNo=%s&date=%s&channel=' % (fNo, fData)
    print("url", url)
    htmlList = getUrlData(url)
    flight = dataProcess(htmlList)
    return flight

#根据航段查询
def getArrDepData(arr, dep, fData):
    url = 'http://www.umetrip.com/mskyweb/fs/fa.do?dep=' \
    '%s&arr=%s&date=%s&channel=' % (arr, dep, fData)
    htmlList = getUrlData(url)
    citysData(htmlList)


if __name__ == '__main__':
    today = datetime.date.today()
    deltadays = datetime.timedelta(days=185)
    for x in range(0,1): 
        print(x)
        # getFNoData("CA1701", str(today))  #CA1701 3U8315
        getArrDepData("HGH", "CTU", "2018-03-26")
        # today -= deltadays




















