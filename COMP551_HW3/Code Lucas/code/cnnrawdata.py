from __future__ import print_function
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 17:07:44 2016
@author: taken from : 
https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py
"""

import numpy as np
import pandas as pd
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import model_from_json
import os
import matplotlib.pyplot as plt
from keras.utils.visualize_util import plot

# GLOBAL VARIABLES : 

batch_size = 128
nb_classes = 55
nb_epoch = 5 # 12, cuz aint nobody got time for that

# input image dimensions
img_rows, img_cols = 60, 60
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)
# number of examples in 1 file
ex_per_file = 25000

repo_x_name = 'data/img_with_bg'
repo_y_name = 'data/label_no_bg'

#%%#################################################
#                      METHODS                   ###
####################################################
def loadData(index):
    x = np.load(repo_x_name + str(index) + '.npy')
    x = x.reshape((ex_per_file,60,60))
    y = np.load(repo_y_name + str(index) + '.npy')
    
    return x, y

def formatData(X, getInputShape=False):
    if K.image_dim_ordering() == 'th':
        print('here')
        X = X.reshape(X.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        print('not here')
        X = X.reshape(X.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)
    
    X = X.astype('float32')
    X /= 255
    print('X shape:', X.shape)
    print(X.shape[0], 'samples')
    
    if getInputShape : 
        return X, input_shape
    else : 
        return X

# check graph image to recreate previous architecture 

def createModel(input_shape):
    model = Sequential()
    # input shape = (100000, 60, 60, 1)
    
    #first convolution layer
    model.add(Convolution2D(32, 7, 7,
                            border_mode='same',
                            input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.5))
    
    # second convolution layer
    model.add(Convolution2D(64, 5, 5, border_mode='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.5))
    
    # third convolution layer
    model.add(Convolution2D(128, 4, 4, border_mode='valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.5))  
    
    # flattening the convolution layers
    model.add(Flatten())
    
    # first dense layer
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    # second dense layer
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))  
    
    # final output layer
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    return model

#%%#################################################
#             TRAINING SECTION                   ###
####################################################

# real shit going down : 
x_test , y_test = loadData(0)
remove_bg(x_test)
x_test, input_shape = formatData(x_test, getInputShape=True)
#%%
#remove_bg(x_test)
model = createModel(input_shape)
    
#%%
for i in range(6,250): # restart at 6
    index = i % 50 + 1
    x_train, y_train = loadData(index)
    remove_bg(x_train)
    x_train = formatData(x_train)
    model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=1,
          verbose=1, validation_data=(x_test[:10000], y_test[:10000]))
          
    if i %  5 == 0 : 
        model_json = model.to_json()
        with open("model_new3.json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights("model_new3.h5")
        print("saved model to disk")

=#%%#################################################
#             SAVING MODEL SECTION               ###
####################################################
model_json = model.to_json()
with open("model_new3.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model_new3.h5")
print("saved model to disk")

#%%#################################################
#             LOADING MODEL SECTION              ###
####################################################
json_file = open('model_new3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('model_new3.h5')
print('loaded model from disk')

# remains to compile the model : 
loaded_model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
                  
model = loaded_model
#%%#################################################
#            TESTING MODEL SECTION  ?            ###
####################################################
x_test , y_test = loadData(0)  

x_test = formatData(x_test)       
score = loaded_model.evaluate(x_test, y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])


#%%
# looking at my data with added backgrounds
x_test , y_test = loadData(1)  

x_test = x_test[:100]
for i in range(0, 10):
    plt.imshow(x_test[i].reshape((60,60)), cmap='Greys_r')
    plt.show()
remove_bg(x_test)
for i in range(0, 10):
    plt.imshow(x_test[i].reshape((60,60)), cmap='Greys_r')
    plt.show()

#%%
x_test_no_bg = np.array(x_test)
for i in range(x_test.shape[0]):
    remove_background(x_test_no_bg[i], False)
#%%%    
x_test_pred = loaded_model.predict(x_test_no_bg)
x_test_pred_formatted = formatAnswer(x_test_pred)
#%%
acc = accuracy(x_test_pred_formatted, formatAnswer(y_test))
# bagging : 
#%%
#pred_bg = model.predict(x_test)
best = getMostConfident([x_test_pred, pred_bg])

acc = accuracy(best, formatAnswer(y_test))

    
# ideas : try the same predictor, but with different threshold values. Then, take the most confident
# or simply take the average
#%%
