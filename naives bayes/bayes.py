# -*- coding: utf-8 -*-
# !/usr/bin/env python

import words2vec as bayes
import numpy as np

def main():
	# 加载数据集
	listOPosts,listClasses = bayes.loadDataSet()
	# 获取所有的词向量
	myVocabList = bayes.creatVocabList(listOPosts)
	# 文本向量转换成数字向量
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(bayes.setOfWords2Vec(myVocabList,postinDoc))
	p0V,p1V,pAb = bayes.trainNB0(np.array(trainMat),np.array(listClasses))
	testEntry = ['love', 'my', 'dalmation']
	thisDoc = bayes.setOfWords2Vec(myVocabList,testEntry)
	thisResult = bayes.classifyNB(thisDoc,p0V,p1V,pAb)
	print(testEntry,'classified as ',thisResult)

	testEntry = ['stupid', 'garbage']
	thisDoc = bayes.setOfWords2Vec(myVocabList,testEntry)
	thisResult = bayes.classifyNB(thisDoc,p0V,p1V,pAb)
	print(testEntry,'classified as ',thisResult)

if __name__ == '__main__':
	main()


