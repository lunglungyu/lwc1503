import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import csv
import calendar
TSLength = 30		# Time series length
interval = 5		# interval to take next Time Series
yeardayMax = 365
startYear = 2004
numOfYear = 10
MAXLAG = 5
Threshold = 0.05
print 'Time Series Length:', TSLength
print 'Interval:', interval
oneDay = dt.timedelta(days = 1)
keyMMDD = [] 
firstDay = dt.date(startYear,1,1)
periods = (yeardayMax - TSLength) / interval + 1	# no. of TS in the year
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
    keyMMDD.append("%02d"%m1 + "-" + "%02d"%d1)
    y2 = ppLastDay.year
    m2 = ppLastDay.month
    d2 = ppLastDay.day
    print ppStartDay
    #print ppLastDay
print keyMMDD
# we need the key when print final table to retrieve from record


