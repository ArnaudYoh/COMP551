#!bin/usr/python
import csv
import numpy as np
import _pickle as cPickle

import Input_getter as ig

from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, accuracy_score,precision_score, f1_score, recall_score

def main(): 
	matrices = ig.main(7)
	X = matrices[0]
	Y = matrices[1]
	X = np.matrix(X)
	Y = np.array(Y)
	print(Y)
	print(Y.size)	
	print(X.shape)
	to_test = [0.0001,0.001,0.01,0.1,1.0,10,100,1000,10000]
	#to_test = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
	#cla = load_cla('cla.pk1')
	i = 0
	#for C_value in to_test:
	cla = linear_model.LogisticRegression(penalty='l2', dual=False, tol = 0.0001, C=10 ,fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=1000, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
	scores = cross_val_score(cla, X, Y, cv=int(Y.size/2))
	#print('Test for C = ' + str(C_value))
	print("Accuracy: %0.5f (+/- %0.2f) \n" % (scores.mean(), scores.std() * 2))
	print("Precision: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='precision').mean()))
	print("F1-Score: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='f1').mean()))
	print("Recall: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='recall').mean()))
	
	filename = 'logregliblin' + str(i) +'.pk1'
	save_cla(cla, filename)
	i = i+1

	cla.fit(X,Y)
	print(cla.coef_)


def save_cla(cla, filename):
	with open(filename,'wb') as fid:
		cPickle.dump(cla,fid)


def load_cla(filename):     
	with open(filename,'rb') as fid:
		cla = cPickle.load(fid)
	return cla


if __name__ == "__main__":
	main()
