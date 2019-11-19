import csv
from sklearn.cluster import KMeans
import numpy as np


csvfile = "clean_North_negative.csv"

heading = []
i=0
prev=-1
curr=-1
with open(csvfile, 'rt') as csvfile, open("clean_North_negative_labels.csv", "wb") as outfile:
     reader = csv.reader(csvfile, delimiter=',', quotechar='|')
     writer = csv.writer(outfile)
     headers = next(reader, None)
     print headers
     #writer.writerow(headers)
     #writer.writerow([0])
     #writer.writerow([0])
     writer.writerow(["id","label"])
     first_row = next(reader, None)
     second_row = next(reader, None)
     prev=second_row[0]
     label_list = []
     for row in reader:
         label = 0
         if row[0] != prev:
             label = 1
         label_list.append([i,label])
         #writer.writerow([i,label])
         heading.append(float(row[7]))
         prev = row[0]
         i=i+1
     label_list.append([i,1])
     i=i+1
     label_list.append([i,0])
     for el in label_list:
         writer.writerow(el)

heading = np.asarray(heading)
print heading.shape

heading = heading.reshape(-1,1)
print heading.shape

kmeans = KMeans(n_clusters=2, random_state=0).fit(heading)
print kmeans.labels_
