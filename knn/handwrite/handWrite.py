# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import pandas as pd
from os import listdir
import operator

32*32 转 1*1024向量 
def img2vector(filename):
	returnVet = np.zeros((1, 1024))
	fr = open(filename)
	for i in range(32):
		lineStr = fr.readline()
		for j in range(32):
			returnVet[0,i*32+j] = int(lineStr[j])
	return returnVet	

# def img2vector(filename):
	# returnVet = np.zeros((1, 1024))
	# fr = np.array(open(filename).readlines())
	# returnVet = fr.reshape(1,32*32)

	# lineData = []
	# for line in open(filename).readlines():
	# 	lineStr = line.strip()
	# 	lineData.append(lineStr)
	# returnVet = np.array(lineData).reshape(1,32*32)

	# for i in range(32):
	# 	lineStr = fr.readline()
	# 	for j in range(32):
	# 		returnVet[0,i*32+j] = int(lineStr[j])
	# return returnVet		

# 使用 listdir 读取数据
def getDataSet(filePath):
	FileList = listdir(filePath)
	DataLen = len(FileList)
	DataMat = np.zeros((DataLen, 1024))
	Labels = []
	for i in range(1):  #DataLen
		filename = FileList[i]
		fileStr = filename.split('.')[0]
		fileLabel = fileStr.split('_')[0]
		Labels.append(fileLabel)
		DataMat[i] = img2vector('%s/%s' % (filePath,filename))
	return DataMat,Labels

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

# 测试分类器
def handWriteClassTest():
	trainingMat,trainingLabels = getDataSet('digits/trainingDigits')
	testMat,testLables = getDataSet('digits/testDigits')
	errorCount = 0
	for i in range(1):  #testMat.shape[0]
		classifieRet = classify(testMat[i], trainingMat, trainingLabels, 10)
		if(classifieRet != testLables[i]):
			errorCount += 1
			print('ret: %s, label:%s' % (classifieRet,testLables[i]))
	print('errCnt:%d,errRat:%.6s' % (errorCount, errorCount/testMat.shape[0]))

if __name__ == '__main__':
	handWriteClassTest()









