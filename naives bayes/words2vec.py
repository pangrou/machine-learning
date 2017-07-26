# -*- coding: utf-8 -*-
# !/usr/bin/env python

# 从文本中构建词向量

import numpy as np
import math

def loadDataSet():
	postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
				   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
				   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
				   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
				   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
				   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0,1,0,1,0,1]
	return postingList,classVec

def creatVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	# vocabSet = map(lambda x: set(x), dataSet)

	# ravel() 拉平 二维数组转换成一位数组
	# unique() 去重
	# dataSet = np.array(dataSet).flatten()
	# vocabSet = np.unique(dataSet)
	# vocabSet = [set(document) for document in dataSet]
	return vocabSet

def setOfWords2Vec(vocabList, inputSet):
	returnVet = [1 if w in inputSet else 0 for w in vocabList]
	# returnVet = map(lambda x: 1 if x in vocabList else 0, inputSet)
	return returnVet

# def bagOfWords2VecMN(vocabList, inputSet):
# 	returnVet = [0] * len(vocabList)
# 	for word in vocabList:
# 		if word in inputSet:
# 			returnVet[vocabList.index(word)] += 1
# 	return returnVet	

def bagOfWords2VecMN(vocabList, inputSet):
	returnVet = [0] * len(vocabList)
	for i in range(len(vocabList)):
		if vocabList[i] in inputSet:
			returnVet[i] += 1
	return returnVet

# 训练算法：从词向量计算概率
# trainMatrix：文档矩阵(数字向量)
# trainCategory：文档对应的类别 0正常 1垃圾
def trainNB0(trainMatrix, trainCategory):
	# 文档数量
	numTrainDocs = len(trainMatrix)
	# 词汇量大小
	numWords = len(trainMatrix[0])
	# 垃圾文档的概率
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	# 创建一个全部为0的矩阵p0Num
	# [1,2,3,4,0,0,1]即第一个词在垃圾文档中出现的次数1次，第二个出现2次
	# p1Denom 所有的词出现的总数 即1+2+3+4+1=11
	p0Num = np.ones(numWords); p1Num = np.ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0

	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	# 得到每个词在垃圾文档中出现的频率[1/11,2/11,3/11,4/11,0,0,1/11]	
	p1Vect = [math.log(x/p1Denom) for x in p1Num]
	p0Vect = [math.log(x/p0Denom) for x in p0Num]
	# p1Vect = p1Num/p1Denom
	# p0Vect = p0Num/p0Denom
	return p1Vect,p0Vect,pAbusive

def classifyNB(vec2Classify, p0Vect,p1Vect,pClass1):
	p1VecSum = 0; p0VecSum = 0
	for i in range(len(p0Vect)):
		p1VecSum += vec2Classify[i] * p1Vect[i]
		p0VecSum += vec2Classify[i] * p0Vect[i]

	p1 = p1VecSum + math.log(pClass1)
	p0 = p0VecSum + math.log(1.0 - pClass1)
	# p1 = sum(vec2Classify * p1Vect) + math.log(pClass1)
	# p0 = sum(vec2Classify * p0Vect) + math.log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0















