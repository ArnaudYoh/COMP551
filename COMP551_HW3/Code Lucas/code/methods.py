# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 17:03:23 2016
methods 
@author: pcluc
"""

    
#%%#################################################
#                      METHODS                   ###
####################################################

import random
import numpy as np
from keras.datasets import mnist
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from sklearn.cluster import SpectralClustering, KMeans
import numpy as np

def getTopLeft(limit=12):
    
    distance = 0
    while distance < limit:
        x1 = random.randint(0, 60 - 29)
        x2 = random.randint(0, 60 - 29)
        y1 = random.randint(0, 60 - 29)
        y2 = random.randint(0, 60 - 29)
        
        distance = np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2)
    return [(x1, y1), (x2, y2)]
    

def mergeImages(images, limit=12):
    topLeft = getTopLeft(limit)
    image = np.zeros((60,60))
    
    for index in range(2):
        x, y = topLeft[index]
        for i in range(28):
            for j in range(28):
                image[i + x][j + y] = max(image[i + x][j + y], images[index][i][j])
    
    return image

def addNoise(img, clusters, radius):
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            p = random.randint(0,100)
            if p > 98:
                radius_x = 1#random.randint(0,4)
                radius_y = 1#random.randint(0,4)
                for ii in range(max(0, i - radius_x), min(59, i + radius_x)):
                    for jj in range(max(0, j - radius_y), min(59, j + radius_y)):
                        if random.randint(0,100) > 30:
                            img[ii][jj] = 255
def getBackgrounds():
    images = []
    for i in range(0,12):
        img = Image.open('bg' + str(i) + '.png').convert('L')
        images.append(np.array(img))
    return images
    
def getBackgroundSample(images, eazy=100, index=-1):
    if index == -1:
        index = random.randint(0,len(images) -1)
    img = images[index]
    x = random.randint(0, img.shape[0] -60)
    y = random.randint(0, img.shape[1] -60)
    bg = np.zeros((60,60)) 
    for i in range(60):
        for j in range(60):
            bg[i][j] = img[i+x][j+y]
    return bg / eazy
    
def addBackground(img, background):
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            img[i][j] = max(img[i][j], background[i][j])   
    return img
    
def getDict():
    mapper = dict()
    summ = dict()
    index = 0
    for i in range(0,10):
        for j in range(0,10):
            if (i,j) not in mapper and (j,i) not in mapper : 
                mapper[(i,j)] = index
                mapper[(j,i)] = index
                summ[index] = i + j
                index += 1
    return mapper, summ
    
    
def remove_bg(array):
    for ex in array : 
        remove_background(ex, False)
    
    
    
def remove_background(t, removeNoise, returnTupple=False, threshold=0.9, returnPercentageRemoved=False): 
    # first pass : remove background
    tupples = []
    count = [0,0]
    maxx = np.max(t)
    threshold *= maxx
    for i in range(0,t.shape[0]) : 
        for j in range(0,t.shape[1]) : 
            value = t[i][j]
                
            if removeNoise :
                if check_neighbor(t, (i,j)) > 0.05 and value >= threshold:
                    tupples.append([i,j])
                else : 
                    t[i][j] = 0
            else : 
                if value >= threshold : 
                    # TODO : might have to reverse this
                    t[i][j] = maxx
                    tupples.append([i,j])
                    count[0] += 1
                else : 
                    t[i][j] = 0
                    count[1] += 1
                

    if returnTupple : 
        tupples = np.array(tupples)
        #print("tupple shape : " + str(tupples.shape))
        kept = 100. * tupples.shape[0] / float(t.shape[0]*t.shape[1])
        #print("kept : " + str(kept) + " % of the data")
        if kept > 35:
            if threshold == 245:
                #plt.imshow(t, cmap='Greys_r')
                #plt.show()
                raise Exception('problem with image : kept : ' + str(kept))
            else : 
                return remove_background(t, removeNoise, returnTupple=True, threshold=maxx)
        else : 
            return tupples
    
    if returnPercentageRemoved:
        return float(count[0])/count[1]

def predict(model, patches):
    total = 0
    for patch in patches : 
        total += np.argmax(model.predict(patch.reshape(-1,28,28,1)))
    return total
    
def accuracy(pred, labels):
        delta = np.array(pred) - np.array(labels)
        wrong = 0
        for guess in delta:
            if guess != 0 : 
                wrong += 1
        return 1 - (float(wrong)) / len(pred)
        
def formatAnswer(pred):
    # need to create dicts first : 
    mapper, inv = getDict()
    out = []
    for p in pred : 
        out.append(inv[np.argmax(p)])
    return np.array(out)
    
def getMostConfidentOld(pred1, pred2):
    # need to create dicts first : 
    mapper, inv = getDict()
    out = []
    for i in range(pred1.shape[0]):
        max1 = pred1[i][np.argmax(pred1[i])]
        max2 = pred2[i][np.argmax(pred2[i])]
        if max1 > max2 : 
            out.append(inv[np.argmax(pred1[i])])
        else : 
            out.append(inv[np.argmax(pred2[i])])
    return np.array(out)
    
        
def getMostConfident(predictions):
    # need to create dicts first : 
    mapper, inv = getDict()
    out = []
    for i in range(predictions[0].shape[0]):
        best_confidence = 0
        best_pred = None
        for j in range(len(predictions)):
            model = predictions[j]
            model_confidence = model[i][np.argmax(model[i])]
            if model_confidence > best_confidence : 
                best_confidence = model_confidence
                best_pred = inv[np.argmax(model[i])]
        out.append(best_pred)
    
    return np.array(out)

        
    
    
                
        
        
    
    
                

