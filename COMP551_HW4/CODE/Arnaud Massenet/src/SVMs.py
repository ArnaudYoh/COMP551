#!bin/usr/python
import csv
import numpy as np
import _pickle as cPickle

import Input_getter as ig

from sklearn import svm
from sklearn.model_selection import cross_val_score

def main(): 
	matrices = ig.main(4)
	X = matrices[0]
	Y = matrices[1]
	X = np.matrix(X)
	Y = np.array(Y)
	#to_test = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
	to_test = [0.1,1.0,10,100,1000]
	to_test2 = [0.001,0.1,1,10,100]


	i = 0
	#for C_value in to_test:
	#	for ga_value in to_test2: 	
	cla = svm.SVC(C=1, kernel='rbf', degree=3, gamma=0.001, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None)		
	scores = cross_val_score(cla, X, Y, cv=int(Y.size/2))
	#print('Test for C = ' + str(C_value) + ' and Gamma = ' +  str(ga_value))
	print("Accuracy: %0.10f (+/- %0.2f) \n" % (scores.mean(), scores.std() * 2))
	print("Precision: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='precision').mean()))
	print("F1-Score: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='f1').mean()))
	print("Recall: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='recall').mean()))


	filename = 'nusvmrbf' + str(i) +'.pk1'
	save_cla(cla, filename)
	i = i+1

	#cla = load_cla('cla.pk1')
	
#	cla = svm.NuSVC(nu=0.5, kernel='poly', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None)
#	cla.fit(X,Y)
#	save_cla(cla,'nusvmpoly.pk1')

#	cla = svm.NuSVC(nu=0.5, kernel='sigmoid', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None)
#	cla.fit(X,Y)
#	save_cla(cla,'nusvmsigm.pk1')



def save_cla(cla, filename):
	with open(filename,'wb') as fid:
		cPickle.dump(cla,fid)


def load_cla(filename):     
	with open(filename,'rb') as fid:
		cla = cPickle.load(fid)
	return cla


if __name__ == "__main__":
	main()
