import matplotlib.pyplot as plt
import numpy as np
import csv
file_name = "../QueryAndImportantData/output_pairData_p1234_general/output_0315_533910_542590.csv"
count = 0
arr = []
startDate = []
cc = []
with open(file_name, 'rb') as csvfile:
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
        startDate.append(row['StartDate'])

        #print ', '.join(row)
ind = np.arange(count)
fig, ax = plt.subplots()
width=1.5
ax.bar(ind,arr,width,color=cc)
ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
ax.set_xticklabels(('01-01', '02-20', '04-11', '05-31', '07-20', '09-08', '10-28'))
#ax.set_xticks((ind+0.2))
#ax.set_xticklabels((startDate))
print(ind)
print(arr)
plt.show()
