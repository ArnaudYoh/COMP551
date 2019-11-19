import csv
import operator
from string import punctuation
import math
import numpy as np
import sklearn
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import scripter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time
import logging
import pandas as pd
from IPython.display import display
from sklearn.model_selection import KFold
import sys

def main(argv):

	k = str(sys.argv[0])
	#Load training data 
	abstracts = scripter.get_csv_content('train_in2.csv','abstract')  
	classes = scripter.get_csv_content('train_out.csv','category')
	testing = scripter.get_csv_content('test_in2.csv', 'abstract')

	#Perform vectorization of input and test data
	vectorizer = TfidfVectorizer(min_df =1)
	x = vectorizer.fit_transform(abstracts)
	x_test = vectorizer.transform(testing)

	print ('input vectorized')

	#train
	if k == 'rbf':
		clf = SVC( C=10, gamma = 1  ).fit(x, classes)
	else:
		clf = LinearSVC(C=0.6).fit(x,classes)

	print('trained')

	pred = clf.predict(x_test)

	print('predicted')


	#write prediction to csv 
	with open('output.csv', 'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
		wr.writerow(["id", "category"])
		j = 0
		for i in range(0, len(pred)):
			wr.writerow([i, pred[i]])

if __name__ == "__main__": 
	main(sys.argv[1:])