# -*- coding: utf-8 -*-
# !/usr/bin/env python

import feedparser
import re
import words2vec as bayes
import numpy as np
import operator	

def testParse(bigString):
	# 去掉单词、数字，字符串长度小于2
	lisetOfToken = re.split('\\W*', bigString)
	# 全部小写处理
	return [tok.lower() for tok in lisetOfToken if len(tok) > 2]

# 取出前三十个高频字符串   with and you for之类
def calcMostFreq(vocabList, fullText):
	freqDict = {}
	for token in vocabList:
		freqDict[token] = fullText.count(token)
	# iteritems 排序
	sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1),\
					reverse=True)
	return sortedFreq[:50]					

def localWords(feed1, feed0):
	docList = []; classList = []; fullText = []
	minLen = min(len(feed1['entries']), len(feed0['entries']))
	# print(minLen)
	for i in range(minLen):
		wordList = testParse(feed1['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = testParse(feed0['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	# 创建所有 词向量
	vocabList = bayes.creatVocabList(docList)
	# 取出前三十个高频字符串
	top30Words = calcMostFreq(vocabList, fullText)
	# print(top30Words)
	# 去掉高频词
	for pairW in top30Words:
		if pairW[0] in vocabList:
			vocabList.remove(pairW[0])
	print(vocabList)
	print(len(vocabList))		
	# 留存交叉验证	 随机取20个作为测试集 其他为训练集
	trainingSet = list(range(2 * minLen)); testSet = []
	for i in range(20):
		randIndex = int(np.random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])	
		del(trainingSet[randIndex])
	# print(testSet)
	# 训练模型
	trainMat = []; trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(bayes.bagOfWords2VecMN(list(vocabList),docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V,p1V,pSpam = bayes.trainNB0(np.array(trainMat), np.array(trainClasses))
	# print('pSpam: ',pSpam)
	# 测试数据 查看错误率
	errorCount = 0
	for docIndex in testSet:
		wordVector = bayes.bagOfWords2VecMN(list(vocabList),docList[docIndex])
		if bayes.classifyNB(wordVector,p0V,p1V,pSpam) != classList[docIndex]:
			errorCount += 1
			# print(docList[docIndex], 'error')
	print('the error rate is: ', float(errorCount)/len(testSet))	
	return vocabList,p0V,p1V	

def getTopWords(ny,sf):
	vocabList,p0V,p1V = localWords(ny,sf)
	topNY = []; topSF = []
	for i in range(len(p0V)):
		if p0V[i] > -6.0:	
			topSF.append((list(vocabList)[i],p0V[i]))
		if p1V[i] > -6.0:
			topNY.append((list(vocabList)[i],p1V[i]))

	sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
	print('SF *****   *****    *****')
	top10SF = map(lambda x: x[0], sortedSF[:10])
	for i in top10SF:
		print(i)

	sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
	print('NY *****   *****    *****')
	for item in sortedNY[:10]:
		print(item[0])

if __name__ == '__main__':
	ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
	sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
	getTopWords(ny,sf)







	








