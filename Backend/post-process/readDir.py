# read general directions file

startYear = 2003
lastYear = 2012

GenDir = {}

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
	header = f.readline().split(',')
	print header
	for line in f:
		line = line.rstrip()
		rec = {}
		for i in range(len(header)):
			rec[header[i]] = line[i]
		s = rec['station']
		date = rec['date']
		yy = int(date.split('-')[0])
		mmdd = date[5:]
		#tmp_dir = {'angle': rec['angle'],
		#		   'angle_1': rec['angle_1'],
		#		   'angle_2': rec['angle_2'],
		#		   }
		GenDir[yy][s][mmdd] = rec

		