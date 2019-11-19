#!/usr/bin/python





#####################################################
#                                                   #
#   Takes the strings from the column of a csv file #
#   and remove all possible stopwords, punctuation  #
#   and stems the results. The output is then       #
#   written in another csv file                     #                                         
#                                                   #
#####################################################


import csv
import operator
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk

global eng_stopwords 
eng_stopwords = stopwords.words("english")

global porter
porter = nltk.PorterStemmer()


def main():
	sanatize_csv_content('test_in.csv','abstract','test_in2.csv','abstract')
    
# sanatize one string
def sanatizer(abstract):
    abstract = abstract.lower()
    abstract = ''.join(c for c in abstract if c not in punctuation)
    abstract = word_tokenize(abstract)
    abstract = ' '.join([porter.stem(word) for word in abstract if  word not in eng_stopwords ])
   return abstract

# sanatize the string of one dict entry and write a file with the id and the sanatized string
def sanatize_csv_content(title,category,title2,category2):
    input_file = list(csv.DictReader(open(title)))
    field_names = ['id',category2]
    output_file = csv.DictWriter(open(title2, 'w'), fieldnames=field_names)
    output_file.writeheader()
    for row in input_file:
    	print("Sanatizing abstract {}".format(row['id']))
    	row[category] = sanatizer(row[category])
    	output_file.writerow(row)
    return 42     

if __name__ == "__main__":
	main()  