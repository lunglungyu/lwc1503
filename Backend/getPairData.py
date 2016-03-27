import MySQLdb as dbapi
import sys
import csv
import os
dbServer='127.0.0.1'
dbPass='fyp'
dbUser='root'
dbName = 'lwc1503'
dbQuery='SELECT id,station1,station2,startDate,p1,p2,p3,p4,p5 FROM pythonResult where station1= %s and station2 = %s'
pairFile = r'../QueryAndImportantData/Causality_Pair_p12345.csv'
pairFileDirectory = r'../QueryAndImportantData/pairData/'
d = os.path.dirname(pairFileDirectory)
if not os.path.exists(d):
    os.makedirs(d)
    print 'create pairFileDirectory'
db=dbapi.connect(host=dbServer,user=dbUser,passwd=dbPass,db=dbName)
cur=db.cursor()
f = open(pairFile, 'r')  
for row in csv.reader(f):  
    print row  
    pairCount = int(row[0])
    station1 = row[1]
    station2 = row[2]
    outputFileName = "%04d" %pairCount  + "_" + station1 + "_" + station2 +".csv"
    #print outputFileName
    outputPath = os.path.join(pairFileDirectory,outputFileName)
    print outputPath
    print dbQuery % (station1,station2)
    cur.execute(dbQuery % (station1,station2))
    result=cur.fetchall()
    #lines = []
    #for row in result:
    #    value = str(row)
    #    lines.append(value)
    of = open(outputPath,"wb")
    c = csv.writer(of, delimiter=',', quoting=csv.QUOTE_ALL)
    c.writerows(result)
    of.close()
f.close()  
