#!/usr/bin/python

import csv
import operator
from string import punctuation
from nltk.corpus import stopwords


#####################################################
#                                                   #
#   Takes the input and output from 2 csv files.    #
#   It will compute the conditional probability     #
#   of words in a class, given that they appear     #
#   frequently enough.                              #
#   For each class we will write a csv file         #
#   with the words and their associated             #
#   probability.                                    #
#                                                   #
#####################################################



def main():
    abstracts = get_csv_content('train_in2.csv','abstract')  
    classes = get_csv_content('train_out.csv','category')   
    class_probs = class_probs_get(classes)
    print("Class prob done")
    word_probs = word_probs_get(classes,abstracts,0.5,500)
    print("Word prob done")
    for classe in list(word_probs.keys()): 
        write_csv(classe,word_probs[classe])
	

# Gets the probability of each category
def class_probs_get(classes):
    class_count = class_counter(classes)
    total = sum(list(class_count.values()))
    class_prob = dict()
    for classe in list(class_count.keys()):
        class_prob[classe] = class_count[classe]/total
    return class_prob


# Counts the occurence of each class from a list of strings (the strings are the name of the classes)
def class_counter(dict_classes):
    class_count = dict()
    for classe in dict_classes:
        if classe in class_count:
            class_count[classe] =  class_count[classe] + 1
        elif classe != 'category':
            class_count[classe] = 1
    return class_count


# Sanatize the strings from a list of strings
# NOT USED ANYMORE
def sanatizer(abstracts):
    eng_stopwords = stopwords.words("english")
    for i in range(len(abstracts)):
        print("Sanatizing abstract {}".format(i))
        abstracts[i] = ''.join(c for c in abstracts[i] if c not in punctuation)
        abstracts[i] = abstracts[i].lower()
        abstracts[i] = ([word for word in abstracts[i].split() if word not in eng_stopwords])
    return abstracts


# Gets the probability P(w|c) for each word
def word_probs_get(classes,abstracts, alpha, size): 
    word_count = dict()
    for i in range(len(abstracts)):
        abstract = abstracts[i].split()
        classe = classes[i]
        if classe == 'category':
            continue
        if not (classe in word_count):
            word_count[classe] = dict()
        for j in range(len(abstract)):
            if abstract[j] in word_count[classe]:
                (word_count[classe])[abstract[j]] = (word_count[classe])[abstract[j]] + 1
            else:
                (word_count[classe])[abstract[j]] = 1
    #Counting each occurences of each class
    class_count = class_counter(classes)
    #Selecting the 2000 most represented words for each class.
    word_prob = dict()
    for classe in word_count:
        word_prob[classe] = select_best(word_count[classe],size)
    for classe in list(word_prob.keys()):
        for word in word_prob[classe]:
            (word_prob[classe])[word] = (float)((float)((word_prob[classe][word]) + alpha)/(float)(class_count[classe] + alpha* (float) (len(list((word_prob[classe]).keys())))))
    return word_prob 
   
# Returns a dict that contains the n entries with highest value                             
def select_best(dic,n):
    counter = 0
    new_dict = dict()
    sorted_list = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
    for key, value in sorted_list:
        counter = counter + 1
        if counter == n:
            break
        new_dict[key] = value
    return new_dict


# Gets the entry of one column into a list
def get_csv_content(title,category):
    input_file = list(csv.DictReader(open(title)))
    entry = list()
    for i in range(len(input_file)):
        entry.append(input_file[i][category])
    return entry            
 
# Writes a dictionnary to a csv file
def write_csv(classe,word_dict):
    name = classe+".csv"
    words = list(word_dict.keys())
    writer = csv.DictWriter(open(name,'w'), fieldnames=words)
    writer.writeheader()
    writer.writerow(word_dict)

# You know what this is for 
if __name__ == "__main__": 
    main()
