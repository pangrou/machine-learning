# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

df = pd.read_csv("/Users/m2shad0w/Desktop/python/机器学习相关/逻辑回归-House Prices/train.csv")
test_data = pd.read_csv("/Users/m2shad0w/Desktop/python/机器学习相关/逻辑回归-House Prices/test.csv")

misGarage = ["GarageType","GarageFinish",\
				"GarageCars","GarageArea","GarageQual","GarageCond"]
misBmst = ["BsmtQual","BsmtCond","BsmtExposure","BsmtFinType1",\
			"BsmtFinSF1","BsmtFinType2","BsmtFinSF2","BsmtUnfSF"]

def fill_Garage_Bmst(misList):
	for i in xrange(len(misList)):
		df[misList[i]][df[misList[i]].isnull()] = None

def fill_GarageYrBlt():
	df.GarageYrBlt[df.GarageYrBlt.isnull()] = df.YearBuilt[df.GarageYrBlt.isnull()]

def fill_LotFrontage():
	median_lot = np.array(df.LotFrontage[df.LotFrontage.notnull()])
	df.LotFrontage[df.LotFrontage.isnull()] = np.median(median_lot)



def fill_mis_val():
	#填补车库的缺失值
	fill_Garage_Bmst(misGarage)
	#填补 地下室
	fill_Garage_Bmst(misBmst)
	#填补车库的建造年份=房子yearbuild
	fill_GarageYrBlt()
	fill_LotFrontage()

def plot_data():
	# sns.distplot(df.SalePrice)
	var = 'GrLivArea'
	data = pd.concat([df['SalePrice'],df['GrLivArea']],axis=1)
	print(data[:5])
	# data.plot.scatter(x=var,y='SalePrice',ylim=(0,800000))



def house_prices():
	#补全数据
	# fill_mis_val()
	plot_data()
	# print(df.SalePrice.describe())
	# print(df.info())


if __name__ == '__main__':
	house_prices()	
	print('hello')



