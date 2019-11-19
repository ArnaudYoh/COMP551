import csv
from sklearn.cluster import KMeans
import numpy as np


with open("barentsraw.csv", 'rt') as csvfile, open("barentsTestNorth.csv", "wb") as outfile,  open("barentsTestSouth.csv", "wb") as outfileSouth, open("barentsNegNorth.csv", "wb") as neg_north_file, open("barentsNegSouth.csv", "wb") as neg_south_file:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    writer_north = csv.writer(outfile)
    writer_south = csv.writer(outfileSouth)
    writer_neg_north = csv.writer(neg_north_file)
    writer_neg_south = csv.writer(neg_south_file)
    neg_north_num = 6
    neg_south_num = 6
    headers = next(reader, None)
    print headers
    first_row = next(reader,None)
    write_buffer = []
    i=0
    north_id=0
    south_id=0
    north_neg_id=0
    south_neg_id=0
    example_id_north = 0
    example_id_south = 0
    example_id_north_neg = 0
    example_id_south_neg = 0
    nb = 1

    writer_north.writerow(["group","id","original-row-nb","location-long","location-lat","ground-speed","height-above-msl","ECMWF Interim Full Daily SFC Temperature (2 m above Ground)","MODIS Land Terra Vegetation Indices 500m 16d NDVI","MODIS Land Aqua Vegetation Indices 500m 16d NDVI"])
    writer_south.writerow(["group","id","original-row-nb","location-long","location-lat","ground-speed","height-above-msl","ECMWF Interim Full Daily SFC Temperature (2 m above Ground)","MODIS Land Terra Vegetation Indices 500m 16d NDVI","MODIS Land Aqua Vegetation Indices 500m 16d NDVI"])
    writer_neg_north.writerow(["group","id","original-row-nb","location-long","location-lat","ground-speed","height-above-msl","ECMWF Interim Full Daily SFC Temperature (2 m above Ground)","MODIS Land Terra Vegetation Indices 500m 16d NDVI","MODIS Land Aqua Vegetation Indices 500m 16d NDVI"])
    writer_neg_south.writerow(["group","id","original-row-nb","location-long","location-lat","ground-speed","height-above-msl","ECMWF Interim Full Daily SFC Temperature (2 m above Ground)","MODIS Land Terra Vegetation Indices 500m 16d NDVI","MODIS Land Aqua Vegetation Indices 500m 16d NDVI"])

    all_rows = []

    for row in reader:
        row[3] = row[3]
        row[4] = row[4]
        all_rows.append(row)
    
    for idx,row in enumerate(all_rows):
        toWrite = []
        if row[9] != all_rows[idx-1][9]:
            write_buffer = []
            i=i+1
            #example_id = example_id + 1
        toWrite.append(i)
        toWrite.append(float(row[3]))

        toWrite.append(float(row[4]))
        if (len(write_buffer) > 30):
            write_buffer.pop()
        try:
            write_buffer.append([idx+2, row[2],float(row[3]),float(row[4]),"NaN","NaN",float(row[14]),float(row[15]),float(row[16])])
        except ValueError:
            p=0
        try:
            
            if (abs((float(all_rows[idx][3])-float(all_rows[idx+1][3]))) > 1 or abs((float(all_rows[idx][4])-float(all_rows[idx+1][4]))) > 1):
                if (abs(float(all_rows[idx+1][3])-float(all_rows[idx+2][3])) > 1 or abs(float(all_rows[idx+1][4])-float(all_rows[idx+2][4])) > 1):
                    if (abs(float(all_rows[idx+2][3])-float(all_rows[idx+3][3])) > 1 or abs(float(all_rows[idx+2][4])-float(all_rows[idx+3][4])) > 1):
                        if(abs((float(all_rows[idx][3])-float(all_rows[idx-1][3])) < 1) and abs((float(all_rows[idx][4])-float(all_rows[idx-1][4]))) < 1):
                            if (float(all_rows[idx+2][3])-float(all_rows[idx+1][3]) > 0):
                                for el in write_buffer:
                                    el.insert(0,north_id)
                                    el.insert(0,example_id_north)
                                    writer_north.writerow(el)
                                    north_id=north_id + 1
                                example_id_north=example_id_north+1
                            if (float(all_rows[idx+2][3])-float(all_rows[idx+1][3]) < 0):
                                for el in write_buffer:
                                    el.insert(0,south_id)
                                    el.insert(0,example_id_south)
                                    writer_south.writerow(el)
                                    south_id=south_id+1
                                example_id_south=example_id_south+1
                            write_buffer = []
            if (south_id > 0 and len(write_buffer) > 29):
                for el in write_buffer:
                    el.insert(0,south_neg_id)
                    el.insert(0,example_id_south)
                    writer_neg_south.writerow(el)
                    south_id=south_id+1
                    neg_south_num = neg_south_num - 1
                    
                write_buffer = []
                example_id_south=example_id_south+1
                
            elif (north_id > 0 and len(write_buffer) > 29):
                for el in write_buffer:
                    el.insert(0,north_neg_id)
                    el.insert(0,example_id_north)
                    writer_neg_north.writerow(el)
                    north_id=north_id+1
                    neg_north_num = neg_north_num - 1
                write_buffer = []
                example_id_north=example_id_north+1
                            
                
        except:
            p=0
            #print "error"
            #for el in write_buffer:
                #writer.writerow(el)