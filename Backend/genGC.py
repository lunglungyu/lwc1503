import os
import datetime as dt
import numpy as np
import statsmodels.api as sm

#execfile('importFiles.py')
from ccc_gct import hacked_gct

def diff(A, k):
	for i in range(k):
		A = [A[i+1]-A[i] for i in range(len(A)-1)]
	return A

TSLength = 30		# Time series length
interval = 5		# interval to take next Time Series
yeardayMax = 365

startYear = 2003
n_years = 10
MAXLAG = 5

n_total_result = 0
missing_count = 0
year_checked = startYear

print 'starting year:', startYear
print 'last year:', startYear + n_years - 1
print 'Time Series Length:', TSLength
print 'Interval:', interval

start_time = dt.datetime.now()

oneDay = dt.timedelta(days = 1)
# year
for yi in range(n_years):
	result = []
	#if yy != 2003:
	#	break
	yy = startYear + yi
	firstDay = dt.date(yy,1,1)
	periods = (yeardayMax - TSLength) / interval + 1	# no. of TS in the year

	for s1 in stationList:
		#if s1 == '504340-99999': 		# second station
		#	break
		for s2 in stationList:
			if s1 != s2:
				#if s2 != '504340-99999':
				#	break
				for pp in range(periods):
					t1 = []
					t2 = []
					# check if TS is complete
					ppStartDay = firstDay + pp*interval*oneDay
					ppLastDay = ppStartDay + (TSLength-1)*oneDay
					y1 = ppStartDay.year
					m1 = ppStartDay.month
					d1 = ppStartDay.day
					y2 = ppLastDay.year
					m2 = ppLastDay.month
					d2 = ppLastDay.day
					L1 = station[s1][y2][m2][d2]['i'] - station[s1][y1][m1][d1]['i']
					L2 = station[s2][y2][m2][d2]['i'] - station[s2][y1][m1][d1]['i']
					if L1 == TSLength-1 and L2 == L1:
						complete = True
						for i in range(TSLength-2):
							tmp_date = ppStartDay + i*oneDay
							mm = tmp_date.month
							dd = tmp_date.day
							#t1.append(station[s1][yy][mm][dd]['temp'])
							#t2.append(station[s2][yy][mm][dd]['temp'])
							t1.append(station[s1][yy][mm][dd]['diff2'])
							t2.append(station[s2][yy][mm][dd]['diff2'])

					else:
						complete = False
					'''
					complete = True
					for i in range(TSLength):
						tmp_date = firstDay + (pp*TSLength + i)*oneDay
						mm = tmp_date.month
						dd = tmp_date.day
						if not (dd in station[s1][yy][mm] and dd in station[s2][yy][mm]):
							complete = False
							break
						else:
							t1.append(station[s1][yy][mm][dd])
							t2.append(station[s2][yy][mm][dd])
					'''
					# Granger Causality
					if complete:
						#t1_d2 = diff(t1, 2)
						#t2_d2 = diff(t2, 2)
						#x = np.matrix([t2_d2,t1_d2]).T 	# t1 Granger causes t2 ?
						x = np.matrix([t2,t1]).T 	# t1 Granger causes t2 ?
						#x = []
						#for i in range(len(t1_d2)):
						#	x.append([t1_d2[i], t2_d2[i]])
						gcRecord = [s1, s2, str(yy)+'-'+str(ppStartDay.month)+'-'+str(ppStartDay.day)]		# [s1, s2, date]
						#'''
						gc = hacked_gct(x, MAXLAG, verbose=False)	# max lag: 5
						ps = []
						coess = []
						# take Probs, coes
						for j in range(1, MAXLAG+1):
							p = str(gc[j][0]['params_ftest'][1])
							coes = gc[j][1][1].params[1:].tolist()		# to list
							coes = ' '.join([str(ai) for ai in coes])		# list to string
							ps.append(p)
							coess.append(coes)
						gcRecord.extend(ps)
						gcRecord.extend(coess)
						#'''
						result.append(','.join(gcRecord))
						n_total_result += 1
					else:
						missing_count += 1
	tmp_time = dt.datetime.now()
	print 'year checked:', year_checked, ', ', tmp_time - start_time
	# write year data of GC
	output_file = 'result_' + str(start_time.year) + '-' + str(start_time.month) + '-' + str(start_time.day)
	if not os.path.exists(output_file):
		os.makedirs(output_file)
	output_path = os.path.join(output_file, str(year_checked) + '.txt')
	with open(output_path, 'w') as ff:
		for rec in result:
			ff.write(rec)
			ff.write('\n')
	#
	year_checked += 1
end_time = dt.datetime.now()

print 'Done.'
print 'time consumed:', end_time - start_time
print 'number of results:', n_total_result
print 'number of incomplete time series:', missing_count

