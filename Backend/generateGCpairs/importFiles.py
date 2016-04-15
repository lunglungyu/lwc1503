import os
import datetime as dt
yearStartImport = 2003		# first year
yearsImport = 1
yearLastImport = yearStartImport + yearsImport - 1		# last year

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

# 76 stations
stationList = []
with open('fypCutStation') as f:
	for line in f:
		line = line.rstrip()
		stationList.append(line)
count = 0

oneDay = dt.timedelta(days = 1)
# initialize dict
station = {}
for s in stationList:
	station[s] = {}
	for yi in range(yearsImport):		# 2003-2012
		y = yearStartImport + yi
		station[s][y] = {}
		for mi in range(12):
			m = mi + 1
			station[s][y][m] = {} 
		if isLeap(y):
			max_dd = 366
		else:
			max_dd = 365
		for di in range(max_dd):
			tmp_date = dt.date(y,1,1) + di*oneDay
			m = tmp_date.month
			d = tmp_date.day
			station[s][y][m][d] = {}
			station[s][y][m][d]['i'] = -1

# find those 76 stations files in (2003, 2012)
for filename in os.listdir('ChinaAll'):
	if len(filename) > 18:
		fStation = filename[:12]
		fYear = int(filename[13:17])
		if fStation in stationList and fYear <= yearLastImport and fYear >= yearStartImport:
			# valid data file
			with open(os.path.join('ChinaAll',filename)) as f:
				f.readline()
				count = 0
				for line in f:
					count += 1
					line = line.split(' ')
					while True:
						try:
							line.remove('')
						except:
							break
					tmp_date = line[2]
					yy = int(tmp_date[:4])
					mm = int(tmp_date[4:6])
					dd = int(tmp_date[6:])
					temperature = float(line[3])
					station[fStation][yy][mm][dd]['temp'] = temperature
					station[fStation][yy][mm][dd]['i'] = count

missingList = []
for s in station:
	for yy in station[s]:
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
			if 'temp' in station[s][yy][mm][dd]:
				TS.append(station[s][yy][mm][dd]['temp'])
			else:
				TS.append(None)
				missingList.append(s+', '+str(yy)+'-'+str(mm)+'-'+str(dd))
		TS = diff(TS, 2)
		TS.append(None)
		TS.append(None)
		for mm in station[s][yy]:
			for dd in station[s][yy][mm]:
				dayIndex = (dt.date(yy,mm,dd) - firstDay).days
				station[s][yy][mm][dd]['diff2'] = TS[dayIndex]
