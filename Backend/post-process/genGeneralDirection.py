import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import math

#
# find arrows !
# for year,
# 		for station,
# 			for date,
# 				- find all gc
# 				- calculate arrows
# 					- 
#

yearStart = 2003
n_year = 1
yearEnd = yearStart+n_year-1

minArrowGC = 4
maxAngle = 30

#execfile( 'readGCs.py' )
#execfile( 'read76position.py' )

def bearing ( lat1, lng1, lat2, lng2 ):
	# in radian
	dLon = lng2 - lng1
	x = math.cos( lat1 )*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
	y = math.sin( dLon ) * math.cos( lat2 )
	brng = toDegree( math.atan2( y, x ))
	return 360 - ((brng + 360) % 360)

def toRadian( deg ):
	return deg * math.pi / 180

def toDegree( radian ):
	return radian * 180 / math.pi

def isSmallAngle( a1, a2, threshold ):
	diff = abs(a1 - a2)
	if diff > threshold and 360 - diff > threshold:
		return False
	else:
		return True

# 1. find 
# 
all_gcData = {}

kk = 0
for yy in range(yearStart, yearEnd+1):
	for s1 in gcFromTo[yy]:
		for mmdd in gcFromTo[yy][s1]:
			# for a given s1, mmdd,
			# store all GC records first
			s1 = '548080-99999'
			yy = 2003
			mmdd = '7-10'

			tmp_gcData = []		# tmp_gcData[i] = [s1,s2,p1_pos, p2_pos, fromto]
			# store all out GCs
			for s2 in gcFromTo[yy][s1][mmdd]:
				single_gc = {}
				single_gc['s1'] = s1
				single_gc['s2'] = s2
				single_gc['p1_pos'] = pos76[s1]
				single_gc['p2_pos'] = pos76[s2]
				single_gc['fromto'] = True
				tmp_gcData.append( single_gc )
			# store all in GCs
			for s2 in gcToFrom[yy][s1][mmdd]:
				single_gc = {}
				single_gc['s1'] = s1
				single_gc['s2'] = s2
				single_gc['p1_pos'] = pos76[s1]
				single_gc['p2_pos'] = pos76[s2]
				# check if there is also a out GC to s2
				if s2 not in gcFromTo[yy][s1][mmdd]:
					single_gc['fromto'] = False
					tmp_gcData.append( single_gc )

			# remove bidirectional from tmp_gcData first
			i = 0
			while i < len(tmp_gcData):
				if tmp_gcData[i]['fromto'] == None:
					del tmp_gcData[i]
				else:
					i += 1

			# calculate angle
			for single_gc in tmp_gcData:
				lng1 = toRadian( single_gc['p1_pos']['lng'] )
				lat1 = toRadian( single_gc['p1_pos']['lat'] )
				lng2 = toRadian( single_gc['p2_pos']['lng'] )
				lat2 = toRadian( single_gc['p2_pos']['lat'] )
				single_gc['angle'] = bearing( lat1, lng1, lat2, lng2 )

			tmp_gcData.sort(key=lambda rec: rec['angle'])
			n_gcData = len(tmp_gcData)
			tmp_gcData.extend(tmp_gcData)	# repeat the data

			outGCseq = [0 for i in range(n_gcData)]
			inGCseq = [0 for i in range(n_gcData)]

			outDirs = []
			inDirs = []
			print n_gcData
			# 1. mark sequence
			for i in range(len(tmp_gcData)):
				if tmp_gcData[i]['fromto'] == True:
					if i == 0:
						outGCseq[ i%n_gcData ] = 1
						inGCseq[ i%n_gcData ] = 0
					else:
						previous_same_gc = (outGCseq[ (i-1)%n_gcData ] > 0)
						a1 = tmp_gcData[i-1]['angle']
						a2 = tmp_gcData[i]['angle']
						if (previous_same_gc) and (not isSmallAngle(a1, a2, maxAngle)):
							outGCseq[ i%n_gcData ] = 0
						else:
							outGCseq[ i%n_gcData ] = outGCseq[ (i-1)%n_gcData ] + 1
						inGCseq[ i%n_gcData ] = 0
				elif tmp_gcData[i]['fromto'] == False:
					if i == 0:
						outGCseq[ i%n_gcData ] = 0
						inGCseq[ i%n_gcData ] = 1
					else:
						previous_same_gc = (inGCseq[ (i-1)%n_gcData ] > 0)
						a1 = tmp_gcData[i-1]['angle']
						a2 = tmp_gcData[i]['angle']
						if (previous_same_gc) and (not isSmallAngle(a1, a2, maxAngle)):
							inGCseq[ i%n_gcData ] = 0
						else:
							inGCseq[ i%n_gcData ] = inGCseq[ (i-1)%n_gcData ] + 1
						outGCseq[ i%n_gcData ] = 0
			print outGCseq
			print inGCseq
			# find valid subsequence (1,2,3,...)
			def findGeneralDirections( gcData, seq, minCount, fromto ):
				result = []
				n = len(seq)
				for i in range(len(seq)):
					if seq[i] == 0:
						count = seq[ (i-1+n)%n ]
						first_angle = gcData[ (i-count+n)%n ]['angle']
						if count >= minCount:
							angleSum = 0
							tmp_angle_list = []
							for j in range(count):
								tmp_angle = gcData[ (i-count+j+n)%n ]['angle']
								tmp_angle_list.append( tmp_angle )
								relative_angle = (tmp_angle + 360 - first_angle)%360
								angleSum += relative_angle
							angleAvg = (angleSum/count + first_angle)%360
							datum = {}
							datum['dir'] = angleAvg
							datum['str'] = count
							datum['fromto'] = fromto
							result.append( datum )
				return result

			outDirs = findGeneralDirections( tmp_gcData, outGCseq, minArrowGC, True )
			inDirs = findGeneralDirections( tmp_gcData, inGCseq, minArrowGC, False )
			print outDirs
			print inDirs
			break
		break


