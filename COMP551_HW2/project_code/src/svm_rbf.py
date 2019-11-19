import csv
import operator
from string import punctuation
import math
import numpy as np
import sklearn
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
#from sklearn.model_selection import train_test_split

TARGETS = ['math', 'cs', 'physics', 'stat']

parameters = {
	#'vect__max_features' : ['None', 100, 1000, 10000],
	'clf__C' : [0.1, 0.9, 1.0, 1.1, 10], 
	'clf__kernel':['rbf', 'sigmoid'],
	#'clf__degree' : [2,3], 
	'clf__gamma':[ 0.001, 0.1, 1, 10, 100]
	}

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC()),
])



if __name__ == "__main__": 

	#Get data
	abstracts = scripter.get_csv_content('train_in2.csv','abstract')  
	classes = scripter.get_csv_content('train_out.csv','category')
	testing = scripter.get_csv_content('test_in2.csv', 'abstract')

	#Temporary to reduce training set
	x_train, x_valid, y_train, y_valid = train_test_split(abstracts, classes, test_size = 0.99, random_state =0)


	grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=0)

	print("Performing grid search...")
	print("pipeline:", [name for name, _ in pipeline.steps])
	print("parameters:")
	pprint(parameters)
	t0 = time()
	grid_search.fit(x_train, y_train)
	print("done in %0.3fs" % (time() - t0))
	print()

	print("Scores")
	#print(grid_search.cv_results_)

	#use pandas for data visualization
	s = pd.DataFrame(grid_search.cv_results_)
	display(s)
	#write latex 
	latex = s.to_latex(columns = [2,3,4,5,6,8])
	latex2 = s.to_latex(columns = [-4,-3,-2,-1])
	with open('latex.csv','wb') as csvfile:
		wr = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
		wr.writerow([latex, latex2])

	with open('csv.csv','wb') as csvfile2:
		s.to_csv(csvfile2)
	print("Best score: %0.3f" % grid_search.best_score_)
	print("Best parameters set:")
	best_parameters = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
		print("\t%s: %r" % (param_name, best_parameters[param_name]))