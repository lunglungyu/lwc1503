import os
import datetime as dt
import numpy as np
import statsmodels.api as sm
import calendar
import numpy as np
import matplotlib.pyplot as plt
def getAllFilesRecursive(root):
    files = [ join(root,f) for f in listdir(root) if isfile(join(root,f))]
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                files.append(join(root,f))
    return files

TSLength = 30		# Time series length
interval = 5		# interval to take next Time Series
yeardayMax = 365
startYear = 2003
numOfYear = 10
MAXLAG = 5
Threshold = 0.05
pair_directory = "../QueryAndImportantData/pairData_p12345"
output_directory = r'../stationVisualize/output_pairData_p12345'
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
ind = np.arange(68)
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
        outputFileName = os.path.join(output_directory, r'output_'+filename+'.png')
        print readFileName , " -> " , outputFileName
        #print readFileName +","+ outputFileName
        #print(os.path.join(dirname, r'output_'+filename))
#print info
# we need the key when print final table to retrieve from record
        outputDict = {}
        for i in range(numOfYear):
            yy = str(i+startYear)
            print yy
            outputDict[yy] = {}
        with open(readFileName, "r") as ins:
            array = []
            for line in ins:
                line = line.rstrip('\n\r')
                line = line.rstrip('\r')
                line = line.rstrip('\n')
                #print line
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
                outputDict[yy][thisKey] = p5
        probDict = {}
        plt.figure()
        plt.hold(True)
        for i in range(numOfYear):
            yy = str(i+startYear)
            probDict[yy]=[]
            for kk in keyMMDD:
                #print yy + "," + kk
                if kk not in outputDict[yy]:
                    outputDict[yy][kk] = float('nan')
                probDict[yy].append((outputDict[yy][kk]))
            print probDict[yy]
            plt.plot(ind,probDict[yy])
        plt.savefig(outputFileName)
        #plt.hold(False)
        #plt.show()
