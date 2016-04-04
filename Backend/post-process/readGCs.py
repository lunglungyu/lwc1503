import os
import datetime as dt
import numpy as np
import statsmodels.api as sm

inFolder = os.path.join('..','Data','continuous_light_d30_i5_2003_2012')
startYear = 2003
lastYear = 2012

#print 'Read folder:', inFolder
# read year files
gcFromTo = {}		# gcFromTo[yy][s1][mmdd][s2] = p
gcToFrom = {}
stationDict = {}	# stationDict[s1][s2,yy-mm-dd] = p
stationList = []

# 76 datas
with open('fypCutStation') as f:
	for line in f:
		line = line.rstrip()
		stationList.append(line)

# initialize dict
for yy in range( startYear, lastYear+1 ):
	gcFromTo[yy] = {}
	gcToFrom[yy] = {}
	for s in stationList:
		gcFromTo[yy][s] = {}
		gcToFrom[yy][s] = {}
for s in stationList:
	stationDict[s] = {}

for yy in range( startYear, lastYear+1 ):
	readPath = os.path.join( inFolder, str(yy)+'.txt' )
	with open( readPath ) as fin:
		for line in fin:
			tmp = line.split(',')
			#rawGCs.append(tmp)
			s1 = tmp[0]
			s2 = tmp[1]
			mmdd = tmp[2][5:]
			p = tmp[3:8]
			try:
				gcFromTo[yy][s1][mmdd][s2] = p
			except:
				gcFromTo[yy][s1][mmdd] = {}
				gcFromTo[yy][s1][mmdd][s2] = p


			try:
				gcToFrom[yy][s2][mmdd][s1] = p
			except:
				gcToFrom[yy][s2][mmdd] = {}
				gcToFrom[yy][s2][mmdd][s1] = p

			s2_date = ','.join(tmp[1:3])
			stationDict[s1][s2_date] = p



