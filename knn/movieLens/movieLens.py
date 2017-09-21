# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import numpy as np
import pandas as pd
# http://www.jianshu.com/p/b44ade7f6ba8

def loadTrainSet():
	movieList = {}
	for line in open("data/ml-100k/u.item", encoding='ISO-8859-1').readlines():
		# u.item 包含电影id,电影名称
		(movieId, title) = line.split('|')[0:2]
		movieList[movieId] = title

	userInfo = {}
	userInfoUid = {}
	for line in open("data/ml-100k/u.data").readlines():
		# u.data 包含用户id,电影id,评分
		(uid, mid, rating) = line.split('\t')[0:3]
		if uid not in userInfoUid.keys():
			userInfoUid[uid] = {}
		userInfoUid[uid][movieList[mid]] = int(rating)

		if movieList[mid] not in userInfo.keys():
			userInfo[movieList[mid]] = {}
		userInfo[movieList[mid]][uid] = int(rating)
	return 	movieList,userInfo,userInfoUid

# {电影，用户，评分}
def transfromUserInfo(data):
	userInfo = {}
	for k1, v1 in data.items():
		for k2, v2 in v1.items():
			if k2 not in userInfo.keys():
				userInfo[k2] = []
			userInfo[k2][k1] = v2
	return userInfo			

# 计算距离

# 欧几里得距离评价
def edclidean(data, person1, person2):
	# 两个都评价过的电影列表
	sameList = [item for item in data[person1].keys() if item in data[person2].keys()]
	print(sameList)
	# 对这些电影列表，计算距离
	dis = math.sqrt((np.square(data[person1][item] - data[person2][item])).sum())
	return dis

# 皮尔逊相关系数评价:
def pearson(data, movie1, movie2):
	personList = [person for person in data[movie1].keys() if person in data[movie2].keys()]
	pLen = len(personList)	
	if pLen == 0:
		return 0
	# print('movie1:',movie1)
	# print('movie2:',movie2)
	# print('personList:',personList)
	# print('pLen:',pLen)

	rating1 = [data[movie1][p] for p in personList]
	rating2 = [data[movie2][p] for p in personList]
	ratingSq1 = [data[movie1][p]**2 for p in personList]
	ratingSq2 = [data[movie2][p]**2 for p in personList]	

	# 计算评价和 评价平方和 评价成绩和
	sum1 = sum(rating1)
	sum2 = sum(rating2)
	sumSq1 = sum(ratingSq1)
	sumSq2 = sum(ratingSq2)
	psum = sum([data[movie1][p] * data[movie2][p] for p in personList])

	# 皮尔逊相关系数计算
	num = psum - (sum1 * sum2) / pLen
	den = np.sqrt((sumSq1 - np.square(sum1)/pLen) * (sumSq2 - np.square(sum2)/pLen))

	if den == 0:
		return 0
	return num/den

def topRating(data, movie, k = 5):
	# 计算该电影与每部电影之间的皮尔逊相关系数
	scores = {}
	for mov in data.keys():
		if mov != movie:
			scores[mov] = pearson(data, movie, mov)
	scoSorted = sorted(scores.items(),key=lambda scores:scores[1],reverse=True)		
	# print('movie {0}, scoSorted: top {1}, {2}'.format(movie, k, scoSorted[:k]))
	return scoSorted[:k]
	
def getMovieList(data):
	matchMovieList = {}
	for mov in data.keys():
		matchMovieList[mov] = topRating(data, mov, 5)
	return matchMovieList

def getRecommendMov(data, matchmov, userid, k=5):
	try:
		userRating = data[userid]
	except KeyError:
		print('No User')
		return 0
	scores = {}  #记录加权和	
	totalSco = {} #记录评分和

	# 用户所有评过分的电影
	for mov, rating in userRating.items():
		# 遍历当前电影的所有相似电影
		for nearMov, nearPear in matchmov[mov]:
			if nearMov in userRating.keys():
				continue
			if nearMov not in scores.keys():
				scores[nearMov] = nearPear * rating
				totalSco[nearMov] = nearPear
			scores[nearMov] += nearPear * rating
			totalSco[nearMov] += nearPear

	rankings = [(scores[nearMov]/totalSco[nearMov],nearMov) for nearMov in  scores.keys() if totalSco[nearMov] != 0]
	rankings.sort(key=lambda x:x[0], reverse=True)
	recommendMov = [rankings[i][1] for i in range(k)]
	return recommendMov

def movielensClass():
	movieList,userInfo,userInfoUid = loadTrainSet()
	matchmov = getMovieList(userInfo)
	return matchmov,userInfo,userInfoUid


if __name__ == '__main__':
	matchmov,userInfo,userInfoUid = movielensClass()
	while True:
		userid = input("input userid:")
		if userid == 'exit':
			break
		else:
			near = getRecommendMov(userInfoUid, matchmov, userid)
			print('near:',near)
	







