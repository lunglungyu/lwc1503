import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import csv 
execfile('importFilesWithoutCalcLag.py')
TSLength = 30		# Time series length
interval = 1		# interval to take next Time Series
yeardayMax = 365
startYear = 2003
n_years = 4
MAXLAG = 5

n_total_result = 0
missing_count = 0
year_checked = startYear
#print 'starting year:', startYear
#print 'last year:', startYear + n_years - 1
#print 'Time Series Length:', TSLength
#print 'Interval:', interval
start_time = dt.datetime.now()
oneDay = dt.timedelta(days = 1)
# year
for yi in range(n_years):
	yyn = startYear + yi
	firstDay = dt.date(yyn,1,1)
	periods = (yeardayMax - TSLength) / interval + 1	# no. of TS in the year
	for s1 in stationList:
	    result = []
            for pp in range(periods):
                ppStartDay = firstDay + pp*interval*oneDay
                ppLastDay = ppStartDay + (TSLength-1)*oneDay
                #print(ppStartDay)
                gcRecord = [s1,  str(ppStartDay.year)+'-'+str(ppStartDay.month)+'-'+str(ppStartDay.day)]
                y1 = ppStartDay.year
                m1 = ppStartDay.month
                d1 = ppStartDay.day
                y2 = ppLastDay.year
                m2 = ppLastDay.month
                d2 = ppLastDay.day
                for lag in range(1,MAXLAG+1):
                    t1 = []
                    t2 = []
                    # check if TS is complete
                    ppStartDay_lag = firstDay + pp*interval*oneDay  + lag*oneDay
                    ppLastDay_lag = ppStartDay + (TSLength-1)*oneDay + lag*oneDay
                    y1_lag = ppStartDay_lag.year
                    m1_lag = ppStartDay_lag.month
                    d1_lag = ppStartDay_lag.day
                    y2_lag = ppLastDay_lag.year
                    m2_lag = ppLastDay_lag.month
                    d2_lag = ppLastDay_lag.day
                    complete = True
                    try:
                        for i in range(TSLength): # 30 days then
                                tmp_date = ppStartDay + i*oneDay
                                yy = tmp_date.year
                                mm = tmp_date.month
                                dd = tmp_date.day
                                tmp_date_lag = ppStartDay + i*oneDay + lag*oneDay
                                yy_lag = tmp_date_lag.year
                                mm_lag = tmp_date_lag.month
                                dd_lag = tmp_date_lag.day
                                t1.append(station[s1][yy][mm][dd]['temp'])
                                t2.append(station[s1][yy_lag][mm_lag][dd_lag]['temp'])
                    except KeyError:
                        complete = False
                    if len(t1)!=len(t2):
                        complete = False
                    if complete:
                            corr = np.corrcoef(t1,t2)[0,1]
                            gcRecord.append(corr) 
                            #result.append(','.join(gcRecord))
                            n_total_result += 1
                            #print(ppStartDay_lag)
                            #print(t1)
                            #print(t2)
                            #print(corr)
                            #print('----')
                            result.append(gcRecord)
                    else:
                            missing_count += 1
                print(gcRecord)
            f = open(str(s1)+"_corr.csv","a")  
            w = csv.writer(f)  
            w.writerows(result)  
            f.close() 
	#tmp_time = dt.datetime.now()
	#print 'year checked:', year_checked, ', ', tmp_time - start_time
	## write year data of GC
	#output_file = 'result_' + str(start_time.year) + '-' + str(start_time.month) + '-' + str(start_time.day)
	#if not os.path.exists(output_file):
	#	os.makedirs(output_file)
	#output_path = os.path.join(output_file, str(year_checked) + '.txt')
	#with open(output_path, 'w') as ff:
	#	for rec in result:
	#		ff.write(rec)
	#		ff.write('\n')
	#
	year_checked += 1
 
