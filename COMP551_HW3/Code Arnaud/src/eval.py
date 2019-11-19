#!/usr/bin


import linreg
import numpy as np

from sklearn.metrics import classification_report, accuracy_score,precision_score, f1_score, recall_score


def main(): 
    title = input()
    X = np.fromfile('train_x.bin', dtype='uint8')
    X = X.reshape(100000,3600)
    X = linreg.clean_data(X)
    ylist = linreg.get_csv_int('train_y.csv', list('P'))
    y = np.array(ylist, ndmin=1)

    cla = linreg.load_cla(title)

    results = cla.predict(X)

    print("Precision: ", precision_score(y,results))
    print("Accuracy: ", accuracy_score(y,results))
    print("F1: ", f1_score(y,results))
    print("Recall: ", recall_score(y, results))

if __name__ == "__main__":
    main()
