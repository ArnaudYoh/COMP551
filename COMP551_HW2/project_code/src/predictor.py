#!/usr/bin/python

import csv
import operator
from string import punctuation
from nltk.corpus import stopwords



#########################################################
#                                                       #
#   Reads the probabilties associated with the classes  #
#   from the csv files written with "scripter.py".      #
#   Computes the probability, makes the predictions     #
#   and write them in a csv file, using the format      #
#   required by Kaggle                                  #
#                                                       #
#########################################################



global eng_stopwords 
eng_stopwords = stopwords.words("english")

def main(input_strings, train_output, valid_output, alpha): 
    classes = ['cs','stat','math','physics']
    word_probs = dict()
    class_count = class_counter(train_output)
    results = list()
    for classe in classes: 
        word_probs[classe] = get_probs(classe)
    for i in range(len(input_strings)): 
    	#print("Predicting abstract {}".format(i))
        result = predict(word_probs,input_strings[i], class_count, alpha)
        results.append(result)
    #write_prediction('output.csv',results)
    print(error_counter(results, valid_output))
    return error_counter(results, valid_output)


def predict(word_probs,string,class_count, alpha): 
    prob = dict()
    abstract = string.split() 
    for i in range(len(abstract)):
        for classe in list(word_probs.keys()): 
        	if not classe in prob:
        		prob[classe] = 1
        	if abstract[i] in word_probs[classe]:
        		prob[classe] = (float)(prob[classe])*(float)((word_probs[classe])[abstract[i]])
        	else:
        		prob[classe] = (float)(prob[classe])*(float)(alpha/(class_count[classe]+ alpha*(float)(len(list(word_probs[classe].keys())))))
    return max(prob, key=prob.get)


# Gets the entry of one column into a list
def get_csv_content(title,category):
    input_file = list(csv.DictReader(open(title)))
    entry = list()
    for i in range(len(input_file)):
        entry.append(input_file[i][category])
    return entry  


def error_counter(result, answer):
	error_count = 0
	for i in range(len(result)): 
		if result[i] != answer[i]:
			error_count += 1
	return error_count

# sanatize one string
# NOT USED 
def sanatizer(abstract):
    abstract = ''.join(c for c in abstract if c not in punctuation)
    abstract = abstract.lower()
    abstract = ' '.join([word for word in abstract.split() if word not in eng_stopwords])
    return abstract


def get_probs(classe):
	title = classe+".csv"
	myfile = csv.DictReader(open(title))
	for row in myfile:
		result = row
	return result

# Counts the occurence of each class from a list of strings (the strings are the name of the classes)
def class_counter(dict_classes):
    class_count = dict()
    for classe in dict_classes:
        if classe in class_count:
            class_count[classe] =  class_count[classe] + 1
        elif classe != 'category':
            class_count[classe] = 1
    return class_count

# Write into csv files named 'title' the results in the category column
def write_prediction(title,results): 
    field_names = ['id','category']
    writer = csv.DictWriter(open(title,'w'), fieldnames=field_names)
    writer.writeheader()
    for i in range(len(results)):
    	dic = dict()
    	dic['id'] = i
    	dic['category'] = results[i]
    	writer.writerow(dic)


if __name__ == "__main__":
    input_strings = get_csv_content('train_in2.csv','abstract')
    output = get_csv_content('train_out.csv','category')
    main(input_strings, output, output, 0.5)