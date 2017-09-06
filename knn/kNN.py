# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import operator

def CreatDataSet():
	group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['A','A','B','B']
	return group,labels

def classify0(inX, dataSet, labels, k):
	# 计算欧式距离
	dataSetSize = dataSet.shape[0]
	diffMat = np.tile(inX, (dataSetSize,1)) 
	sqDiffMat = np.square(diffMat - dataSet)
	distances = np.sqrt(sqDiffMat.sum(axis=1))
	# 排序
	sortedDistIndicies = distances.argsort()
	# print(distances)
	# print(sortedDistIndicies)
	# 选择距离最小的k个点 和每个类别出现的次数
	classCount = {}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	print(classCount)	
	# 对每个类别出现的次数进行排序
	sortedClassCount = sorted(classCount.items(),
				key = operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]


if __name__ == '__main__':
	group,labels = CreatDataSet()
	result = classify0([0,0], group, labels, 3)
	print(result)



