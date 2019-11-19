# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:08:41 2016

@author: pcluc
"""
import numpy as np
x = np.fromfile('train_x.bin', dtype='uint8')
x = x.reshape((100000,3600))

f = open('train_x.csv', 'w')
import csv
w = csv.writer(f)
for i in range (0,x.shape[0]):
    w.writerow(x[i])
f.close()