# remove single general direction
import os
import datetime as dt

#execfile( 'readDir.py ')

inFile = 'generalDirections.txt'
outFile = 'continuous_generalDirections.txt'

maxFriendAngle = 30

startYear = 2003
n_year = 1
lastYear = startYear+n_year-1
interval = 5

original_count = 0
count = 0

print 'remove Dir that is alone'
print 'read file:', inFile
print 'save file:', outFile

def angleDiff(a, b):
	# in degree
	return min(abs(a-b), abs(a+360-b)%360)

outData = []
oneDay = dt.timedelta(days = 1)
for yy in range( startYear, lastYear+1 ):
	#lines = []		# data for f.write
	#with open(inFile) as fin:
	#	for line in fin:
	#		lines.append(line)
	ss = sorted( GenDir[yy].keys() )
	for s in ss:
		#print 'station:', s
		mmdds = sorted( GenDir[yy][s].keys() )
		for mmdd in mmdds:
			# for each Dir, check if it has friend
			#print 'check mmdd:',mmdd
			for this_dir in GenDir[yy][s][mmdd]:
				#print "dir:", this_dir['angle'], ', fromto:', this_dir['fromto']
				this_angle = this_dir['angle']
				friend = 0
				mm = int(mmdd.split('-')[0])
				dd = int(mmdd.split('-')[1])
				tmp_date = dt.date( yy, mm, dd )
				prev_date = tmp_date - interval*oneDay
				prev_mmdd = '-'.join([str(prev_date.month), str(prev_date.day)])
				#print 'prev date:', prev_date
				next_date = tmp_date + interval*oneDay
				next_mmdd = '-'.join([str(next_date.month), str(next_date.day)])
				#print 'next date:', next_date
				# if not first TS (200x-1-1)
				if prev_date.year == yy and prev_mmdd in GenDir[yy][s]:
					#print 'not first TS'
					# for each dir, if one of them has similar angle to this
					for tmp_dir in GenDir[yy][s][prev_mmdd]:
						tmp_angle = tmp_dir['angle']
						#print 'compare angle:', tmp_angle
						# if tmp_dir is in acceptable angle change
						if angleDiff( this_angle, tmp_angle ) < maxFriendAngle:
							# has friend dir
							friend += 1
							break
				# if not last TS (200x-12-5)
				if next_date.year == yy and next_mmdd in GenDir[yy][s]:
					#print 'not last TS'
					for tmp_dir in GenDir[yy][s][next_mmdd]:
						tmp_angle = tmp_dir['angle']
						#print 'compare angle:', tmp_angle
						if angleDiff( this_angle, tmp_angle ) < maxFriendAngle:
							friend += 1
							break
				if friend > 0:
					# not alone Dir, f.write
					outData.append(this_dir)
with open(outFile, 'w') as f:
	f.write('station,date,angle,angle_1,angle_2,str,fromto,dist')
	for rec in outData:
		output = [
				  rec['station'],
				  rec['date'],
				  str(rec['angle']), 
				  str(rec['angle_1']), 
				  str(rec['angle_2']), 
				  str(rec['str']), 
				  str(rec['fromto']), 
				  str(rec['dist'])
				  ]
		f.write('\n')
		f.write(','.join(output))
print 'no. of new Dirs:', len(outData)