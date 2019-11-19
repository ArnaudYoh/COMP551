import csv
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt

"""
Read a csv file
param input : name of the file to read
return : 3D list [sample, timestamps, features]
"""
def read_data(input):
	with open(input, 'rt') as f:
		reader = csv.reader(f)
		lines = list(reader)[1:] # get rid of first line

	# normalize environmental variables
	env_data = []
	for row in lines:
		env_data.append(row[8:11])
	scaler = MinMaxScaler(feature_range=(0, 1))
	env_data = scaler.fit_transform(np.array(env_data))

	# extract timestamps in the form (sample number, list of env variables)
	timestamps = []
	for i in range(len(lines)):
		timestamps.append((lines[i][0], env_data[i]))

	# gather timestamps with the same sample number
	samples = {}
	for ts in timestamps:
		sampleNum, features = ts
		if sampleNum in samples:
			samples[sampleNum].append(features)
		else:
			samples[sampleNum] = [features]

	# convert samples into 3D list [sample, timestamps, features]
	output = []
	for sampleNum in samples:
		output.append(samples[sampleNum])
	
	return output

""" 
Get data in format that can be fed to RNN 
return : 
	 - X is a 3D numpy array in the form [sample, timestamps, features]
	where each sample is made of a sequence of timestamps zero padded at the beginning
	- y is a 1D numpy array
"""
def get_data():
	# read data
	X_pos = read_data('data/clean_north_positive.csv')
	X_neg = read_data('data/clean_north_negative.csv')
	X = X_pos + X_neg
	y = np.concatenate((np.ones(len(X_pos)), np.zeros(len(X_neg))))

	# pad sequences with zeros at beginning
	max_len = len(max(X,key=len))
	for sample in X:
		len_to_pad = max_len - len(sample)
		for i in range(len_to_pad):
			sample.insert(0, [0., 0., 0.])

	X = np.array(X).astype('float32')
	
	return X, y




# fix random seed for reproducibility
np.random.seed(33)

# get data in right format
X, y = get_data()
# split into training and validation sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)

# create model
model = Sequential()
model.add(LSTM(4, input_dim=3)) # 3 features
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X_train, y_train, validation_data=[X_test, y_test], nb_epoch=120, batch_size=1)

# visualize results
plt.figure(1)
plt.subplot(121)
plt.xlabel('Number of training epochs')
plt.ylabel('Mean cross-entropy error')
plt.plot(history.history['loss'], color='g', label='Training loss');
plt.plot(history.history['val_loss'], color='b', label='Validation loss');
plt.legend(loc=1)
plt.subplot(122)
plt.xlabel('Number of training epochs')
plt.ylabel('Accuracy')
plt.plot(history.history['acc'], color='y', label='Training accuracy')
plt.plot(history.history['val_acc'], color='r', label='Validation accuracy')
plt.legend(loc=4)
plt.show()
plt.savefig("plots/rnn_results.png")

























