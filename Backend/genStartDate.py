# run with a non leap year is *** importan *** to get standardize start date,  leap year will be fixed in other processing
import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import csv
import calendar
TSLength = 30		# Time series length
interval = 5		# interval to take next Time Series
yeardayMax = 365
startYear = 2003
numOfYear = 10
MAXLAG = 5
Threshold = 0.05
print 'Time Series Length:', TSLength
print 'Interval:', interval
oneDay = dt.timedelta(days = 1)
keyMMDD = [] 
firstDay = dt.date(startYear,1,1)
periods = (yeardayMax - TSLength) / interval + 1	# no. of TS in the year
out = open(r"startDate.csv", 'wb')
writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
header = ['startDate']
writer.writerow(header)
for pp in range(periods):
    ppStartDay = firstDay + pp*interval*oneDay
    ppLastDay = ppStartDay + (TSLength-1)*oneDay
    y1 = ppStartDay.year
    m1 = ppStartDay.month
    d1 = ppStartDay.day
    #if calendar.isleap(y1) and m1>=3:
    #    ppStartDay = ppStartDay - oneDay
    #    ppLastDay = ppStartDay + (TSLength-1)*oneDay
    #    y1 = ppStartDay.year
    #    m1 = ppStartDay.month
    #    d1 = ppStartDay.day
    mmddStr = "%02d"%m1 + "-" + "%02d"%d1
    row = [mmddStr]
    writer.writerow(row)
    keyMMDD.append(mmddStr)
    y2 = ppLastDay.year
    m2 = ppLastDay.month
    d2 = ppLastDay.day
    print ppStartDay
    #print ppLastDay
print keyMMDD
# we need the key when print final table to retrieve from record


