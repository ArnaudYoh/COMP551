# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:04:44 2016
pour Arnaud. 
@author: pcluc
"""

import matplotlib.pyplot as plt


import pandas as pd
import numpy as np
import linreg


from PIL import Image
from sklearn.cluster import SpectralClustering, KMeans
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn import linear_model
from keras.datasets import mnist

def convertLabels(labels):
    mapper = dict()
    
    for i in range(10):
        for j in range(10):
            summ = i + j
            if summ not in mapper : 
                mapper[summ] = [(i,j)]
            else : 
                mapper[summ] = mapper[summ] + [(i,j)]
                      
    converter = dict()
    
    for index in mapper.keys():
        vector = np.zeros((10))
        possibleValues = mapper[index]
        for tupple in possibleValues : 
            i, j = tupple
            vector[i] += 1
            vector[j] += 1
        vector = vector / np.sum(vector)
        converter[index] = vector  
        
    out = []
    
    for label in labels : 
        out.append(converter[label[0]])
        
    return out
    
# image is a 2d np array
# start a tupple representing the top left corner of the image
# take a 28x28 patch of a 60x60 image
def get_patch(image, start):
    out = []
    x, y = start
    if x > 45:
        x = 45
    if x < 14 : 
        x = 14
    if y > 45 : 
        y = 45
    if y < 14 : 
        y = 14
    for i in range(x - 14, x + 13):
        line = np.zeros((28))
        for j in range(y - 14, y + 13):
            line[j - (y-14)] = image[i][j]
        out.append(line)
    return out
            
          
def clusterData(data, kMeans=False, returnPoints=True):    
    k = 2
    if not kMeans : 
        kmeans = SpectralClustering(n_clusters=k)
    else : 
        kmeans = KMeans(n_clusters=k)
        
    kmeans.fit(data)
   
    labels = kmeans.labels_
    
    for i in range(k):       
        # select only data observations with cluster label == i
        ds = data[np.where(labels==i)]
        
        plt.plot(ds[:,0],ds[:,1],'o')
    plt.show()
    
    ds = data[np.where(labels==1)]
    ds2 = data[np.where(labels==0)]
  
    if ds.shape[0] > 0.90*data.shape[0]: 
        print('clustering failed to separate in 2 big clusters. removing smallest cluster')
        data = removeCluster(data, ds2)
        return clusterData(data)#kMeans=True)
    elif ds.shape[0] < 0.1*data.shape[0]:# and kMeans==False:
        print('clustering failed to separate in 2 big clusters. removing smallest cluster')
        data = removeCluster(data, ds)
        return clusterData(data)#kMeans=True)
        
    elif ds.shape[0] > 0.80*data.shape[0] and not kMeans: 
        print('clustering failed to separate in 2 big clusters. K means')
        return clusterData(data, kMeans=True)
    elif ds.shape[0] < 0.2*data.shape[0] and not kMeans:# and kMeans==False:
        print('clustering failed to separate in 2 big clusters. K means')
        return clusterData(data, kMeans=True)
    
    else : 
        # return the median (x, y) of both classes
        dss = [ds, ds2]
            
        if returnPoints:
            return dss
            
        tupples = []
        for classes in dss:
            x = classes[:,0]
            y = classes[:,1]
            x = np.sort(x)
            y = np.sort(y)
            index = x.shape[0]/2
            med_x = x[index]
            med_y = y[index]
            tupples.append((med_x, med_y))
        
        return tupples
            
        
    
# loc is a tupple (i,j), as in get_patch
# checks the amt of valid pixels given a point
def check_neighbor(image, loc, square=3, threshold=230):
    x, y = loc
    total = 0
    present = 0
    for i in range(-square, square):
        for j in range(-square, square):
            if x + i >= 0 and x + i < 60 and y + j >= 0 and y + j < 60 and (i != 0 or j !=0):
                total += 1
                if image[x+i][y+j] > threshold:
                    present += 1
    if total != 0:
        return float(present) / total 
    else :
        raise Exception('error : no neighboring pixels...')
        

# instead of extracting the patch directly from the image, let's make it from the data
# that was labelled/clustered. This way, we avoid having overlapping data in our patches.
def make_patch(data):
    # assume data is sorted
    x = data[:,0]
    y = data[:,1]
    x = np.sort(x)
    y = np.sort(y)
    
    index = x.shape[0]/2
    med_x = x[index]
    med_y = y[index]
    
    data = list(data)
    
    out = np.zeros((28,28))
    counter = [0,0]
    for i in range(med_x - 14, med_x + 14):
        for j in range(med_y - 14, med_y + 14):
            if in_array(data, (i,j)): 
                counter[0] += 1
                out[i - (med_x - 14)][j - (med_y - 14)] = 255
            else :
                counter[1] += 1
    return out

def in_array(data, tupple):
    x, y = tupple
    for tupple in data : 
        if tupple[0] == x and tupple[1] == y:
            return True
    return False
    
def removeCluster(data, cluster):
    clean = []
    for datapoint in data:
        x = datapoint[0]
        y = datapoint[1]
        addit = True
        for tupple in cluster : 
            if tupple[0] == x and tupple[1] == y:
                addit = False
        if addit : 
            clean.append(datapoint)
            
    clean = np.array(clean)
    if clean.shape == data.shape : 
        raise Exception('nothing was removed')
    
    return clean
            
        
        
# return a pair of 28x28 images to feed to CNN
def processImage(image):
    patches = []
    tupples = remove_background(image, True, returnTupple=True)
#    plt.imshow(image, cmap='Greys_r')
#    plt.show()

    points = clusterData(tupples)
    for cate in points : 
        patch = make_patch(cate)
        patches.append(patch)
    return patches
    
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
    
                

#%%

(X_train, y_train), (X_test, y_test) = mnist.load_data()
#print("X Shape", X_train.shape, "Y shape", y_train.shape)

cla = linear_model.LogisticRegression(solver='liblinear')
cla.fit(X_train[:20000].reshape(20000, X_train.shape[1] ** 2),y_train[:20000])
linreg.save_cla(cla, 'arnaudclaliblin2.pk1')

cla = linear_model.LogisticRegression(solver='lbfgs')
cla.fit(X_train[:20000].reshape(20000, X_train.shape[1] ** 2),y_train[:20000])
linreg.save_cla(cla, 'arnaudclalbfgs2.pk1')

cla = linear_model.LogisticRegression(solver='newton-cg')
cla.fit(X_train[:20000].reshape(20000, X_train.shape[1] ** 2),y_train[:20000])
linreg.save_cla(cla, 'arnaudclanewton2.pk1')

cla = linear_model.LogisticRegression(solver='sag')
cla.fit(X_train[:20000].reshape(20000, X_train.shape[1] ** 2),y_train[:20000])
linreg.save_cla(cla, 'arnaudclasag2.pk1')

#cla = linreg.load_cla('arnaudclasag2.pk1')


x_test = np.fromfile('train_x.bin', dtype='uint8')
x_test = x_test.reshape((100000,60,60))
Y_test = linreg.get_csv_int('train_y.csv',list('P'))
predictions = []
all_patches = []
for i in range(1000):
    print("processing " + str(i) + "th image.")
    #plt.imshow(x_test[i], cmap='Greys_r')
    #plt.show()
    patches = processImage(x_test[i])
    patches = np.array(patches)
    patches = patches.reshape(2,patches.shape[1] ** 2)
    #for patch in patches : 
    #    plt.imshow(patch, cmap='Greys_r')
    #    plt.show()
    all_patches.append(patches)

#all_patches = linreg.load_cla('patches.pk1')
linreg.save_cla(all_patches, 'patches.pk1')

results = []
for i in range(len(all_patches)):
    first_digit = cla.predict(all_patches[i][0])
    second_digit = cla.predict(all_patches[i][1])
#    print("First: ",first_digit)
#    print("Second: ", second_digit)
#    print("TEST: ", Y_test[i])
    results.append(first_digit[0] + second_digit[0])

print("Accuracy: ", accuracy_score(Y_test[:5],results))
print("Precision: ", precision_score(Y_test[:5],results))
print("F1 score: ", f1_score(Y_test[:5],results))
print("Recall: ", recall_score(Y_test[:5],results))


#%%
#for patches in all_patches : 
#    for patch in patches :
#        plt.imshow(patch.reshape((28,28)), cmap='Greys_r')
#        plt.show()
#    print("---------")
    

    
