import csv
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


in_file= "barentssea.csv"
out_file= "barentssea_gradient.csv"
colormap = np.array(['red', 'lime', 'black'])
long_idx=4
lat_idx=5

with open(in_file, 'rt') as csvfile, open(out_file, "wb") as outfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    writer = csv.writer(outfile)
    neg_south_num = 6
    headers = next(reader, None)
    print headers
    #first_row = next(reader,None)
    plotx = []
    ploty = []
    U=[]
    V=[]


    writer.writerow(["group","id","original-row-nb","timestamp","location-long","location-lat","ground-speed","height-above-msl","ECMWF Interim Full Daily SFC Temperature (2 m above Ground)","MODIS Land Terra Vegetation Indices 500m 16d NDVI","MODIS Land Aqua Vegetation Indices 500m 16d NDVI"])
    prev_lat = 0
    prev_long = 0
    for row in reader:
        #print row
        
        new_row = list(row)
        #print "---------------------------------------------------"
        #print new_row
        new_row[3] = float(row[3]) - prev_long
        new_row[4] = float(row[4]) - prev_lat
        prev_long=float(row[3])
        prev_lat=float(row[4])
        #print "========================================"
        #print new_row
        writer.writerow(new_row)
        plotx.append(float(row[3]))
        ploty.append(float(row[4]))
        
        
        U.append(new_row[3])
        V.append(new_row[4])
    #plt.figure(figsize=(14,7))
    #plt.subplot(1, 2, 2)
    #plt.scatter(plotx, ploty, s=40)
    ax = plt.gca()
    plt.figure()
    ax.quiver(plotx,ploty,U,V,angles='xy',scale_units='xy',scale=2)
    #ax.set_xlim([-1,10])
    #ax.set_ylim([-1,10])
    plt.title('Velocity gradient')
    plt.show()
