# -*- coding: utf-8 -*-
"""decor_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Tt3qZePsf2P6kNNao-hQ58DlG71Abj5a

# 📑 &nbsp; Deep Learning. P5: Decor Recognition & Colorization
<a href="https://olgabelitskaya.github.io/README.html">&#x1F300; &nbsp; Home Page &nbsp; &nbsp; &nbsp;</a> 
<a href="https://www.instagram.com/olga.belitskaya/">&#x1F300; &nbsp; Instagram Posts &nbsp; &nbsp; &nbsp;</a>
<a href="https://www.pinterest.ru/olga_belitskaya/code-style/">&#x1F300; &nbsp; Pinterest Posts</a><br/>
"""

import pylab; from skimage import io,color,measure
def vector(file,cm,level=.75):
    path1='https://olgabelitskaya.github.io/'
    path2='pattern0%s'%(file)+'.jpeg'
    img=io.imread(path1+path2); level=level
    gray_img=color.colorconv.rgb2grey(img) 
    contours=measure.find_contours(gray_img,level)
    n=len(contours)
    pylab.figure(figsize=(int(7),int(7)))
    pylab.gca().invert_yaxis()
    [pylab.plot(contours[i][:,int(1)],
                contours[i][:,int(0)],lw=.5,
                color=pylab.get_cmap(cm)(i/n)) 
     for i in range(n)]
    pylab.xticks([]); pylab.yticks([]); pylab.show()
vector(1,'autumn')

"""## ✒️ &nbsp;Step 0. Import Libraries"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import h5py,urllib,zipfile
import pandas as pd,numpy as np,pylab as pl
import seaborn as sn,keras as ks,tensorflow as tf
from skimage.transform import resize
import warnings; warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
np.set_printoptions(precision=6)
pl.style.use('seaborn-whitegrid')
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential,load_model,Model
from keras.layers import Input,Activation,Dense,LSTM
from keras.layers import Flatten,Dropout,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import GlobalAveragePooling2D,GlobalMaxPooling2D
from keras.layers.advanced_activations import PReLU,LeakyReLU
from keras import __version__
print('keras version:', __version__)
print('tensorflow version:',tf.__version__)

fw='weights.decor.hdf5'
dr2,dr25,dr3,dr5=\
float(.2),float(.25),float(.3),float(.5)
fr,al=float(.5),float(.02)
[i0,i1,i2,i3,i4,i5,i6]=\
[int(0),int(1),int(2),int(3),int(4),int(5),int(6)]
[i7,i8,i10,i11,i12,i16]=\
[int(7),int(8),int(10),int(11),int(12),int(16)]
[i20,i32,i48,i50,i64,i96]=\
[int(20),int(32),int(48),int(50),int(64),int(96)]
[i100,i128,i150,i196,i200]=\
[int(100),int(128),int(150),int(196),int(200)]
[i256,i512,i1024,i2048]=\
[int(256),int(512),int(1024),int(2048)]

def ohe(x): 
    return OneHotEncoder(categories='auto')\
           .fit(x.reshape(-i1,i1))\
           .transform(x.reshape(-i1,i1))\
           .toarray().astype('int64')
def tts(X,y): 
    x_train,x_test,y_train,y_test=\
    train_test_split(X,y,test_size=float(.2),
                     random_state=i1)
    n=int(len(x_test)/2)
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    return x_train,x_valid,x_test,y_train,y_valid,y_test
def resh(x,n):
    y=[resize(el,(n,n,i3),
              anti_aliasing=True) for el in x]
    return np.array(y)
def gresh(x,n): 
    y=np.array([resize(el,(n,n,i1),
                       anti_aliasing=True) for el in x])
    return y.reshape(-i1,n,n,i1)

def history_plot(fit_history):
    pl.figure(figsize=(12,10)); pl.subplot(211)
    keys=list(fit_history.history.keys())[0:4]
    pl.plot(fit_history.history[keys[0]],
            color='crimson',label='train')
    pl.plot(fit_history.history[keys[2]],
            color='firebrick',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid()
    pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[1]],
            color='crimson',label='train')
    pl.plot(fit_history.history[keys[3]],
            color='firebrick',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid()
    pl.title('Accuracy'); pl.show()
def history_plot2(fit_history):
    lk=[1,2,3]
    keys=list(fit_history.history.keys())[8:]
    pl.figure(figsize=(12,10)); pl.subplot(211)
    pl.plot(fit_history.history[keys[0]],
            color='crimson',label='valid 1')
    pl.plot(fit_history.history[keys[1]],
            color='firebrick',label='valid 2')
    pl.plot(fit_history.history[keys[2]],
            color='#FF355E',label='valid 3')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid(); pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[3]],
            color='crimson',label='valid 1')
    pl.plot(fit_history.history[keys[4]],
            color='firebrick',label='valid 2')
    pl.plot(fit_history.history[keys[5]],
            color='#FF355E',label='valid 3')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid(); pl.title('Accuracy'); pl.show()

"""## ✒️ &nbsp;Step 1. Load and Explore the Data"""

fpath='https://olgabelitskaya.github.io/'
zf='DecorColorImages.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb')
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys())
[countries,decors,images,types]=\
[np.array(f[keys[i]]) for i in range(4)]
pd.DataFrame([el.shape for el in 
              [countries,decors,images,types]])

fpath2='https://raw.githubusercontent.com/OlgaBelitskaya/'+\
       'deep_learning_projects/master/DL_PP5/'
data=pd.read_csv(fpath2+'decor.txt')
n=np.random.choice(484,size=6,replace=False)
data.loc[n]

images=images/255
fig=pl.figure(figsize=(12,5))
for i,idx in enumerate(n):
    ax=fig.add_subplot(2,3,i+1,xticks=[],yticks=[])
    ax.imshow(images[idx])
    ax.set_title(data['country'][idx]+'; '+\
                 data['decor'][idx]+'; '+data['type'][idx])
pl.show()

gray_images=np.dot(images[...,:3],[.299,.587,.114])
pl.figure(figsize=(3,3))
n=np.random.choice(484,size=1,replace=False)[0]
pl.imshow(images[n])
pl.title(data['country'][n]+'; '+\
         data['decor'][n]+'; '+data['type'][n])
pl.imshow(gray_images[n],cmap=pl.cm.bone); pl.show()
gray_images=gray_images.reshape(-1,150,150,1)

ccountries,cdecors,ctypes=\
ohe(countries),ohe(decors),ohe(types)
ctargets=np.concatenate((ccountries,cdecors),axis=1)
ctargets=np.concatenate((ctargets,ctypes),axis=1)
pd.DataFrame([images.shape,gray_images.shape,
              ccountries.shape,cdecors.shape,
              ctypes.shape,ctargets.shape])

# Color Images / Countries 
x_train1,x_valid1,x_test1,\
y_train1,y_valid1,y_test1=tts(images,ccountries)
# Grayscaled Images / Countries 
x_train2,x_valid2,x_test2,\
y_train2,y_valid2,y_test2=tts(gray_images,ccountries)
# Color Images / Decors 
x_train3,x_valid3,x_test3,\
y_train3,y_valid3,y_test3=tts(images,cdecors)
# Grayscaled Images / Decors 
x_train4,x_valid4,x_test4,\
y_train4,y_valid4,y_test4=tts(gray_images,cdecors)
# Color Images / Multi-Label Targets
x_train5,x_valid5,x_test5,\
y_train5,y_valid5,y_test5=tts(images,ctargets)
# Grayscaled Images / Multi-Label Targets 
x_train6,x_valid6,x_test6,\
y_train6,y_valid6,y_test6=tts(gray_images,ctargets)
sh=[el.shape for el in \
[x_train1,y_train1,x_valid1,y_valid1,x_test1,y_test1,
 x_train3,y_train3,x_valid3,y_valid3,x_test3,y_test3,
 x_train5,y_train5,x_valid5,y_valid5,x_test5,y_test5]]
sh2=[el.shape for el in \
[x_train2,y_train2,x_valid2,y_valid2,x_test2,y_test2,
 x_train4,y_train4,x_valid4,y_valid4,x_test4,y_test4,
 x_train6,y_train6,x_valid6,y_valid6,x_test6,y_test6]]
pd.DataFrame([sh,sh2]).T

y_train5_list=[y_train5[:,:i4],y_train5[:,i4:i11], y_train5[:,i11:]]
y_test5_list=[y_test5[:,:i4],y_test5[:,i4:i11], y_test5[:,i11:]]
y_valid5_list=[y_valid5[:,:i4],y_valid5[:,i4:i11], y_valid5[:,i11:]]
y_train6_list=[y_train6[:,:i4],y_train6[:,i4:i11], y_train6[:,i11:]]
y_test6_list=[y_test6[:,:i4],y_test6[:,i4:i11], y_test6[:,i11:]]
y_valid6_list=[y_valid6[:,:i4],y_valid6[:,i4:i11], y_valid6[:,i11:]]

"""## ✒️&nbsp;Step 2. One-Label Classification Models"""

# Color Images / Countries
def model():
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same',
                     input_shape=x_train1.shape[i1:]))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i96,(i5,i5)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))   
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i512,activation='relu'))
    model.add(Dropout(dr25))    
    model.add(Dense(i4))
    model.add(Activation('softmax'))   
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])   
    return model
model=model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=model.fit(x_train1,y_train1,epochs=i32,
                  batch_size=i16,verbose=i2,
                  validation_data=(x_valid1,y_valid1),
                  callbacks=[checkpointer,lr_reduction])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test1,y_test1)

# Color Images / Decors
def model(leaky_alpha):
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train3.shape[i1:]))
    model.add(LeakyReLU(alpha=leaky_alpha))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i96,(i5,i5)))
    model.add(LeakyReLU(alpha=leaky_alpha))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))   
    model.add(GlobalMaxPooling2D())     
    model.add(Dense(i512))
    model.add(LeakyReLU(alpha=leaky_alpha))
    model.add(Dropout(dr25))     
    model.add(Dense(i7))
    model.add(Activation('softmax'))   
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])   
    return model
model=model(float(.005))

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=model.fit(x_train3,y_train3, 
                  epochs=i48,batch_size=i16,verbose=i2,
                  validation_data=(x_valid3,y_valid3),
                  callbacks=[checkpointer,lr_reduction])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test3,y_test3)

# Grayscaled Images / Countries
def gray_model():
    model=Sequential()
    model.add(Conv2D(i16,(i5,i5),padding='same', 
                     input_shape=x_train2.shape[i1:]))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i128,(i5,i5)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))   
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i512,activation='tanh'))
    model.add(Dropout(dr25))
    model.add(Dense(i4))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])
    return model
gray_model=gray_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=gray_model.fit(x_train2,y_train2, 
                       epochs=i64,batch_size=i16,verbose=i2,
                       validation_data=(x_valid2,y_valid2),
                       callbacks=[checkpointer,lr_reduction])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test2,y_test2)

# Grayscaled Images / Decors
def gray_model(leaky_alpha):
    model=Sequential()
    model.add(Conv2D(i16,(i5,i5),padding='same', 
                     input_shape=x_train4.shape[i1:]))
    model.add(LeakyReLU(alpha=leaky_alpha))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i128,(i5,i5)))
    model.add(LeakyReLU(alpha=leaky_alpha))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))  
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i512, activation='tanh'))
    model.add(Dropout(dr25))   
    model.add(Dense(i7))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])
    return model
gray_model=gray_model(float(.01))

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=gray_model.fit(x_train4,y_train4, 
                       epochs=i64,batch_size=i16,verbose=i2,
                       validation_data=(x_valid4,y_valid4),
                       callbacks=[checkpointer,lr_reduction])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test4,y_test4)

"""## ✒️&nbsp;Step 3. Multi-Label Classification Models"""

def multi_model(leaky_alpha):    
    model_input=Input(shape=x_train5.shape[i1:])
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i5,i5),padding='same')(model_input)
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)   
    x=Conv2D(i128,(i5,i5),padding='same')(x)
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)            
    x=GlobalMaxPooling2D()(x)  
    x=Dense(i512)(x) 
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=Dropout(dr25)(x)    
    y1=Dense(i4,activation='softmax')(x)
    y2=Dense(i7,activation='softmax')(x)
    y3=Dense(i2,activation='softmax')(x)   
    model=Model(inputs=model_input,outputs=[y1,y2,y3])
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])   
    return model
multi_model=multi_model(float(.005))

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=multi_model.fit(x_train5,y_train5_list, 
                        epochs=i48,batch_size=i16,verbose=i2,
                        validation_data=(x_valid5,y_valid5_list),
                        callbacks=[checkpointer,lr_reduction])

multi_model.load_weights(fw)
multi_scores=multi_model.evaluate(x_test5,y_test5_list,verbose=0)
print("Scores: \n" ,(multi_scores))
print("Country label. Accuracy: %.2f%%"%(multi_scores[i4]*100))
print("Decor label. Accuracy: %.2f%%"%(multi_scores[i5]*100))
print("Type label. Accuracy: %.2f%%"%(multi_scores[i6]*100))

history_plot2(history)

def gray_multi_model(leaky_alpha):    
    model_input=Input(shape=x_train6.shape[i1:])
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i5,i5), padding='same')(model_input)
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)  
    x=Conv2D(i256,(i5,i5),padding='same')(x)
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)             
    x=GlobalMaxPooling2D()(x) 
    x=Dense(i2048)(x) 
    x=LeakyReLU(alpha=leaky_alpha)(x)
    x=Dropout(dr25)(x)   
    y1=Dense(i4,activation='softmax')(x)
    y2=Dense(i7,activation='softmax')(x)
    y3=Dense(i2,activation='softmax')(x) 
    model=Model(inputs=model_input,outputs=[y1,y2,y3])   
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])  
    return model
gray_multi_model=gray_multi_model(float(.01))

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=gray_multi_model.fit(x_train6,y_train6_list,
                             epochs=i48,batch_size=i16,verbose=i2,
                             validation_data=(x_valid6,y_valid6_list),
                             callbacks=[checkpointer,lr_reduction])

gray_multi_model.load_weights(fw)
gray_multi_scores=\
gray_multi_model.evaluate(x_test6,y_test6_list,verbose=i0)
print("Scores: \n" ,(gray_multi_scores))
print("Country label. Accuracy: %.2f%%"%(gray_multi_scores[4]*100))
print("Decor label. Accuracy: %.2f%%"%(gray_multi_scores[5]*100))
print("Type label. Accuracy: %.2f%%"%(gray_multi_scores[6]*100))

history_plot2(history)

"""## ✒️  Step 4. Keras Applications"""

from keras.applications.resnet50 import \
ResNet50,preprocess_input as rn50pi
from keras.applications.inception_v3 import \
InceptionV3,preprocess_input as iv3pi
from keras.applications.xception \
import Xception,preprocess_input as xpi
from keras.applications.inception_resnet_v2 import \
InceptionResNetV2,preprocess_input as iv2pi
import scipy; from scipy import misc

resize_x_train3=np.array([resize(x_train3[i],(180,180,3)) 
                          for i in range(0,len(x_train3))]).astype('float32')
resize_x_valid3=np.array([resize(x_valid3[i],(180,180,3)) 
                          for i in range(0,len(x_valid3))]).astype('float32')
resize_x_test3=np.array([resize(x_test3[i],(180,180,3)) 
                          for i in range(0,len(x_test3))]).astype('float32')
#x_train_bn3=rn50pi(resize_x_train3)
#x_valid_bn3=rn50pi(resize_x_valid3)
#x_test_bn3=rn50pi(resize_x_test3)
resnet50base_model=\
ResNet50(weights='imagenet',include_top=False)
x_train_bn3=resnet50base_model.predict(resize_x_train3)
x_valid_bn3=resnet50base_model.predict(resize_x_valid3)
x_test_bn3=resnet50base_model.predict(resize_x_test3)

sh=x_train_bn3.shape[1:]
def resnet50_model():
    model=Sequential()
    model.add(GlobalAveragePooling2D(input_shape=sh))    
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.5))        
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.5))
    model.add(Dense(7, activation='softmax'))   
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
resnet50_model=resnet50_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.75)
estopping=EarlyStopping(monitor='val_loss',patience=16,verbose=2)
history=\
resnet50_model.fit(x_train_bn3,y_train3,
                   validation_data=(x_valid_bn3,y_valid3),
                   epochs=100,batch_size=128,verbose=2,
                   callbacks=[checkpointer,lr_reduction,estopping]);

history_plot(history)
resnet50_model.load_weights(fw)
resnet50_scores=resnet50_model.evaluate(x_test_bn3,y_test3)
print("Accuracy: %.2f%%"%(resnet50_scores[1]*100))
resnet50_scores