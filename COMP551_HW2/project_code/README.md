#Abstract Classification

## Naive Bayes

Example usage:
```	
	python predictor.py
```
Produces `.csv` file containing predicted categories. 

## Decision Trees

Example usage:

```
	python decision_tree.py -i ../Data/train_in.csv -o ../Data/train_out.csv -f 400 -e 1.5 -s 1000

	python decision_tree -h
```

A decision tree will be trained on `train_in.csv` and evaluated against `train_out.csv`. It will use 400 words as features and 
have an entropy threshold of 1.5, it will use 1000 examples to train the tree.


Will produce a file DTmetrics.txt containing the performance metrics of the decision tree classifier.
    

## SVM
Example usage:

```
	python svm_prediction.py linear

	python svm_rbf.py

	python svm.py
```

svm_rbf.py performs a grid search to find the optimal parameters for a gaussian-kernel SVM and outputs them to the screen
svm.py performs a grid search to find the optimal parameters for a linear-kernel SVM and outputs them to the screen
svm_prediction.py does a prediction using the optimal parameters found previously. It outputs a file output.csv containing the prediction. 

Arguments: rbf or linear. If rbf the gaussian kernel is used, if linear the linear kernel is used.