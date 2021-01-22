# -*- coding: utf-8 -*-
"""xgb_symbol_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oeMkr6YFssz2Hw7cUe0EMNL9xbhjjPPJ

# Code Modules & Helpful Functions
"""

import warnings; warnings.filterwarnings('ignore')
import os,h5py,urllib,zipfile
import pandas as pd,numpy as np,xgboost as xgb
import pylab as pl,seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
from keras.datasets import mnist
from keras.utils import to_categorical

def ohe(x): 
    return OneHotEncoder(categories='auto')\
           .fit(x.reshape(-1,1))\
           .transform(x.reshape(-1,1))\
           .toarray().astype('int64')
def tts(X,y): 
    x_train,x_test,y_train,y_test=\
    train_test_split(X,y,test_size=float(.2),
                     random_state=1)
    n=int(len(x_test)/2)
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    return x_train,x_valid,x_test,y_train,y_valid,y_test

"""# Data Loading & Preprocessing"""

(x_train1,y_train1),(x_test1,y_test1)=mnist.load_data()
n=int(len(x_test1)/2)
x_valid1,y_valid1=x_test1[:n],y_test1[:n]
x_test1,y_test1=x_test1[n:],y_test1[n:]
#cy_train1=to_categorical(y_train1,10)
#cy_valid1=to_categorical(y_valid1,10)
#cy_test1=to_categorical(y_test1,10)
x_train1=x_train1.reshape(-1,784)
x_test1=x_test1.reshape(-1,784)
x_valid1=x_valid1.reshape(-1,784)
[el.shape for el in [x_train1,x_valid1,x_test1,
                     y_train1,y_valid1,y_test1]]

fpath='https://olgabelitskaya.github.io/'
zf='LetterColorImages_123.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb')
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys())
letters=u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
letter_backgrounds=np.array(f[keys[0]])
letter_images=np.array(f[keys[1]])/255
letter_labels=np.array(f[keys[2]])
pl.figure(figsize=(2,3)); il=10**4
pl.xticks([]); pl.yticks([])
pl.title('Label: %s \n'%letters[letter_labels[il]-1]+\
         'Background: %s'%letter_backgrounds[il],
         fontsize=18)
pl.imshow(letter_images[il]); pl.show()

letter_gimages=np.dot(letter_images[...,:3],[.299,.587,.114])
pl.figure(figsize=(2,3))
pl.title('Label: %s \n'%letters[letter_labels[il]-1]+\
         'Background: %s'%letter_backgrounds[il],
         fontsize=18)
pl.imshow(letter_gimages[il],cmap=pl.cm.bone)
pl.xticks([]); pl.yticks([]); pl.show()

letter_cbackgrounds,letter_clabels=\
ohe(letter_backgrounds),ohe(letter_labels)
letter_ctargets=\
np.concatenate((letter_clabels,letter_cbackgrounds),axis=1)
pd.DataFrame([letter_clabels.shape,letter_cbackgrounds.shape,
              letter_ctargets.shape])

x_train2,x_valid2,x_test2,\
y_train2,y_valid2,y_test2=tts(letter_images,letter_labels)
x_train3,x_valid3,x_test3,\
y_train3,y_valid3,y_test3=tts(letter_gimages,letter_labels)
#ny_train2=np.array([np.argmax(y) for y in y_train2])
#ny_valid2=np.array([np.argmax(y) for y in y_valid2])
#ny_test2=np.array([np.argmax(y) for y in y_test2])
#ny_train3=np.array([np.argmax(y) for y in y_train3])
#ny_valid3=np.array([np.argmax(y) for y in y_valid3])
#ny_test3=np.array([np.argmax(y) for y in y_test3])
[el.shape for el in [x_train2,x_valid2,x_test2,
                     y_train2,y_valid2,y_test2,
                     x_train3,x_valid3,x_test3,
                     y_train3,y_valid3,y_test3]]

"""# Models"""

params={'objective':'multi:softprob','verbosity':2,
        'random_state':42,'num_class':10,
        'n_estimators':784,'learning_rate':.3,'max_depth':11,
        'tree_method':'gpu_hist','predictor':'gpu_predictor'}
clf=xgb.XGBClassifier(**params)
clf.fit(x_train1,y_train1,eval_metric='mlogloss',
        eval_set=[(x_train1,y_train1),(x_valid1,y_valid1)])

print(clf.evals_result())
y_xgb_train1=clf.predict(x_train1)
y_xgb_valid1=clf.predict(x_valid1)
y_xgb_test1=clf.predict(x_test1)
for [y,py] in [[y_train1,y_xgb_train1],
               [y_valid1,y_xgb_valid1],
               [y_test1,y_xgb_test1]]:
    print(metrics.accuracy_score(y,py))
    print(metrics.confusion_matrix(y,py))

clf2=xgb.XGBClassifier(objective="multi:softprob",
                       verbosity=2,num_class=33,
                       random_state=42,learning_rate=.05,
                       max_depth=11,n_estimators=256,
                       tree_method='gpu_hist',predictor='gpu_predictor')
clf2.fit(x_train2.reshape(-1,32*32*3),y_train2,eval_metric='mlogloss',
         eval_set=[(x_train2.reshape(-1,32*32*3),y_train2),
                   (x_valid2.reshape(-1,32*32*3),y_valid2)])

print(clf2.evals_result())
y_xgb_train2=clf2.predict(x_train2.reshape(-1,32*32*3))
y_xgb_valid2=clf2.predict(x_valid2.reshape(-1,32*32*3))
y_xgb_test2=clf2.predict(x_test2.reshape(-1,32*32*3))
for [y,py] in [[y_train2,y_xgb_train2],
               [y_valid2,y_xgb_valid2],
               [y_test2,y_xgb_test2]]:
    print(metrics.accuracy_score(y,py))
    print(metrics.confusion_matrix(y,py))

clf3=xgb.XGBClassifier(objective="multi:softprob",
                       verbosity=2,num_class=33,
                       random_state=42,max_depth=16,
                       tree_method='gpu_hist',predictor='gpu_predictor')
clf3.fit(x_train3.reshape(-1,32*32),y_train3,eval_metric='mlogloss',
         eval_set=[(x_train3.reshape(-1,32*32),y_train3),
                   (x_valid3.reshape(-1,32*32),y_valid3)])

print(clf3.evals_result())
y_xgb_train3=clf3.predict(x_train3.reshape(-1,32*32))
y_xgb_valid3=clf3.predict(x_valid3.reshape(-1,32*32))
y_xgb_test3=clf3.predict(x_test3.reshape(-1,32*32))
for [y,py] in [[y_train3,y_xgb_train3],
               [y_valid3,y_xgb_valid3],
               [y_test3,y_xgb_test3]]:
    print(metrics.accuracy_score(y,py))
    print(metrics.confusion_matrix(y,py))