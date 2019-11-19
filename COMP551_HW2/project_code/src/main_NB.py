#!/usr/bin/python

import csv
import operator
from random import shuffle
import scripter
import predictor
import numpy as np 


#####################################################
#                                                   #
#   Computes the 10-fold cross-validation results   #
#   using different tweeking parameters, such as    #
#   the alpha and the feature number limit.         #
#   Outputs the results for each combination.       #
#                                                   #
#####################################################


def main(): 
    abstracts = scripter.get_csv_content('train_in2.csv','abstract')  
    classes = scripter.get_csv_content('train_out.csv','category')
    sizes = [100,200,500,1000,2000]
    alphas = [0.01,0.1,0.3,0.5,0.7,1]
    sizes = [500]
    alphas = [1]
    results = list()
    for i in range(len(sizes)):
    	results.append(list())
    	for j in range(len(alphas)): 
    		results[i].append(k_fold(abstracts,classes,10,alphas[j],sizes[i] ))
    		print("We have {} for i: {} and j: {}".format(results[i][j], i, j))
    print(results)

def k_fold(abstracts, classes, k, alpha, size):
    chunksize = len(classes)/k
    error_count = 0
    for v in np.arange(0, len(classes), chunksize):
        left_bound = v 
        right_bound = v + chunksize
        #print("Getting the correct subsets")
        valid_input = abstracts[left_bound : right_bound]
        valid_output = classes[left_bound : right_bound]
        train_in = abstracts[0 : left_bound] + abstracts[right_bound : len(abstracts)-1]
        train_out = classes[0 : left_bound] + classes[right_bound : len(abstracts)-1]
#        train_in = [abstracts[i] for i in range(len(abstracts)) if i not in range(left_bound, right_bound)] 
#        train_out = [classes[i] for i in range(len(classes)) if i not in range(left_bound, right_bound)] 
        #print("Done with subsets")
        word_probs = scripter.word_probs_get(train_out,train_in, alpha , size) 
        for classe in list(word_probs.keys()): 
            scripter.write_csv(classe,word_probs[classe])
        error_count += (float)(predictor.main(valid_input, train_out, valid_output,alpha)/(float)(len(valid_output)))
    #print((float)((float)(error_count)/(float)(k)))
    return (float)((float)(error_count)/(float)(k))



if __name__ == "__main__": 
  main()
