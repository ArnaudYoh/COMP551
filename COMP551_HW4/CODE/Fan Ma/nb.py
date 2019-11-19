import csv
import numpy as np
#import pickle as cPickle

import Input_getter as ig
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import linear_model


def main():
    matrices = ig.main(5)
    X = matrices[0]
    Y = matrices[1]
    X = np.matrix(X)
    X_valid = X[21:26,:]
    X = X[0:20,:]
	
    Y = np.array(Y)
    print Y.shape
    Y_valid = Y[21:26]
    Y = Y[0:20]
    gnb = BernoulliNB()
    cla = gnb.fit(X,Y)
    #cla.fit(X,Y)
    score = cla.score(X_valid,Y_valid)
    predictions = cla.predict(X)
    print predictions
    print Y_valid
    print Y
    print score
    #print X.shape

if __name__ == "__main__":
	main()