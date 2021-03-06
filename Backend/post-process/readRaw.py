import os
import datetime as dt

readFileName = '76raw.txt'
yearStartImport = 2003		# first year
yearsImport = 10
stationList = []
data = {}

def isLeap(yy):
	c1 = dt.date(yy,1,1)
	c2 = dt.date(yy+1,1,1)
	if (c2-c1).days ==  366:
		return True
	return False

def diff(A, k):
	for i in range(k):
		for i in range(len(A)-1):
			if A[i] != None and A[i+1] != None:
				A[i] = A[i+1] - A[i]
			else:
				A[i] = None
		del A[-1]
		#A = [A[i+1]-A[i] for i in range(len(A)-1)]
	return A

# 76 datas
with open('fypCutStation') as f:
	for line in f:
		line = line.rstrip()
		stationList.append(line)

oneDay = dt.timedelta(days = 1)
# initialize dict
for s in stationList:
	data[s] = {}
	for yi in range(yearsImport):		# 2003-2012
		y = yearStartImport + yi
		data[s][y] = {}
		for mi in range(12):
			m = mi + 1
			data[s][y][m] = {} 
		if isLeap(y):
			max_dd = 366
		else:
			max_dd = 365
		for di in range(max_dd):
			tmp_date = dt.date(y,1,1) + di*oneDay
			m = tmp_date.month
			d = tmp_date.day
			data[s][y][m][d] = {}
			data[s][y][m][d]['i'] = -1

with open(readFileName) as fin:
	for line in fin:
		line = line.rstrip()
		line = line.split(',')
		for i in range(1,4):
			line[i] = int(line[i])
		s = line[0]
		y = line[1]
		m = line[2]
		d = line[3]
		if line[4] != 'None':
			line[4] = float(line[4])
		else:
			line[4] = None
		data[s][y][m][d]['temp'] = line[4]


for s in data:
	for yy in data[s]:
		firstDay = dt.date(yy,1,1)
		if isLeap(yy):
			yearDays = 366
		else:
			yearDays = 365
		TS = []
		for di in range(yearDays):
			tmp_date = firstDay + di*oneDay
			mm = tmp_date.month
			dd = tmp_date.day
			TS.append(data[s][yy][mm][dd]['temp'])
		TS = diff(TS, 2)
		TS.append(None)
		TS.append(None)
		for mm in data[s][yy]:
			for dd in data[s][yy][mm]:
				dayIndex = (dt.date(yy,mm,dd) - firstDay).days
				data[s][yy][mm][dd]['diff2'] = TS[dayIndex]