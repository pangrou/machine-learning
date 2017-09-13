# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import pandas as pd
from os import listdir
import operator

# 计算欧式距离
def getEucDistance(trainSet, dataSet):
	dataSetSize = dataSet.shape[0]
	inX = np.tile(trainSet, (dataSetSize, 1))
	dist = np.sqrt((np.square(inX - dataSet)).sum(axis=1))
	return dist

# 分类器
def classify(inX, dataSet, labels, k):
	dist = getEucDistance(inX, dataSet)
	SortDit = dist.argsort()
	classCount = {}
	for i in range(k):
		voterIlabel = labels[SortDit[i]]
		classCount[voterIlabel] = classCount.get(voterIlabel, 0) + 1
	sortedclassCount = sorted(classCount.items(), 
		key=operator.itemgetter(1),reverse=True)
	return sortedclassCount[0][0]

def loadDataSet(path):
	dataSet = pd.read_csv(path)
	dataSetMat = np.array(dataSet)
	dataLabel = dataSetMat[:,0]
	trainMat = dataSetMat[:,1:]
	m,n = trainMat.shape
	datMat = np.multiply(trainMat != np.zeros((m,n)), np.ones((m,1)))
	return datMat,dataLabel

# 测试分类器
def handWriteClassTest():
	trainingMat,trainingLabels = loadDataSet('train.csv')
	
	testSet = np.array(pd.read_csv('test.csv'))
	m,n = testSet.shape
	testMat = np.multiply(testSet != np.zeros((m,n)), np.ones((m,1)))

	result = []
	for i in range(testMat.shape[0]):  
		classifieRet = classify(testMat[i], trainingMat, trainingLabels, 10)
		result.append(classifieRet)
	return result

def saveToCsv(result):
	imageId = np.arange(1, len(result)+1)
	output = pd.DataFrame({'ImageId':imageId, 'Label':result})
	output.to_csv("result.csv",index=False)

if __name__ == '__main__':
	result = handWriteClassTest()
	saveToCsv(result)







