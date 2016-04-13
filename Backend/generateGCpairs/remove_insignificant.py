#
# Remove record with no significant GC
#

import os

inFolder = 'd30_i5_2003_2012'
outFolder = 'light_' + inFolder

startYear = 2003
lastYear = 2012

original_count = 0
count = 0

print 'read folder:', inFolder
print 'save folder:', outFolder

for yy in range(startYear, lastYear+1):
	data = []
	readPath = os.path.join(inFolder, str(yy)+'.txt')
	savePath = os.path.join(outFolder, str(yy)+'.txt')
	with open(readPath) as fin:
		for line in fin:
			original_count += 1
			tmp = line.split(',')
			valid = False
			for i in range(3,8):
				if float(tmp[i]) < 0.05:
					valid = True
					break
			if valid:
				data.append(line)
				count += 1
	if not os.path.exists(outFolder):
		os.makedirs(outFolder)
	with open(savePath, 'w') as fout:
		for rec in data:
			fout.write(rec)

print 'Done.'
print 'no. of original records:', original_count
print 'no. of significant records:', count