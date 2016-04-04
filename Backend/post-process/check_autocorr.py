# calculate autocorrelation of TS that has bidirection GC with other stations
# * check "tau" for shift >= 2
# * 
#   ---------------- Result  ----------------
# time consumed: 0:02:50.727000
# histogram 1: "tau"s of TSs with bidirection GC
# histogram 2: "tau"s of TSs without bi-GC
# temperature TS without diff2):
# mean 1: 0.40143
# mean 2: 0.41016
# 
# temperature TS with diff2):
# mean for bi-GC TSs autocorr at "tau": 0.354657668643
# mean for all-GC TSs autocorr at "tau": 0.345854893035
#
# No significant difference between them :(

import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

start_time = dt.datetime.now()

#execfile( 'readRaw.py' )
#execfile( 'readGCs.py' )

def getTempTS(s1, yy, mm, dd, length=30):
	TS = []
	yy = int(yy)
	mm = int(mm)
	dd = int(dd)
	oneDay = dt.timedelta(days = 1)
	for i in range(length):
		tmpDate = dt.date(yy,mm,dd) + i*oneDay
		mi = tmpDate.month
		di = tmpDate.day
		TS.append(data[s1][yy][mi][di]['temp'])
	return TS

def getTempDiffTS(s1, yy, mm, dd, length=28):
	TS = []
	yy = int(yy)
	mm = int(mm)
	dd = int(dd)
	oneDay = dt.timedelta(days = 1)
	for i in range(length):
		tmpDate = dt.date(yy,mm,dd) + i*oneDay
		mi = tmpDate.month
		di = tmpDate.day
		TS.append(data[s1][yy][mi][di]['diff2'])
	return TS
'''
bidirection_list = {}
bidirection_count = 0
# find bidirection pairs
for s1 in stationDict:
	for rec in stationDict[s1]:
		s2 = rec.split(',')[0]
		date = rec.split(',')[1]
		rec2 = ','.join([s1,date])
		if rec2 in stationDict[s2]:
			if ','.join([s2,s1,date]) not in bidirection_list:
				bidirection_list[','.join([s1,s2,date])] = 1
				bidirection_count += 1
print "number of bidirection GC:", bidirection_count
'''

# bidirection GC TS autocorr
autocorr_list = []
autocorr = sm.tsa.stattools.acf
recs = bidirection_list.keys()
print 'calculate autocorr_list...'
for i in range(len(recs)):
	recs[i] = recs[i].split(',')
	recs[i] = ','.join([recs[i][0],recs[i][2],recs[i][1]])
recs.sort()

date = None
for rec in recs:
	tmp = rec.split(',')[1:]
	s1 = rec.split(',')[0]
	s2 = tmp[1]
	if tmp[0] != date:
		#print s1,date
		date = tmp[0]
		yy = date.split('-')[0]
		mm = date.split('-')[1]
		dd = date.split('-')[2]
		ts1 = getTempDiffTS(s1, yy, mm, dd)
		yo1 = abs(autocorr(ts1))
	ts2 = getTempDiffTS(s2, yy, mm, dd)
	yo2 = abs(autocorr(ts2))
	autocorr_list.append(max(yo1[2:]))
	autocorr_list.append(max(yo2[2:]))

# try all normal GCs TS autocorr
all_autocorr_list = []
print 'calculate all_autocorr_list...'
for s1 in stationDict:
	date = None
	recs = stationDict[s1].keys()
	recs = [','.join( rec.split(',')[::-1] ) for rec in recs]
	recs.sort()
	#print recs
	for i in range(len(recs)):

		tmp = recs[i].split(',')
		#print tmp
		s2 = tmp[1]
		if tmp[0] != date:
			#print s1,date
			date = tmp[0]
			yy = date.split('-')[0]
			mm = date.split('-')[1]
			dd = date.split('-')[2]
			ts1 = getTempDiffTS(s1, yy, mm, dd)
			yo1 = abs(autocorr(ts1))
		ts2 = getTempDiffTS(s2, yy, mm, dd)
		yo2 = abs(autocorr(ts2))
		all_autocorr_list.append(max(yo1[2:]))
		all_autocorr_list.append(max(yo2[2:]))


end_time = dt.datetime.now()
print 'time consumed:', end_time - start_time
print 'mean for bi-GC TSs autocorr at "tau":', np.mean(autocorr_list)
print 'mean for all-GC TSs autocorr at "tau":', np.mean(all_autocorr_list)
# run in console to see histogram

#plt.hist(autocorr_list, 1000);
#plt.hist(all_autocorr_list, 1000);