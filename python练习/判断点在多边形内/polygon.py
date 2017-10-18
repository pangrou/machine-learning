# 参考：<http://www.cnblogs.com/On1Key/p/5673886.html>


# -*- coding: utf-8 -*-
# !/usr/bin/env python

class Point:
	lng = ''
	lat = ''

	def __init__(self, lng, lat):
		self.lng = lng
		self.lat = lat

	def show(self):	
		print(self.lng,"\t",self.lat)

# 外包矩形
def getPolygonBounds(points):
	pointLen = len(points)
	top = down = left = right = points[0]
	for i in range(1, pointLen):
		if points[i].lng > top.lng:
			top = points[i]
		elif points[i].lng < down.lng:
			down = points[i]

		if points[i].lat > right.lat:
			right = points[i]
		elif points[i].lat < left.lat:
			left = points[i]
	point0 = Point(top.lng,  left.lat)
	point1 = Point(top.lng,  right.lat)
	point2 = Point(down.lng, right.lat)
	point3 = Point(down.lng, left.lat)
	polygonBounds = [point0,point1,point2,point3]
	return polygonBounds

def isPointInRect(point, polygonBounds):
	if point.lng >= polygonBounds[3].lng and \
		point.lng <= polygonBounds[0].lng and \
		point.lat >= polygonBounds[3].lat and \
		point.lat <= polygonBounds[2].lat:
		return True
	else:
		return False

# 射线法判断点集里的每个点是否在多边形集内，返回在多边形集内的点集
def isPointsInPolygons(xyset, polygonset):
	inpolygonList = []
	for points in polygonset:
		# 外包矩形
		polygonBounds = getPolygonBounds(points)
		for point in xyset:
			if not isPointInRect(point, polygonBounds):
				print("out of the Rect")
				continue

			pointLen = len(points)
			p = point
			p1 = points[0]
			flag = False

			for i in range(1, pointLen):
				p2 = points[i]
				# 点与多边形顶点重合
				if (p.lng == p1.lng and p.lat == p1.lat) or \
					(p.lng == p2.lng and p.lat == p2.lat):
					print("on the Vertex")
					inpolygonList.append(p)
					break

				# 判断线段两端是否在射线两侧
				if (p2.lat < p.lat and p1.lat >= p.lat) or \
					(p1.lat < p.lat and p2.lat >= p.lat):
					print("on both sides")
					# 线段上与射线y坐标相同的点的x 的坐标
					if p1.lat == p2.lat:
						x = (p1.lng + p2.lng)/2
					else:
						x = p2.lng - (p2.lat - p.lat)*(p2.lng - p1.lng)/(p2.lat - p1.lat) 
					# 点在多边形的边上
					if x == p.lng:
						print("on the edge")
						inpolygonList.append(p)
						break
					# 射线穿过多边形的边界
					if x > p.lng:
						print("throw")
						flag = not flag
					else:
						pass

				else:
					pass

				p1 = p2
			
			if flag:
				inpolygonList.append(p)
	return inpolygonList		

def polygon():
	xyset = []
	polygonset = []

	# 加载所有多边形到polygonset

	polyList = ["116.325011 31.068331 116.441755 31.525895 117.184675 31.290317 116.882203 30.927891 116.500131 31.086453 116.325011 31.068331",
				"116.393091 39.921916 116.393413 39.914510 116.393091 39.921916"]
	for line in polyList:
		strList = line.strip().split()
		# print('strList:',strList)
		pointsLen = len(strList)
		if pointsLen%2 != 0:
			print('error: invalid pointsLen:', pointsLen)
			continue

		points = []
		for i in range(0,pointsLen,2):
			axesPoint = Point(float(strList[i]),float(strList[i+1]))	
			points.append(axesPoint)
		midAxes = int(pointsLen/2) - 1
		if (points[0].lng != points[midAxes].lng or \
			points[0].lat != points[midAxes].lat):
			# print('points[0].lng:',points[0].lng)
			# print('points[0].lat:',points[0].lat)
			# print('points[midAxes].lng:',points[midAxes].lng)
			# print('points[midAxes].lat:',points[midAxes].lat)
			continue
		polygonset.append(points)	
		# print('polygonset:', polygonset)

	# 加载map的所有输入点到点集xyset
	xyList = ["116.860971 31.467001","116.256027 32.074063","116.616875 31.195181"]
	for line in xyList:
		xy = line.strip().split()
		if len(xy) != 2:
			continue
		try:
			x = float(xy[0])
			y = float(xy[1])
		except ValueError:
			continue
		point = Point(x,y)
		xyset.append(point)		

	if len(xyset) == 0:
		sys.exit(0)

	inpolygonList = isPointsInPolygons(xyset, polygonset)

	for point in inpolygonList:
		point.show()


if __name__ == '__main__':
	polygon()














