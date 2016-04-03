import os
import datetime as dt
import numpy as np
import statsmodels.api as sm

inFolder = os.path.join('..','Data','continuous_light_d30_i5_2003_2012')
startYear = 2003
lastYear = 2012

#print 'Read folder:', inFolder
# read year files
gcFromTo = {}
gcToFrom = {}
rawGCs = []

# 76 datas
with open('fypCutStation') as f:
	for line in f:
		line = line.rstrip()
		dataList.append(line)

# initialize dict
for yy in range( startYear, lastYear+1 ):
	gcFromTo[yy] = {}
	gcToFrom[yy] = {}
	for s in dataList:
		gcFromTo[yy][s] = {}
		gcToFrom[yy][s] = {}
	'''
	for y in range( startYear, lastYear+1 ):
		gcFromTo[s][y] = {}
		for m in range( 1, 13 ):
			gc[s][y][m] = {}'''

for yy in range( startYear, lastYear+1 ):
	readPath = os.path.join( inFolder, str(yy)+'.txt' )
	with open( readPath ) as fin:
		for line in fin:
			tmp = line.split(',')
			rawGCs.append(tmp)
			s1 = tmp[0]
			s2 = tmp[1]
			mmdd = tmp[2][5:]

			try:
				gcFromTo[yy][s1][s2][mmdd] = tmp[3:8]
			except:
				gcFromTo[yy][s1][s2] = {}
				gcFromTo[yy][s1][s2][mmdd] = tmp[3:8]


			try:
				gcFromTo[yy][s2][s1][mmdd] = tmp[3:8]
			except:
				gcFromTo[yy][s2][s1] = {}
				gcFromTo[yy][s2][s1][mmdd] = tmp[3:8]



