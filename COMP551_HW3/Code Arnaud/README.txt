We have five files:
	- train_y.csv is a modified version of the given train output
	- linreg.py: contains function that are used by other files
	- eval.py: evaluates a "saved" classifier's accuracy, precision,f1-score and recall
	- MNISTtest.py: contains code for evaluating our learners on MNIST data. 
	- LogReg_Clustering.py: Train the learners on MNIST data and then apply the clustering algorithm on the train input and make predictions. 


Simply executing LogReg_Clustering.py will be sufficient to train the 4 Logistic_Regression classifiers we want. The classifiers will be saved in .pk1 files.You can load the classifiers by de-commenting the lines containing "load_cla". 