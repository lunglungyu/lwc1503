# read general directions file
import os
import datetime as dt

startYear = 2003
lastYear = 2012

GenDir = {}

def str2bool(a):
	if a == 'True':
		return True
	elif a == 'False':
		return False
	else:
		print 'Error: Invalid str2bool operation.'

# 76 stations
stationList = []
with open('fypCutStation') as f:
	for line in f:
		line = line.rstrip()
		stationList.append(line)

#initialize
for yy in range( startYear, lastYear+1 ):
	GenDir[yy] = {}
	for s in stationList:
		GenDir[yy][s] = {}

with open('generalDirections.txt') as f:
	header = f.readline().rstrip().split(',')
	for line in f:
		line = line.rstrip().split(',')
		rec = {}
		for i in range(len(header)):
			rec[header[i]] = line[i]
			if i in [2,3,4,7]:
				rec[header[i]] = float(rec[header[i]])
			if i==5:
				rec[header[i]] = int(rec[header[i]])
			if i==6:
				rec[header[i]] = str2bool(rec[header[i]])
		s = rec['station']
		date = rec['date']
		yy = int(date.split('-')[0])
		mmdd = date[5:]
		try:
			GenDir[yy][s][mmdd].append( rec )
		except:
			GenDir[yy][s][mmdd] = []
			GenDir[yy][s][mmdd].append( rec )

def DirInfo(recs):
	print len(recs),'dirs'
	for i in range(len(recs)):
		print 'angle:',recs[i]['angle'], 'fromto:', recs[i]['fromto']

		