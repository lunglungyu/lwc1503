import os
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

#execfile('readDir.py')
#execfile('readGCs.py')

startYear = 2003
n_year = 10
endYear = startYear+n_year-1
interval = 5
TS_Length = 30

oneDay = dt.timedelta(days = 1)
# plot
fig = plt.figure()
fig2 = plt.figure()
ax = fig.add_subplot(111)
ax2 = fig2.add_subplot(111)
months = mdates.MonthLocator()
monthsFmt = mdates.DateFormatter('%b')

for yy in range(startYear, endYear+1):
	year_genDir_count = {}
	year_genDir_count['date'] = []
	year_genDir_count['count'] = []
	year_ratio_count = []	# ratio of GenDir to GCs
	mmdds = []
	firstDay = dt.date(yy,1,1)
	i_TS = 0
	while True:
		tmp_day = firstDay + i_TS*interval*oneDay
		tmp_last_day = tmp_day + TS_Length*oneDay
		if tmp_last_day.year != yy:
			break
		mmdd = str(tmp_day.month) + '-' + str(tmp_day.day)
		mmdds.append( mmdd )
		i_TS += 1

	for mmdd in mmdds:
		genDir_count = 0
		gc_count = 0
		for s in GenDir[yy]:
			if mmdd in GenDir[yy][s]:
				genDir_count += len( GenDir[yy][s][mmdd] )
		mm = int(mmdd.split('-')[0])
		dd = int(mmdd.split('-')[1])
		date = dt.date(2000,mm,dd)
		#year_genDir_count['date'].append( '2000-'+mmdd )
		# dd/mm/yy
		mmddyy = str(mm)+'/'+str(dd)+'/2000'
		year_genDir_count['date'].append( mdates.datestr2num(mmddyy) )
		year_genDir_count['count'].append( genDir_count )
		#print str(yy)+'-'+mmdd+':', genDir_count
		#if genDir_count == 0:
		#	print str(yy)+'-'+mmdd

		# count GCs
		for s1 in gcFromTo[yy]:
			if mmdd in gcFromTo[yy][s1]:
				gc_count += len( gcFromTo[yy][s1][mmdd].keys() )
		ratio = genDir_count / float(gc_count)
		year_ratio_count.append( ratio )

	#plot
	x = year_genDir_count['date']
	y = year_genDir_count['count']
	ax.plot_date( x, y, fmt='.-', label=str(yy) )

	y2 = year_ratio_count
	ax2.plot_date( x, y2, fmt='.-', label=str(yy) )

## tune plot
# month label
ax.xaxis.set_major_locator( months )
ax.xaxis.set_major_formatter( monthsFmt )
ax2.xaxis.set_major_locator( months )
ax2.xaxis.set_major_formatter( monthsFmt )

datemin = dt.date(2000,1,1)
datemax = dt.date(2000,12,1)
ax.set_xlim(datemin, datemax)
ax2.set_xlim(datemin, datemax)
ax.set_title( 'No. of general Granger causality' )
ax2.set_title( 'GGC to GCs ratio' )
ax.set_xlabel( 'Date' )
ax2.set_xlabel( 'Date' )
# legend
box = ax.get_position()
ax.set_position( [box.x0, box.y0, box.width * 0.83, box.height] )
ax2.set_position( [box.x0, box.y0, box.width * 0.83, box.height] )
lgd = ax.legend( bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=2 )
lgd2 = ax2.legend( bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=2 )
plt.show()

ax.axvline( x=mdates.datestr2num('04/01/2000') )
ax.axvline( x=mdates.datestr2num('09/01/2000') )
