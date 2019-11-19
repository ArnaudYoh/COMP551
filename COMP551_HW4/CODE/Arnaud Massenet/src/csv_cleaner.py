import csv
import sys
import time
from math import isnan

def main(): 
	field_names = ['group','id','original-row-nb','timestamp','location-long','location-lat','ground-speed','height-above-msl','ECMWF Interim Full Daily SFC Temperature (2 m above Ground)', 'MODIS Land Terra Vegetation Indices 500m 16d NDVI', 'MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] 
	clean_csv('barent_NP.csv','clean_North_positive.csv', field_names)

#def read_date(): 


def clean_csv(org,dest,field_names): 
	input_file = list(csv.DictReader(open(org)))
	output_file = csv.DictWriter(open(dest, 'w',  newline="\n", encoding="utf-8"), fieldnames=field_names)
	output_file.writeheader()
	j = 0
	i = 1
	group = 0
	change_group = False 
	while i < len(input_file) : 
		print("sanatizing row "+ str(i) ) 
		#print(input_file[i])
		curr = input_file[i]
		if not curr['timestamp']:
			i = i+1
			group = group + 1
			continue
		date = curr['timestamp'].split()[0]
		new_row = dict()
		new_row["location-long"] = float(curr["location-long"])
		new_row['location-lat'] = float(curr['location-lat']) 
		new_row['ground-speed'] = float(curr['ground-speed'] )          
		new_row['height-above-msl'] = float(curr['height-above-msl'] )
		new_row['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)'] = float(curr['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)']) 
		new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI'] = float(curr['MODIS Land Terra Vegetation Indices 500m 16d NDVI']) 
		new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] = float(curr['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] )
		if isnan(new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI']):
			new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI'] = 0.35
		if isnan(new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI']):
			new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] = 0.35
		simi_count = 1
		try:
			next_date = input_file[i+1]['timestamp'].split()[0]
		except :
			next_date = "coucou"
			change_group = True
			i = i + 1
		print(date)
		while next_date == date: 
			print("true")
			simi_count = simi_count + 1
			new_row['location-long'] = new_row['location-long'] + float(input_file[i+1]['location-long'])
			new_row['location-lat'] = new_row['location-lat'] + float(input_file[i+1]['location-lat'])
			new_row['ground-speed'] = new_row['ground-speed'] + float(input_file[i+1]['ground-speed'])
			new_row['height-above-msl'] = new_row['height-above-msl'] + float(input_file[i+1]['height-above-msl'])
			new_row['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)'] = new_row['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)'] + float(input_file[i+1]['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)'])
			if isnan(float(input_file[i+1]['MODIS Land Terra Vegetation Indices 500m 16d NDVI'])):
				to_add =0.35
			else: 
				to_add = float(input_file[i+1]['MODIS Land Terra Vegetation Indices 500m 16d NDVI'])
			new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI'] = new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI'] + to_add
			if isnan(float(input_file[i+1]['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'])):
				to_add =0.35
			else: 
				to_add = float(input_file[i+1]['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'])
			new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] = new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] + to_add
			i = i + 1
			try:
				next_date = (input_file[i+1]['timestamp'].split()[0])
			except :
				next_date = "coucou"
				change_group = True
				i = i + 1   
		new_row['group'] = str(group)
		new_row['id'] = str(j)
		new_row['original-row-nb'] = str(i)
		(year, month, day) = date.split('-')
		year = int(year)
		month = int(month)
		day = int(day)
		date = time.gmtime(time.mktime((year, month, day, 0,0,0,0,0,0)))[7]

		new_row['timestamp'] = str(date)    
		new_row['location-long'] = str(new_row['location-long']/simi_count)
		new_row['location-lat'] = str(new_row['location-lat']/simi_count)
		new_row['ground-speed'] = str(new_row['ground-speed']/simi_count)           
		new_row['height-above-msl'] = str(new_row['height-above-msl']/simi_count)
		new_row['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)'] = str(new_row['ECMWF Interim Full Daily SFC Temperature (2 m above Ground)']/simi_count)
		new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI'] = str(new_row['MODIS Land Terra Vegetation Indices 500m 16d NDVI']/simi_count)
		new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI'] = str(new_row['MODIS Land Aqua Vegetation Indices 500m 16d NDVI']/simi_count) 
		output_file.writerow(new_row)
		if change_group:
			change_group = False
			group = group + 1
		j = j + 1
		i = i + 1

if __name__ == "__main__": 
	main()
