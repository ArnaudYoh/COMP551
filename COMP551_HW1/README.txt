README 

Language we use is MATLAB

For Q1. It includes files :
	cross_val.m : cross_val function for determine lambda and learningRate
	cross_val2.m : determine when to stop the training
	FscoreCollection.m: calcuate the Fscore for both val and training matrix
	higher_order.m: map features to higher order
	logisticRegression.m: logistic regression function
	meanNormalization.m: Doing mean Normalization to input matrix
	mg_sums.m: helper function for high_order.m dont use it alone
	predict.m: predict the binary result
	purepredict.m: predict the probability result
	sigmoid.m:sigmoid function
	training.m: normal training logistic regression
	training_t.m: training in cross_val2.m
	training1.m: training in cross_val.m
	weightUpdate.m: momentum update for weight
	question1.m: main function which has 4 modes, details in the file.

Xiru's Files
	comp_551_a1.m -> Data scraping Program. Will generate the necessary files for bayes_test and anything utilized above.
			 Simply run and it will do everything but takes while.
	bayes_test.m
			This is our bayes model which computes the prediction values and packages everything nicely into one. 
			Requires to run the program above first

	aggregate.m     Aggregates the results into the submission matrix. Requires all results to have been run and the data in the workspace. 


Question 3 files : 
	higher_order.m: INPUT : the features matrix and the order we want to have
			map features to higher order
	mg_sums.m: 
			helper function for high_order.m, not meant to be used alone. 
	closed_form.m : INPUT : The feature matrix and the Y matrix
			Helps computing the weights of the linear regression we modeled. 
	tester.m : The X and Y matrix for the learning part and the input feature matrix to make the predictions. 
			Main function that computes the prediction using linear regression, it will also display a square-error value based on the y_matrix you provide. 