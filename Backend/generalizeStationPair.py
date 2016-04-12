import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import csv
import calendar
def getAllFilesRecursive(root):
    files = [ join(root,f) for f in listdir(root) if isfile(join(root,f))]
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                files.append(join(root,f))
    return files
Threshold_low = 3
Threshold_high = 7
# 4<=x<=6  middle relation for 10 year
TSLength = 30		# Time series length
interval = 5		# interval to take next Time Series
yeardayMax = 365
startYear = 2003
numOfYear = 10
MAXLAG = 5
Threshold = 0.05
pair_directory = "../QueryAndImportantData/pairData_p12345"
output_directory = r'../QueryAndImportantData/output_pairData_p12345_general'
d = output_directory
if not os.path.exists(d):
    os.makedirs(d)
    print 'create outputFileDirectory'
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
    keyMMDD.append("%02d"%m1 + "-" + "%02d"%d1)
    y2 = ppLastDay.year
    m2 = ppLastDay.month
    d2 = ppLastDay.day
    #print ppStartDay
    #print ppLastDay
print keyMMDD
info = []
for dirname, dirnames, filenames in os.walk(pair_directory):
    print filenames
    for filename in filenames:
        info.append(filename)
        print filename
        if filename == '.DS_Store':
            continue
        #print os.path.splitext(filename)
        #if os.path.splitext(filename) != '.csv':
        #    continue
        readFileName = os.path.join(pair_directory, filename)
        outputFileName = os.path.join(output_directory, r'output_'+filename)
        print readFileName , " -> " , outputFileName
        #print readFileName +","+ outputFileName
        #print(os.path.join(dirname, r'output_'+filename))
#print info
# we need the key when print final table to retrieve from record
        outputDict = {}
        with open(readFileName, "r") as ins:
            array = []
            for line in ins:
                #print line
                line = line.rstrip('\n\r')
                line = line.rstrip('\r')
                line = line.rstrip('\n')
                arr = line.split(",")
                p1 = float(arr[4][1:-1])
                p2 = float(arr[5][1:-1])
                p3 = float(arr[6][1:-1])
                p4 = float(arr[7][1:-1])
                p5 = float(arr[8][1:-1])
                ymd = arr[3][1:-1]
                yy,mm,dd = ymd.split("-")
                thisKey  = mm+"-"+dd
                #print thisKey
                # fix
                oneDay = dt.timedelta(days = 1)
                thisDay = dt.date(int(yy),int(mm),int(dd))
                #
                if calendar.isleap(int(yy)) and int(mm)>=3:
                    thisDay = thisDay + oneDay
                    thisKey = '%02d'% thisDay.month + '-' + '%02d' % thisDay.day
                    #print 'leap fix key:'+ thisKey
                if thisKey in outputDict:
                    if p5<= Threshold:
                        outputDict[thisKey] += 1
                    else:
                        pass
                else:
                    if p5<= Threshold:
                        outputDict[thisKey] = 1
                    else:
                        outputDict[thisKey] = 0

        with open(outputFileName, 'wb') as out:
            writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
            header = [r'StartDate',r'Count',r'Class']
            writer.writerow(header)
            for kk in keyMMDD:
                row = []
                row.append(kk)
                row.append(outputDict[kk])
                if outputDict[kk]<=Threshold_low:
                    row.append('L')
                elif outputDict[kk]>=Threshold_high:
                    row.append('H')
                else:
                    row.append('M')
                print row
                writer.writerow(row)


