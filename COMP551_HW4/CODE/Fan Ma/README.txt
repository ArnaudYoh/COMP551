cleaner.py : 
Script takes movebank data and extracts data and labels for us

gradient.py:
Creates a .csv identical to the previous, except replacing long and lat by their gradients (instatneous velocity)

nb.py:
naive bayes

Input_getter.py: 
This script will read from the csv file created by csv_cleaner.py, aggregate k datapoints from a "group" of data into a row. It does this for each "group" and then return a numpy matrix. 