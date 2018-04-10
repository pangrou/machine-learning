# -*- coding: utf-8 -*-
# !/usr/bin/env python

import datetime
from dataProcess import *
from saveToMysql import *
from airport_info import *

db,cursor = db_con_save()

def getFlightInfo(url, isLeg):
    # urlData = getUrlData(url)
    urlData = getXundailiData(url, 0)
    # urlData = getQuanwangData(url, 0)
    print(urlData)
    dataPro = dataProcess(urlData, url+"&limityzm=")
    flights = []
    if type(dataPro) is not dict:
        for data in dataPro:
            if isLeg : flights.append(data["FlightNo"])
            else : save(parseJson(data), db,cursor)
    return flights

def queryAllFlight(flights, fData):
    for f in flights:
        getFnoData(f, fData)

#根据航段查询
def getArrDepData(arr, dep, fData):
    url = 'http://webapp.veryzhun.com/h5/flightsearch?arr=%s&dep=%s&' \
    'date=%s&token=74e5d4cac3179fc076af4f401fd4ebe3' % (arr, dep, fData)
    flights = getFlightInfo(url, True)
    return flights

#根据航班号查询
def getFnoData(fNo, fData):
    url = 'http://webapp.veryzhun.com/h5/flightsearch?fnum=%s&date=%s' \
    '&token=f1c9dae3737f47d45ceeb72cfa3c8094' % (fNo, fData)
    getFlightInfo(url, False)

def flight_center(fData, airports):
    for airportCode in airports:
        if airportCode[0] == "CAN": continue
        # 目的地为 白云机场
        flights = getArrDepData("CAN", airportCode[0], fData)
        queryAllFlight(flights, fData)
        # 出发地为 白云机场
        flights = getArrDepData(airportCode[0], "CAN", fData)
        queryAllFlight(flights, fData)

if __name__ == '__main__':
    airports = getAirports()
    today = datetime.date.today()
    flight_center(str(today), airports)
    # getFnoData("CA1530", str(today))
    # getArrDepData("CTU", "HGH", str(today))
    closeSaveDb(db)






