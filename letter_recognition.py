# -*- coding: utf-8 -*-
"""letter_recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z9Fz0OOi6bpWvH-H2OhExC9CkGPWBYZz

# 📑 &nbsp; Deep Learning. P2: Multi-Label Classification. Letter Recognition
<a href="https://olgabelitskaya.github.io/README.html">&#x1F300; &nbsp; Home Page &nbsp; &nbsp; &nbsp;</a>
<a href="https://www.instagram.com/olga.belitskaya/">&#x1F300; &nbsp; Instagram Posts &nbsp; &nbsp; &nbsp;</a>
<a href="https://www.pinterest.ru/olga_belitskaya/code-style/">&#x1F300; &nbsp; Pinterest Posts</a><br/>
For this project, I have created the dataset of <br/>
14190 color images (32x32x3) with 33 symbols of handwritten Russian letters.<br/>
There are four types of letter backgrounds here.<br/>
They are labeled in this dataset as well.<br/>
"""

from IPython import display
display.HTML("""<style>
@import url('https://fonts.googleapis.com/css?family=Akronim|Ruthie');
</style><div id='im'>
<table style='width:30%; background-color:ghostwhite; 
      font-family:Ruthie; font-size:200%;'>
<tr style='font-family:Akronim;'><th><center>Background</center></th>
<th><center>Image</center></th></tr>
<tr><td><center>0</center></td><td><center>
<img width='50' height='50' 
src='https://olgabelitskaya.github.io/images/03_16.jpeg' alt='bg0'>
</center></td></tr><tr><td><center>1</center></td><td><center>
<img width='50' height='50' 
src='https://olgabelitskaya.github.io/images/08_50.jpeg' alt='bg1'>
</center></td></tr><tr><td><center>2</center></td><td><center>
<img width='50' height='50' 
src='https://olgabelitskaya.github.io/images/11_216.jpeg' alt='bg2'>
</center></td></tr><tr><td><center>3</center></td><td><center>
<img width='50' height='50' 
src='https://olgabelitskaya.github.io/images/20_415.jpeg' alt='bg3'>
</center></td></tr></table></div>""")

"""## ✒️ &nbsp; Step 0. Importing Libraries and Defining Helpful Functions"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import h5py,urllib,zipfile
import pandas as pd,numpy as np,pylab as pl
import keras as ks,tensorflow as tf
import warnings; warnings.filterwarnings('ignore')
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,load_model,Model
from keras.layers import Input,Activation,Dense,LSTM
from keras.layers import Flatten,Dropout,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D,GlobalMaxPooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers.advanced_activations import PReLU,LeakyReLU
i0,i1,i2,i3,i4,i5=int(0),int(1),int(2),int(3),int(4),int(5)
np.set_printoptions(precision=6)
from keras import __version__
print('keras version:', __version__)
print('tensorflow version:', tf.__version__)

#from keras.preprocessing import image as keras_image
#from keras import backend,losses
#from keras.engine.topology import Layer
#from keras.optimizers import Adam,Nadam
#from keras.engine import InputLayer
#from keras.layers import Dense, LSTM, Activation, LeakyReLU
#from keras.layers import Conv2D, MaxPool2D, MaxPooling2D, GlobalMaxPooling2D
#from keras.layers import UpSampling2D, Conv2DTranspose
#from keras.layers.core import RepeatVector, Permute
#from keras.layers import Reshape, concatenate, merge

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
def resh(x):
    y=[resize(el,(int(24),int(24),int(3)),
              anti_aliasing=True) for el in x]
    return np.array(y)
def resh2(x): 
    return x.reshape(-int(1),int(32),int(32),int(1))

def history_plot(fit_history):
    pl.figure(figsize=(12,10))
    pl.subplot(211)
    pl.plot(fit_history.history['loss'],
            color='slategray',label='train')
    pl.plot(fit_history.history['val_loss'],
            color='#348ABD',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid()
    pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history['accuracy'],
            color='slategray',label='train')
    pl.plot(fit_history.history['val_accuracy'],
            color='#348ABD',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid()
    pl.title('Accuracy'); pl.show()

"""## ✒️ &nbsp;Step 1. Loading and Preprocessing the Data"""

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
backgrounds=np.array(f[keys[0]])
images=np.array(f[keys[1]])/255
labels=np.array(f[keys[2]])
pl.figure(figsize=(2,3)); il=10**4
pl.xticks([]); pl.yticks([])
pl.title('Label: %s \n'%letters[labels[il]-1]+\
         'Background: %s'%backgrounds[il],
         fontsize=18)
pl.imshow(images[il]); pl.show()

images.shape

gray_images=np.dot(images[...,:3],[.299,.587,.114])
pl.figure(figsize=(2,3))
pl.title('Label: %s \n'%letters[labels[il]-1]+\
         'Background: %s'%backgrounds[il],
         fontsize=18)
pl.imshow(gray_images[il],cmap=pl.cm.bone)
pl.xticks([]); pl.yticks([]); pl.show()

cbackgrounds,clabels=ohe(backgrounds),ohe(labels)
pd.DataFrame([labels[97:103],clabels[97:103]]).T

ctargets=\
np.concatenate((clabels,cbackgrounds),axis=1)
pd.DataFrame([clabels.shape,cbackgrounds.shape,
              ctargets.shape])

x_train1,x_valid1,x_test1,\
y_train1,y_valid1,y_test1=tts(images,clabels)
x_train2,x_valid2,x_test2,\
y_train2,y_valid2,y_test2=tts(gray_images,clabels)
x_train3,x_valid3,x_test3,\
y_train3,y_valid3,y_test3=tts(images,ctargets)
x_train4,x_valid4,x_test4,\
y_train4,y_valid4,y_test4=tts(gray_images,ctargets)
x_train2,x_valid2,x_test2=\
resh2(x_train2),resh2(x_valid2),resh2(x_test2)
x_train4,x_valid4,x_test4=\
resh2(x_train4),resh2(x_valid4),resh2(x_test4)
sh=[el.shape for el in \
[x_train1,y_train1,x_valid1,y_valid1,x_test1,y_test1,
 x_train2,y_train2,x_valid2,y_valid2,x_test2,y_test2,
 x_train3,y_train3,x_valid3,y_valid3,x_test3,y_test3,
 x_train4,y_train4,x_valid4,y_valid4,x_test4,y_test4]]
pd.DataFrame(sh)

fw='weights.letter.hdf5'
dr,fr,al=float(.2),float(.2),float(.02)
i10,i16,i32,i33=int(10),int(16),int(32),int(33)
i48,i64,i96=int(48),int(64),int(96)
i100,i128,i196,i200=int(100),int(128),int(196),int(200)
i256,i512,i1024=int(256),int(512),int(1024)
n1,n2=int(3000),int(500)

rx_train1,rx_valid1,rx_test1=\
resh(x_train1),resh(x_valid1),resh(x_test1)

"""## ✒️ &nbsp; Step 2. One-Label Classification Models
#### Color Images
"""

def model():
    model=Sequential()
    model.add(Dense(128,input_shape=(32*32*3,)))
    model.add(LeakyReLU(alpha=.2)) 
    model.add(BatchNormalization())
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=.2))
    model.add(BatchNormalization())
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=.2))
    model.add(BatchNormalization())
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=.2))   
    model.add(Dropout(.2))    
    model.add(Dense(33))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
model=model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.75)
estopping=EarlyStopping(monitor='val_loss',
                        patience=32,verbose=2)
history=model.fit(x_train1.reshape(-1,32*32*3),y_train1,epochs=200,batch_size=128,
                  verbose=2,validation_data=(x_valid1.reshape(-1,32*32*3),y_valid1),
                  callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test1.reshape(-1,32*32*3),y_test1)

"""
RNN
def model():
    model=Sequential()
    
    model.add(BatchNormalization())
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=.2))   
    model.add(Dropout(.2))    
    model.add(Dense(33))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
model=model()
"""

def model():
    model=Sequential()
    model.add(Conv2D(i16,(i3,i3),padding='same', 
                     input_shape=rx_train1.shape[i1:]))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))
    model.add(Conv2D(i48,(i3,i3)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))    
    model.add(GlobalMaxPooling2D())     
    model.add(Dense(i512,activation='relu'))
    model.add(Dropout(dr))    
    model.add(Dense(i33,activation='softmax'))   
    model.compile(loss='categorical_crossentropy', 
                  optimizer='nadam',metrics=['accuracy'])   
    return model
model=model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',
                        patience=i32,verbose=i2)
history=model.fit(rx_train1,y_train1,epochs=i200,batch_size=i128,
                  verbose=i2,validation_data=(rx_valid1,y_valid1),
                  callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
model.load_weights(fw)
model.evaluate(rx_test1,y_test1)

def model():
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same',
                     input_shape=x_train1.shape[i1:]))
    model.add(LeakyReLU(alpha=al))   
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))
    model.add(Conv2D(i196,(i5,i5)))
    model.add(LeakyReLU(alpha=al))  
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))
    model.add(GlobalMaxPooling2D())  
    model.add(Dense(i1024))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(2*dr))     
    model.add(Dense(i33,activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])   
    return model
model=model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i32,verbose=i2)
history=model.fit(x_train1,y_train1,epochs=i200,batch_size=i64,
                  verbose=i2,validation_data=(x_valid1,y_valid1),
                  callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test1,y_test1)

steps,epochs=int(1000),int(10)
zr,sr,rr=float(.2),float(.2),int(2)
igen=ImageDataGenerator(zoom_range=zr,shear_range=sr,rotation_range=rr)
generator=model.fit_generator(igen.flow(x_train1,y_train1,batch_size=i64),
                              steps_per_epoch=steps,epochs=epochs,verbose=i2,
                              validation_data=(x_valid1,y_valid1), 
                              callbacks=[checkpointer,lr_reduction])

history_plot(generator)
model.load_weights(fw)
model.evaluate(x_test1,y_test1)

py_test1=model.predict_classes(x_test1)
fig=pl.figure(figsize=(12,12))
for i,idx in enumerate(np.random.choice(x_test1.shape[0],
                                        size=16,replace=False)):
    ax=fig.add_subplot(4,4,i+1,xticks=[],yticks=[])
    ax.imshow(np.squeeze(x_test1[idx]))
    pred_idx=py_test1[idx]
    true_idx=np.argmax(y_test1[idx])
    ax.set_title("{} ({})".format(letters[pred_idx],letters[true_idx]),
                 color=("darkblue" if pred_idx==true_idx else "darkred"))

cy_train1=np.array([np.argmax(y) for y in y_train1])
cy_test1=np.array([np.argmax(y) for y in y_test1])
cy_valid1=np.array([np.argmax(y) for y in y_valid1])

# clf1=GradientBoostingClassifier()\
# .fit(x_train1.reshape(-1,32*32*3),cy_train1)
# [clf1.score(x_test1.reshape(-1,32*32*3),cy_test1),
#  clf1.score(x_valid1.reshape(-1,32*32*3),cy_valid1)]

clf2=RandomForestClassifier()\
.fit(x_train1.reshape(-1,32*32*3),cy_train1)
[clf2.score(x_test1.reshape(-1,32*32*3),cy_test1),
 clf2.score(x_valid1.reshape(-1,32*32*3),cy_valid1)]

"""#### Grayscale Images"""

def gray_model():
    model=Sequential()    
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train2.shape[i1:]))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))
    model.add(Conv2D(i256, (i5,i5)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))   
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i1024,activation='relu'))
    model.add(Dropout(dr))     
    model.add(Dense(i256,activation='relu'))
    model.add(Dropout(dr))    
    model.add(Dense(i33,activation='softmax'))   
    model.compile(loss='categorical_crossentropy', 
                  optimizer='rmsprop',metrics=['accuracy'])
    return model
gray_model=gray_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i32,
                        verbose=i2)
history=gray_model.fit(x_train2,y_train2,epochs=i200,
                       batch_size=i64,verbose=i2,
                       validation_data=(x_valid2,y_valid2),
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test2,y_test2)

def gray_model():
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same',
                     input_shape=x_train2.shape[i1:]))
    model.add(LeakyReLU(alpha=al))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))
    model.add(Conv2D(i128,(i5,i5)))
    model.add(LeakyReLU(alpha=al))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr))   
    model.add(GlobalMaxPooling2D())     
    model.add(Dense(i1024))
    model.add(LeakyReLU(alpha=al)) 
    model.add(Dropout(dr))   
    model.add(Dense(i128))
    model.add(LeakyReLU(alpha=al)) 
    model.add(Dropout(dr))    
    model.add(Dense(i33))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])  
    return model
gray_model=gray_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i32,verbose=i2)
history=gray_model.fit(x_train2,y_train2,epochs=i200,
                       batch_size=i64,verbose=i2,
                       validation_data=(x_valid2,y_valid2),
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test2,y_test2)

steps,epochs=int(1000),int(10)
zr,sr,rr=float(.2),float(.2),int(20)
igen=ImageDataGenerator(zoom_range=zr,shear_range=sr,rotation_range=rr)
generator=\
gray_model.fit_generator(igen.flow(x_train2,y_train2,batch_size=i64),
                         steps_per_epoch=steps,epochs=epochs,verbose=i2,
                         validation_data=(x_valid2,y_valid2), 
                         callbacks=[checkpointer,lr_reduction])

history_plot(generator)
gray_model.load_weights(fw)
gray_model.evaluate(x_test2,y_test2)

cy_train2=np.array([np.argmax(y) for y in y_train2])
cy_test2=np.array([np.argmax(y) for y in y_test2])
cy_valid2=np.array([np.argmax(y) for y in y_valid2])

# clf1=GradientBoostingClassifier()\
# .fit(x_train2.reshape(-1,32*32),cy_train2)
# [clf1.score(x_test2.reshape(-1,32*32),cy_test2),
# clf1.score(x_valid2.reshape(-1,32*32),cy_valid2)]

clf2=RandomForestClassifier()\
.fit(x_train2.reshape(-1,32*32),cy_train2)
[clf2.score(x_test2.reshape(-1,32*32),cy_test2),
 clf2.score(x_valid2.reshape(-1,32*32),cy_valid2)]

"""## ✒️ &nbsp; Step 3. Multi-Label Classification Models
#### Color Images
"""

def multi_model():    
    model_input=Input(shape=(i32,i32,i3))
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i3,i3),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr)(x)   
    x=Conv2D(i128,(i3,i3),padding='same')(x)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr)(x)             
    x=GlobalMaxPooling2D()(x)   
    x=Dense(i1024)(x)
    x=LeakyReLU(alpha=al)(x)
    x=Dropout(dr)(x)   
    x=Dense(i128)(x)  
    x=LeakyReLU(alpha=al)(x)
    x=Dropout(dr)(x)    
    y1=Dense(i33,activation='softmax')(x)
    y2=Dense(i4,activation='softmax')(x)    
    model=Model(inputs=model_input,outputs=[y1,y2])
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])
    return model
multi_model=multi_model()
multi_model.summary()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=multi_model.fit(x_train3,[y_train3[:,:i33],y_train3[:,i33:]],
                        epochs=i100,batch_size=i64,verbose=i2,
                        validation_data=(x_valid3,
                                         [y_valid3[:,:i33],
                                          y_valid3[:,i33:]]),
                        callbacks=[checkpointer,lr_reduction])

multi_model.evaluate(x_test3,\
[y_test3[:,:i33],y_test3[:,i33:]])

"""#### Grayscale Images"""

def gray_multi_model():    
    model_input=Input(shape=(i32,i32,i1))
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i5,i5),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr)(x)   
    x=Conv2D(i256,(i5,i5),padding='same')(x) 
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr)(x)             
    x=GlobalMaxPooling2D()(x)    
    x=Dense(i1024)(x) 
    x=LeakyReLU(alpha=al)(x)
    x=Dropout(dr)(x)   
    x=Dense(i256)(x) 
    x=LeakyReLU(alpha=al)(x)
    x=Dropout(dr)(x)   
    y1=Dense(i33,activation='softmax')(x)
    y2=Dense(i4,activation='softmax')(x)      
    model=Model(inputs=model_input,outputs=[y1,y2])
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])      
    return model
gray_multi_model=gray_multi_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,
                             save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
history=gray_multi_model.fit(x_train4,[y_train4[:,:i33],y_train4[:,i33:]], 
                             validation_data=(x_valid4,
                                              [y_valid4[:,:i33],
                                               y_valid4[:,i33:]],), 
                             epochs=i200,batch_size=i128,verbose=i2, 
                             callbacks=[checkpointer,lr_reduction])

gray_multi_model.evaluate(x_test4,\
[y_test4[:,:i33],y_test4[:,i33:]])

"""## ✒️ &nbsp; Step 4. Keras Applications"""

from keras.applications.vgg16 import VGG16,preprocess_input as prei16
from skimage.transform import resize
def resh(x,n):
    y=[resize(el,(int(n),int(n),int(3)),
              anti_aliasing=True) for el in x]
    return np.array(y)

img=resh(images[100].reshape(1,32,32,3),128).reshape(128,128,3)
pl.figure(figsize=(3,4)); il=10**4
pl.xticks([]); pl.yticks([])
pl.title('Label: %s \n'%letters[labels[il]-1]+\
         'Background: %s'%backgrounds[il],
         fontsize=18)
pl.imshow(img); pl.show()

#vx_train1,vx_valid1,vx_test1=\
#resh(x_train1,128),resh(x_valid1,128),resh(x_test1,128)
#vx_train1,vx_valid1,vx_test1=\
#prei16(x_train1),prei16(x_valid1),prei16(x_test1)
vgg16bmodel=VGG16(weights='imagenet',include_top=False)
pvx_train1=vgg16bmodel.predict(x_train1)
pvx_valid1=vgg16bmodel.predict(x_valid1)
pvx_test1=vgg16bmodel.predict(x_test1)
pvx_train1=pvx_train1.reshape(-1,1,1,pvx_train1.shape[3])
pvx_valid1=pvx_valid1.reshape(-1,1,1,pvx_valid1.shape[3])
pvx_test1=pvx_test1.reshape(-1,1,1,pvx_test1.shape[3])

#np.save('vx_train1.npy',vx_train1)
#np.save('vx_valid1.npy',vx_valid1)
#np.save('vx_test1.npy',vx_test1)
#vx_train1=np.load('vx_train_1.npy')
#vx_valid1=np.load('vx_valid1.npy')
#vx_test1=np.load('vx_test1.npy')

sh=pvx_train1.shape[1:]
def vgg16model():
    model=Sequential()  
    model.add(GlobalAveragePooling2D(input_shape=sh))   
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))        
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))  
#    model.add(Dense(128))
#    model.add(LeakyReLU(alpha=.02))
#    model.add(Dropout(.25)) 
    model.add(Dense(33,activation='softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])
    return model
vgg16model=vgg16model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.8)
estopping=EarlyStopping(monitor='val_loss',patience=30,verbose=2)
history=vgg16model.fit(pvx_train1,y_train1, 
                       validation_data=(pvx_valid1,y_valid1), 
                       epochs=800,batch_size=128,verbose=2, 
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
vgg16model.load_weights(fw)
vgg16model.evaluate(pvx_test1,y_test1)

from keras.applications.vgg19 import VGG19,preprocess_input as prei19
#vx_train1,vx_valid1,vx_test1=\
#resh(x_train1),resh(x_valid1),resh(x_test1)
#vx_train1,vx_valid1,vx_test1=\
#prei19(x_train1),prei19(x_valid1),prei19(x_test1)
vgg19bmodel=VGG19(weights='imagenet',include_top=False)
pvx_train1=vgg19bmodel.predict(x_train1)
pvx_valid1=vgg19bmodel.predict(x_valid1)
pvx_test1=vgg19bmodel.predict(x_test1)
pvx_train1=pvx_train1.reshape(-1,1,1,pvx_train1.shape[3])
pvx_valid1=pvx_valid1.reshape(-1,1,1,pvx_valid1.shape[3])
pvx_test1=pvx_test1.reshape(-1,1,1,pvx_test1.shape[3])

sh=pvx_train1.shape[1:]
def vgg19model():
    model=Sequential()  
    model.add(GlobalAveragePooling2D(input_shape=sh))   
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))        
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))  
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25)) 
    model.add(Dense(33,activation='softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])
    return model
vgg19model=vgg19model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.8)
estopping=EarlyStopping(monitor='val_loss',patience=30,verbose=2)
history=vgg19model.fit(pvx_train1,y_train1, 
                       validation_data=(pvx_valid1,y_valid1), 
                       epochs=800,batch_size=128,verbose=2, 
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
vgg19model.load_weights(fw)
vgg19model.evaluate(pvx_test1,y_test1)

from keras.applications.resnet_v2 import ResNet152V2,preprocess_input as preiRN
#vx_train1,vx_valid1,vx_test1=\
#preiRN(x_train1),preiRN(x_valid1),preiRN(x_test1)
RNbmodel=ResNet152V2(weights='imagenet',include_top=False)
pvx_train1=RNbmodel.predict(x_train1)
pvx_valid1=RNbmodel.predict(x_valid1)
pvx_test1=RNbmodel.predict(x_test1)
pvx_train1=pvx_train1.reshape(-1,1,1,pvx_train1.shape[3])
pvx_valid1=pvx_valid1.reshape(-1,1,1,pvx_valid1.shape[3])
pvx_test1=pvx_test1.reshape(-1,1,1,pvx_test1.shape[3])

sh=pvx_train1.shape[1:]
def RNmodel():
    model=Sequential()  
    model.add(GlobalAveragePooling2D(input_shape=sh))   
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25)) 
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))        
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))   
    model.add(Dense(33,activation='softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])
    return model
RNmodel=RNmodel()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.75)
estopping=EarlyStopping(monitor='val_loss',patience=30,verbose=2)
history=RNmodel.fit(pvx_train1,y_train1, 
                    validation_data=(pvx_valid1,y_valid1), 
                    epochs=800,batch_size=128,verbose=2, 
                    callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
RNmodel.load_weights(fw)
RNmodel.evaluate(pvx_test1,y_test1)

from keras.applications.nasnet import NASNetLarge
NNLbmodel=NASNetLarge(weights='imagenet',include_top=False)
n1,n2=1800,180
def resh(x):
    y=[resize(el,(int(331),int(331),int(3)),
              anti_aliasing=True) for el in x]
    return np.array(y)
pvx_train1,pvx_valid1,pvx_test1=\
resh(x_train1[:n1]),resh(x_valid1[:n2]),resh(x_test1[:n2])
pvx_train1=NNLbmodel.predict(pvx_train1)
pvx_valid1=NNLbmodel.predict(pvx_valid1)
pvx_test1=NNLbmodel.predict(pvx_test1)

pvx_train1.shape

sh=pvx_train1.shape[1:]
def NNLmodel():
    model=Sequential()  
    model.add(GlobalAveragePooling2D(input_shape=sh))   
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25)) 
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))        
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.25))   
    model.add(Dense(33,activation='softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])
    return model
NNLmodel=NNLmodel()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.8)
estopping=EarlyStopping(monitor='val_loss',patience=30,verbose=2)
history=NNLmodel.fit(pvx_train1,y_train1[:n1], 
                     validation_data=(pvx_valid1,y_valid1[:n2]), 
                     epochs=800,batch_size=128,verbose=2, 
                     callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
NNLmodel.load_weights(fw)
NNLmodel.evaluate(pvx_test1,y_test1[:n2])

del pvx_train1,pvx_valid1,pvx_test1