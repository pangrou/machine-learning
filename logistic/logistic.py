# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt

def loadDataSet():
	dataMat = []; labelMat = []
	for line in open('data/testSet.txt').readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat,labelMat

def sigmoid(inX):
	h = []
	for i in range(len(inX)):
		h.append(1.0/(1+math.exp(-inX[i])))
	return np.mat(h).transpose()

def socSigmoid(inX):
	return 1.0/(1+math.exp(-inX))

def gradAscent(dataMatIn, classLabels):
	dataMatrix = np.mat(dataMatIn)
	labelMat = np.mat(classLabels).transpose()
	m,n = np.shape(dataMatIn)
	alpha = 0.001
	maxCycles = 500
	weights = np.ones((n,1))
	for k in range(maxCycles):
		h = sigmoid(np.dot(dataMatrix,weights))
		error = labelMat - h
		weights = weights + alpha*dataMatrix.transpose()*error
	return weights
	
def socGradAscent0(dataMatrix, classLabels):
	m,n = np.shape(dataMatrix)
	alpha = 0.01
	weights = np.ones(n)
	for i in range(m):
		h = socSigmoid(sum(dataMatrix[i]*weights))
		error = classLabels[i] - h
		weights = weights + alpha * dataMatrix[i] * error
	return weights

def socGradAscent1(dataMatrix, classLabels, numIter = 150):
	m,n = np.shape(dataMatrix)
	weights = np.ones(n)
	for j in range(numIter):
		dataIndex = list(range(m))
		for i in range(m):
			alpha = 0.04/(1.0+j+i) + 0.001
			randIndex = int(np.random.uniform(0, len(dataIndex)))
			h = socSigmoid(sum(dataMatrix[randIndex]*weights))
			error = classLabels[randIndex] - h
			weights = weights + alpha * error * dataMatrix[randIndex]
			del(dataIndex[randIndex])
	return weights

def plotBestFit(weights,dataMat,labelMat):
	dataArr = np.mat(dataMat)
	# weights = weights.getA()
	n = np.shape(dataArr)[0]
	xcord1 = []; ycord1 = []
	xcord2 = []; ycord2 = []
	for i in range(n):
		if int(labelMat[i]) == 1:
			xcord1.append(dataArr[i,1])
			ycord1.append(dataArr[i,2])
		else:
			xcord2.append(dataArr[i,1])
			ycord2.append(dataArr[i,2])
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
	ax.scatter(xcord2, ycord2, s=30, c='green')
	x = np.arange(-3.0, 3.0, 0.1)
	y = (-weights[0] - weights[1]*x)/weights[2]	
	ax.plot(x, y)
	plt.xlabel('X1'); plt.ylabel('X2')
	plt.show()

if __name__ == '__main__':
	dataMat,labelMat = loadDataSet()
	# weights = gradAscent(dataMat,labelMat)
	weights = socGradAscent0(np.array(dataMat),labelMat)
	print(weights)
	# plotBestFit(weights,dataMat,labelMat)
				











