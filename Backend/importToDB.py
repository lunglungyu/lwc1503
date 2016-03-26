import MySQLdb
conn = MySQLdb.connect(
                        host="127.0.0.1",
                        user="root",
                        passwd="fyp",
                        db="lwc1503"
                     )
cur = conn.cursor()
print 'connected'
for i in xrange(2003,2013):
    fileName = 'd30_i5_2003_2012/'+ str(i) +'.txt'
    print fileName
    with open(fileName,'r') as FileObj:
        for line in FileObj:
            wholeline = line.split(',')
            wholeline = wholeline[:8]
            cur.execute("INSERT INTO pythonResult(station1, station2, startDate, p1, p2, p3, p4, p5) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", wholeline)
            print wholeline
            #print lines # or do some other thing with the line...
    conn.commit()
#for data in your_data_list:
    #cur.execute("data you want to insert: %s" %data)
conn.close()
