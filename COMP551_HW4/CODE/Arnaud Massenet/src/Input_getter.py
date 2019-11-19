import csv 
import numpy as np
import time

def main(data_size): # number of data points clustered into a single one. 
	neg_lab = list(csv.DictReader(open("clean_North_negative_labels.csv", "r")))
	neg = list(csv.DictReader(open("clean_North_negative.csv", "r")))
	pos_lab = list(csv.DictReader(open("clean_North_positive_labels.csv", "r")))
	pos = list(csv.DictReader(open("clean_North_positive.csv", "r")))
	
	#features = ['timestamp','location-long','location-lat','ground-speed','height-above-msl','ECMWF Interim Full Daily SFC Temperature (2 m above Ground)', 'MODIS Land Terra Vegetation Indices 500m 16d NDVI', 'MODIS Land Aqua Vegetation Indices 500m 16d NDVI']
	features = ['timestamp','ECMWF Interim Full Daily SFC Temperature (2 m above Ground)', 'MODIS Land Terra Vegetation Indices 500m 16d NDVI', 'MODIS Land Aqua Vegetation Indices 500m 16d NDVI']

	labs = [neg_lab, pos_lab]
	raw_data = [neg, pos]

	matrix = list()
	y = list()
	for i in range(2):
		j = 0
		for data in labs[i]:
			if data["label"]=="1":
				matrix_row = list()
				for k in range(data_size): 
					data_line = raw_data[i][j-k]
					for feat in features: 
							matrix_row.append(float(data_line[feat]))					
				matrix.append(matrix_row)
				y.append(i)
			j = j + 1
	return(matrix,y)



if __name__ == "__main__": 
	main(2)