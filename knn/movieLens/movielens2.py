# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import numpy as np
import pandas as pd

def loadTrainSet():
	movieList = {}
	for line in open("data/ml-100k/u.item", encoding='ISO-8859-1').readlines():
		# u.item 包含电影id,电影名称
		(movieId, title) = line.split('|')[0:2]
		movieList[movieId] = title

	userInfo = {}
	for line in open("data/ml-100k/u.data").readlines():
		# u.data 包含用户id,电影id,评分
		(uid, mid, rating) = line.split('\t')[0:3]
		if uid not in userInfo.keys():
			userInfo[uid] = {}
		userInfo[uid][movieList[mid]] = int(rating)
	return 	movieList,userInfo

# 皮尔逊相关系数评价:
def pearson(data, user1, user2):
	movList = [mov for mov in data[user1].keys() if mov in data[user2].keys()]
	mLen = len(movList)	
	if mLen == 0:
		return 0
	# print('user1: ,user2:',user1,user2)
	# print('movList:',movList)

	# 计算评价和 评价平方和 评价成绩和
	sum_x = sum([data[user1][mov] for mov in movList])
	sum_y = sum([data[user2][mov] for mov in movList])
	sum_x2 = sum([data[user1][mov]**2 for mov in movList])
	sum_y2 = sum([data[user2][mov]**2 for mov in movList])	
	sum_xy = sum([data[user1][mov] * data[user2][mov] for mov in movList])

	# 皮尔逊相关系数计算
	num = sum_xy - (sum_x * sum_y) / mLen
	den = np.sqrt((sum_x2 - np.square(sum_x)/mLen) * (sum_y2 - np.square(sum_y)/mLen))

	if den == 0:
		return 0
	return num/den

def topRating(data, user, k = 5):
	# 计算用户与每个用户之间的皮尔逊相关系数
	scores = {}
	for u in data.keys():
		if u != user:
			scores[u] = pearson(data, user, u)
	scoSorted = sorted(scores.items(),key=lambda scores:scores[1],reverse=True)		
	# print('user {0}, scoSorted: top {1}, {2}'.format(user, k, scoSorted[:k]))
	return scoSorted[:k]
	
def NearUserList(data):
	matchUserList = {}
	for u in data.keys():
		matchUserList[u] = topRating(data, u, 5)
	return matchUserList

def getRecommendMov(data, matchNear, user, k=5):
	try:
		userRating = data[user]
	except KeyError:
		print('No User')
		return 0

	scores = {}  #记录加权和	
	totalSco = {} #记录评分和

	# 遍历相似的用户 {用户：相关系数}
	for u, upear in matchNear[user]:
		# {电影：评分}
		for mov, mpear in data[u].items():
			if mov in userRating.keys():
				continue
			if mov not in scores.keys():
				scores[mov] = upear * mpear
				totalSco[mov] = upear
			scores[mov] += upear * mpear
			totalSco[mov] += upear

	rankings = [(scores[mov]/totalSco[mov],mov) for mov in  scores.keys() if totalSco[mov] != 0]
	rankings.sort(key=lambda x:x[0], reverse=True)
	recommendMov = [rankings[i][1] for i in range(k)]
	return recommendMov

def movielensClass():
	movieList,userInfo = loadTrainSet()
	matchNear = NearUserList(userInfo)
	return matchNear,userInfo

if __name__ == '__main__':
	matchNear,userInfo = movielensClass()
	while True:
		userid = input("input userid:")
		if userid == 'exit':
			break
		else:
			near = getRecommendMov(userInfo, matchNear, userid)
			print('near:',near)
	







