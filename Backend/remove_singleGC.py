#
# Remove record that
# both the next and previous TS have no GC for the same station
#
# Assumed all input records have significant GC for at least one of the day lag
#

import os
import datetime as dt

inFolder = 'light_d30_i5_2003_2012'
outFolder = 'continuous_' + inFolder

startYear = 2003
lastYear = 2012
interval = 5

original_count = 0
count = 0

print 'remove GC record that is alone (no GC in next and prev TS)'
print 'read folder:', inFolder
print 'save folder:', outFolder

for yy in range(startYear, lastYear+1):
	lines = []	# data for print
	in_data = []	# data for process
	out_data = []
	readPath = os.path.join(inFolder, str(yy)+'.txt')
	savePath = os.path.join(outFolder, str(yy)+'.txt')
	with open(readPath) as fin:
		for line in fin:
			lines.append(line)
			original_count += 1
			tmp = line.split(',')
			in_data.append(tmp)
	for i in range(len(in_data)):
		# check if alone
		valid = False
		s1 = in_data[i][0]
		s2 = in_data[i][1]
		oneDay = dt.timedelta(days = 1)
		date = in_data[i][2].split('-')
		date = dt.date(int(date[0]), int(date[1]), int(date[2]))
		prev_date = date - interval * oneDay
		next_date = date + interval * oneDay
		# prev
		if i > 0:
			if in_data[i-1][0] == s1 and in_data[i-1][1] == s2:
				tmp_date = in_data[i-1][2].split('-')
				tmp_date = dt.date(int(tmp_date[0]), int(tmp_date[1]), int(tmp_date[2]))
				if tmp_date == prev_date:
					valid = True
		# next 
		if i+1 < len(in_data):
			if in_data[i+1][0] == s1 and in_data[i+1][1] == s2:
				tmp_date = in_data[i+1][2].split('-')
				tmp_date = dt.date(int(tmp_date[0]), int(tmp_date[1]), int(tmp_date[2]))
				if tmp_date == next_date:
					valid = True
		if valid:
			out_data.append(lines[i])
			count += 1
	if not os.path.exists(outFolder):
		os.makedirs(outFolder)
	with open(savePath, 'w') as fout:
		for rec in out_data:
			fout.write(rec)

print 'Done.'
print 'no. of original records:', original_count
print 'no. of non-single records:', count