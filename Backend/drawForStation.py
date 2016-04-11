import matplotlib.pyplot as plt
import numpy as np
import csv
import os
folder_path ="../QueryAndImportantData/output_pairData_p123_general/"
output_folder_path ="../stationVisualize/output_pairData_p123_general/"
#file_name = "../QueryAndImportantData/output_pairData_p1234_general/output_0315_533910_542590.csv"
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
    print 'create pairFileDirectory'
for dirname, dirnames, filenames in os.walk(folder_path):
    print filenames
    for filename in filenames:
        count = 0
        arr = []
        startDate = []
        cc = []
        if filename == '.DS_Store':
            continue
        readFileName = os.path.join(folder_path, filename)
        print(readFileName)
        with open(readFileName, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                count += 1
                ct = int(row['Count'])
                if ct<=3:
                    cc.append('green')
                elif ct<7:
                    cc.append('yellow')
                else:
                    cc.append('red')
                arr.append(ct)
                #startDate.append(row['StartDate'])
        ind = np.arange(count)
        print ind
        print arr
        fig, ax = plt.subplots()
        outputImg = os.path.join(output_folder_path, filename+".png")
        width=1.5
        axes = plt.gca()
        axes.set_ylim([0,10])
        ax.bar(ind, arr, width, color=cc)
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
        ax.set_xticklabels(('01-01', '02-20', '04-11', '05-31', '07-20', '09-08', '10-28'))
        fig.savefig(outputImg)
        #print ', '.join(row)
#fig, ax = plt.subplots()
#width=1.5
#ax.bar(ind,arr,width,color=cc)
#ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
#ax.set_xticklabels(('01-01', '02-20', '04-11', '05-31', '07-20', '09-08', '10-28'))
#ax.set_xticks((ind+0.2))
#ax.set_xticklabels((startDate))
#print(ind)
#print(arr)
#plt.show()
