# filter out 76 position data as file
# 
pos76 = {}
with open('76position.txt') as f:
	f.readline()
	for line in f:
		line = line.rstrip().split(',')
		s = line[0]
		pos = {}
		pos['lng'] = float(line[1])
		pos['lat'] = float(line[2])
		pos76[s] = pos