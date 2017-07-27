# -*- coding: utf-8 -*-
# !/usr/bin/env python

# https://www.kaggle.com/c/word2vec-nlp-tutorial

import numpy as np
import pandas as pd
import re
import math
import operator
from bs4 import BeautifulSoup  #html标签处理

def creatVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return vocabSet	

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
	return p1Vect,p0Vect,pAbusive

def classifyNB(vec2Classify, p0Vect,p1Vect,pClass1):
	p1VecSum = 0; p0VecSum = 0
	for i in range(len(p0Vect)):
		p1VecSum += vec2Classify[i] * p1Vect[i]
		p0VecSum += vec2Classify[i] * p0Vect[i]
	p1 = p1VecSum + math.log(pClass1)
	p0 = p0VecSum + math.log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

# 取出前2000个高频字符串   with and you for之类
def calcMostFreq(vocabList, fullText):
	freqDict = {}
	for token in vocabList:
		freqDict[token] = fullText.count(token)
	# iteritems 排序
	sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1),\
					reverse=True)
	return sortedFreq[:2000]

def textParse(review):
	# 去掉HTML 标签，拿到内容
	wordList = BeautifulSoup(review).get_text()
	# 用正则表达式取出符合规范的部分
	wordList = re.sub("[^a-zA-Z]"," ", wordList)
	# 小写化所有的词，并转成词list
	[tok.lower().split() for tok in wordList if len(tok) > 2]
	return wordList


def getDataSet():
	trainingSet = pd.read_csv("labeledTrainData.tsv",header=0,delimiter="\t",quoting=3)
	testSet = pd.read_csv("testData.tsv",header=0,delimiter="\t")
	testSubmission = pd.read_csv("sampleSubmission.csv")
	dataSet = pd.read_csv("unlabeledTrainData.tsv",header=0,delimiter="\t",quoting=3)
	return trainingSet,testSet,testSubmission,dataSet

def bagsOfPopcorn(trainingSet,testSet):
	docList = []; classList = []; fullText = []
	for i in range(len(trainingSet['id'])):
		wordList = textParse(trainingSet['review'][i])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(trainingSet['sentiment'][i])
	vocabList = creatVocabList(docList)	
	top2000Words = calcMostFreq(vocabList, fullText)
	for word in top2000Words:
		if word[0] in vocabList:
			vocabList.remove(word[0])
	trainMat = []
	for i in range(len(docList)):
		trainMat.append(bagOfWords2VecMN(vocabList, docList[i]))
	p1Vect,p0Vect,pAbusive = trainNB0(trainMat, classList)	
	return vocabList,p1Vect,p0Vect,pAbusive
	
def getResult(vocabList,dataSet,p1V,p0V,pAb):
	Result = []
	for i in range(len(dataSet)):
		wordList = textParse(dataSet['review'][i])
		testList = bagOfWords2VecMN(vocabList, wordList)
		Result.append(classifyNB(testList,p1V,p0V,pAb))	
	return Result

def testModel(vocabList,testSet,p1V,p0V,pAb,testSubmission):
	errorCount = 0; resultID = []
	testResult = getResult(vocabList,testSet,p1V,p0V,pAb)
	result = pd.DataFrame({"id":testSet['id'], "sentiment":testResult})
	result.to_csv("result.csv",index=False)

	for i in range(len(testResult)):
		if testResult[i] != testSubmission['sentiment'][i]:
			errorCount += 1
	print('error rate is : ', float(errorCount)/len(testResult))		

def getSentiment(vocabList,dataSet,p1V,p0V,pAb):
	Result = getResult(vocabList,dataSet,p1V,p0V,pAb)
	output = pd.DataFrame({"id":dataSet['id'], "sentiment":Result})
	output.to_csv("result_test.csv",index=False)
	# print(output.info())
	# print(output[:3])


if __name__ == '__main__':
	trainingSet,testSet,testSubmission,dataSet = getDataSet()
	vocabList,p1V,p0V,pAb = bagsOfPopcorn(trainingSet,testSet)
	testModel(vocabList,testSet,p1V,p0V,pAb,testSubmission)
	getSentiment(vocabList,dataSet,p1V,p0V,pAb)















