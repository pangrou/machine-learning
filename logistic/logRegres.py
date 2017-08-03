# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logistic 
import numpy as np

TRAIN_TIMES = 500

def classifyVector(inX, weights):
	prob = logistic.socSigmoid(sum(inX * weights))
	if prob >= 0.5:
		return 1.0
	else:
		return 0.0

def colicTest():
	trainingSet = []; trainingLabels = []
	for line in open('data/horseColicTraining.txt').readlines():
		currLine = line.strip().split('\t')
		lineArr = []
		for i in range(len(currLine)-1):
			lineArr.append(float(currLine[i]))
		trainingSet.append(lineArr)	
		trainingLabels.append(float(currLine[len(currLine)-1]))
	weights = logistic.socGradAscent1(np.array(trainingSet),trainingLabels,TRAIN_TIMES)
	# print(weights)
	errorCount = 0; numTestVec = 0.0
	for line in open('data/horseColicTest.txt').readlines():
		numTestVec += 1.0
		currLine = line.strip().split('\t')
		lineArr = []
		for i in range(len(currLine)-1):
			lineArr.append(float(currLine[i]))
		if int(classifyVector(lineArr,weights) != int(currLine[len(currLine)-1])):
			errorCount += 1
	# print(errorCount,numTestVec)
	errorRate = float(errorCount)/numTestVec
	print('the error rate of this test is :%f' % errorRate)
	return errorRate

def multiTest():
	numTests = 10; errorSum = 0.0
	for k in range(numTests):
		errorSum += colicTest()
	print('after %d iterations the average error rate is :%f' % (numTests,errorSum/float(numTests)))		


if __name__ == '__main__':
	multiTest()







