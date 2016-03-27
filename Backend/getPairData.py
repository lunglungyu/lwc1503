import MySQLdb as dbapi
import sys
import csv
dbServer='127.0.0.1'
dbPass='fyp'
dbUser='root'
dbQuery='SELECT * FROM pbTest.Orders;'
pairFile = r'pairTest.csv'

db=dbapi.connect(host=dbServer,user=dbUser,passwd=dbPass)
cur=db.cursor()
f = open(pairFile, 'r')  
for row in csv.reader(f):  
    print row  
    #cur.execute(dbQuery)
    #result=cur.fetchall()

    #fileName = 
    #outputFileName = ""
    #c = csv.writer(open(outputFileName,"wb"))
    #c.writerow(result)
f.close()  
