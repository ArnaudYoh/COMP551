#!bin/usr/python
import csv
import numpy as np
import _pickle as cPickle

import Input_getter as ig

from sklearn import tree
from sklearn.model_selection import cross_val_score

def main(): 
	matrices = ig.main(10)
	X = matrices[0]
	Y = matrices[1]
	X = np.matrix(X)
	Y = np.array(Y)

	cla = tree.DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_split=1e-07, class_weight=None, presort=False)
	scores = cross_val_score(cla, X, Y, cv=int(Y.size/2))
	print('Test for Gini')
	#print("Accuracy: %0.10f (+/- %0.2f) \n" % (scores.mean(), scores.std() * 2))
	#print("Precision: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='precision').mean()))
	#print("F1-Score: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='f1').mean()))
	#print("Recall: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='recall').mean()))
	cla.fit(X,Y)
	print(cla.feature_importances_)
	save_cla(cla,'dtgini.pk1')

	cla = tree.DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_split=1e-07, class_weight=None, presort=False)
	scores = cross_val_score(cla, X, Y, cv=int(Y.size/2))
	print('Test for entropy')
	#print("Accuracy: %0.10f (+/- %0.2f) \n" % (scores.mean(), scores.std() * 2))
	#print("Precision: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='precision').mean()))
	#print("F1-Score: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='f1').mean()))
	#print("Recall: %0.5f  \n" % (cross_val_score(cla, X, Y, cv=int(Y.size/2), scoring='recall').mean()))
	cla.fit(X,Y)
	print(cla.feature_importances_)
	save_cla(cla,'dtig.pk1')
	print("\n\n")
	#cla = load_cla('cla.pk1')



def save_cla(cla, filename):
	with open(filename,'wb') as fid:
		cPickle.dump(cla,fid)


def load_cla(filename):     
	with open(filename,'rb') as fid:
		cla = cPickle.load(fid)
	return cla


if __name__ == "__main__":
	main()
