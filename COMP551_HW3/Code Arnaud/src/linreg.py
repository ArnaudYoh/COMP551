#!/usr/bin/python 

import numpy as np
import pandas
import csv
import _pickle as cPickle
from sklearn import linear_model


#CODE TRANSFERED TO "LogReg_Clustering"
'''
def main():
    X = np.fromfile('train_x.bin' ,dtype='uint8' )
    X = X.reshape((100000,3600))
    X = clean_data(X)
    ylist = get_csv_int('train_y.csv',list('P'))
    y = np.array(ylist, ndmin=1)

    cla = linear_model.LogisticRegression(penalty='l2', dual=False, tol = 0.0001, C=2.0,fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='lbfgs', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
    cla.fit(X[:20000],y.ravel()[:20000])
    save_cla(cla,'logreglbfgs2.pk1')

    cla = linear_model.LogisticRegression(penalty='l2', dual=False, tol = 0.0001, C=2.0,fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='newton-cg', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
    cla.fit(X[:20000],y.ravel()[:20000])
    save_cla(cla,'logregnewton2.pk1')
    
    #cla = load_cla('cla.pk1')
    
    cla = linear_model.LogisticRegression(penalty='l2', dual=False, tol = 0.0001, C=2.0,fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
    cla.fit(X[:20000],y.ravel()[:20000])
    save_cla(cla,'logregliblin2.pk1')

    cla = linear_model.LogisticRegression(penalty='l2', dual=False, tol = 0.0001, C=2.0,fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='sag', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
    cla.fit(X[:20000],y.ravel()[:20000])
    save_cla(cla,'logregsag2.pk1')
    
    
    results = list(cla.predict(X))
    err_num = 0
    for i in range(len(ylist)):
        if ylist[i][0] != results[i]:
          #  print(int(ylist[i][0]), results[i])
            err_num +=1
    print(err_num)
'''    
   

def clean_data(Arr):
    for img in Arr:
        for pix in img:
            if int(pix) < 240:
                pix = 0
            else:
                pix = int(pix)
    return Arr

def save_cla(cla, filename):
    with open(filename,'wb') as fid:
        cPickle.dump(cla,fid)


def load_cla(filename):     
    with open(filename,'rb') as fid:
        cla = cPickle.load(fid)
    return cla

def get_csv_int(title,categories):
    input_file = list(csv.DictReader(open(title)))
    entry = list()
    for i in range(len(input_file)):
        to_add = list()
        for category in categories:
            if input_file[i][category] is None:
                to_add.append(0)    
            else:
                to_add.append(input_file[i][category])
#            print(input_file[i][category])
        entry.append(int(to_add[0]))
    return entry 





if __name__ == "__main__":
	main()
