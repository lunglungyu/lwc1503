# filter out 76 position data as file
# 
allDist = {}
with open('stationData.txt') as f:
	for line in f:
		line = line.rstrip().split(',')
		allDist[line[0]] = [line[2], line[3]]

pos76 = {}
for s in stationList:
	tmp_s = s.replace('-','')
	data = allDist[tmp_s]
	pos = {}
	pos['lng'] = data[0]
	pos['lat'] = data[1]
	pos76[s] = pos
with open('76position.txt', 'w') as f:
	f.write('station,lng,lat')
	for s in pos76:
		rec = [s, pos76[s]['lng'], pos76[s]['lat'] ]
		f.write('\n')
		f.write(','.join(rec))
