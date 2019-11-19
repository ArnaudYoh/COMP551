csv_cleaner.py : 
This Script is meant to read a csv file with different "groups" of data separated by an empty row.  It selects the features we want to save for each datapoint, it merges data points that describe data from the same say. The result is written in another csv file with a supplementary column identifying the group to which the point belongs to.  

Decision Trees.py / LogReg.py / SVMs.py : 
Implementation of the methods, using the sklearn library. 

Input_getter.py: 
This script will read from the csv file created by csv_cleaner.py, aggregate k datapoints from a "group" of data into a row. It does this for each "group" and then return a numpy matrix. 