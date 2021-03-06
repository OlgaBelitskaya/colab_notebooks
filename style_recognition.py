# -*- coding: utf-8 -*-
"""style_recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r5yRD-3tQwN6lSql_VRoVuwQ8DaY5zUt

# 📑 &nbsp; Deep Learning. P4: Style Recognition
<a href="https://olgabelitskaya.github.io/README.html">&#x1F300; &nbsp; Home Page &nbsp; &nbsp; &nbsp;</a> 
<a href="https://www.instagram.com/olga.belitskaya/">&#x1F300; &nbsp; Instagram Posts &nbsp; &nbsp; &nbsp;</a>
<a href="https://www.pinterest.ru/olga_belitskaya/code-style/">&#x1F300; &nbsp; Pinterest Posts</a><br/>
For this project, I have made the database of photos sorted by products and brands.<br/>
The dataset consists of 2184 color images (150x150x3) with 7 brands and 10 products.<br/>
Original photo files are in the .png format and the labels are integers and string values.<br/>
"""

import urllib,os; from IPython import display
fpath='https://olgabelitskaya.github.io/images/'
lf=['0_0_026.jpeg','1_3_003.jpeg','2_2_039.jpeg',
    '3_5_012.jpeg','4_1_019.jpeg','5_9_005.jpeg','6_8_004.jpeg']
display.HTML("""
<style>
@import url('https://fonts.googleapis.com/css?family=Akronim|Monsieur La Doulaise');
</style>
<table style='width:42%; background-color:silver; color:#FF355E;
              font-family:Monsieur La Doulaise; font-size:250%;'>
<tr style='font-family:Akronim; font-size:80%;'><th><center>Brand</center></th>
<th><center>Image</center></th></tr>
<tr><td><center>Christian Louboutin</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/0_0_026.jpeg' alt='brand0'>
</center></td></tr>
<tr><td><center>Chanel</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/1_3_003.jpeg' alt='brand1'>
</center></td></tr>
<tr><td><center>Dolce & Gabbana</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/2_2_039.jpeg' alt='brand2'>
</center></td></tr>
<tr><td><center>Gucci</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/3_5_012.jpeg' alt='brand3'>
</center></td></tr>
<tr><td><center>Christian Dior</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/4_1_019.jpeg' alt='brand4'>
</center></td></tr>
<tr><td><center>Versace</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/5_9_005.jpeg' alt='brand5'>
</center></td></tr>
<tr><td><center>Yves Saint Laurent</center></td><td><center>
<img width='70' height='70' 
src='https://olgabelitskaya.github.io/images/6_8_004.jpeg' alt='brand6'>
</center></td></tr>
</table>""")

"""## ✒️&nbsp;Step 0. Importing Libraries and Defining Helpful Functions"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import warnings; warnings.filterwarnings('ignore')
import h5py,urllib,zipfile
import pandas as pd,numpy as np,pylab as pl
import seaborn as sn,keras as ks,tensorflow as tf
from skimage.transform import resize
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

fw='weights.style.hdf5'
dr2,dr25,dr3,dr5,dr6=\
float(.2),float(.25),float(.3),float(.5),float(.6)
fr,al=float(.5),float(.02)
i0,i1,i2,i3,i4,i5,i7,i8=\
int(0),int(1),int(2),int(3),int(4),int(5),int(7),int(8)
i10,i16,i32,i48,i64,i96=\
int(10),int(16),int(32),int(48),int(64),int(96)
i100,i128,i150,i196,i256=\
int(100),int(128),int(150),int(196),int(256)
i512,i1024=int(512),int(1024)

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
    y=[resize(el,(int(50),int(50),int(3)),
              anti_aliasing=True) for el in x]
    return np.array(y)
def gresh(x): 
    y=np.array([resize(el,(int(125),int(125),int(1)),
                       anti_aliasing=True) for el in x])
    return y.reshape(-int(1),int(125),int(125),int(1))

def history_plot(fit_history):
    pl.figure(figsize=(12,10)); pl.subplot(211)
    keys=list(fit_history.history.keys())[0:4]
    pl.plot(fit_history.history[keys[0]],
            color='slategray',label='train')
    pl.plot(fit_history.history[keys[2]],
            color='#348ABD',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid()
    pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[1]],
            color='slategray',label='train')
    pl.plot(fit_history.history[keys[3]],
            color='#348ABD',label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid()
    pl.title('Accuracy'); pl.show()
def history_plot2(fit_history):
    keys=list(fit_history.history.keys())[6:]
    pl.figure(figsize=(12,10)); pl.subplot(211)
    pl.plot(fit_history.history[keys[0]],
            color='slategray',label='valid 1')
    pl.plot(fit_history.history[keys[1]],
            color='#37c9e1',label='valid 2')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid(); pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[2]],
            color='slategray',label='valid 1')
    pl.plot(fit_history.history[keys[3]],
            color='#37c9e1',label='valid 2')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid(); pl.title('Accuracy'); pl.show()

"""## ✒️&nbsp;Step 1. Loading and Preprocessing the Data"""

fpath='https://olgabelitskaya.github.io/'
zf='StyleColorImages.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb')
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys())
bnames=['Christian Louboutin','Chanel','Dolce & Gabbana','Gucci',
        'Christian Dior','Versace','Yves Saint Laurent']
pnames=['shoes','lipstick','handbag','nail polish','necklace',
        'watches','ring','bracelet','boots','earrings']
fpath2='https://raw.githubusercontent.com/OlgaBelitskaya/'+\
       'deep_learning_projects/master/DL_PP4/'
styles=pd.read_csv(fpath2+'data/style.csv')
styles.tail()

pl.figure(figsize=(12,6))
sn.countplot(x='product_name',data=styles,
             facecolor='none',linewidth=3,linestyle='-.',
             edgecolor=sn.color_palette('hsv',10))
pl.title('Product Distribution',fontsize=20)
pl.show()

pl.figure(figsize=(12,10))
sn.countplot(y="product_name",hue="brand_name", 
             data=styles,palette='hsv_r',alpha=.5)
ti='Product Distribution Grouped by Brands'
pl.title(ti,fontsize=20)
pl.legend(loc=4); pl.show()

brands=np.array(f[keys[0]])
images=np.array(f[keys[1]])/255
products=np.array(f[keys[2]])
print('Product: ',styles['product_name'][i100])
print('Brand: ',styles['brand_name'][i100])
pl.figure(figsize=(i5,i5)); pl.imshow(images[i100])
pl.show()

gray_images=np.dot(images[...,:3],[.299,.587,.114])
print('Product: ',styles['product_name'][i100])
print('Brand: ',styles['brand_name'][i100])
pl.figure(figsize=(i5,i5))
pl.imshow(gray_images[i100],cmap=pl.cm.bone); pl.show()
gray_images=gray_images.reshape(-1,150,150,1)

cbrands,cproducts=ohe(brands),ohe(products)
ctargets=np.concatenate((cbrands,cproducts),axis=1)
simages=resh(images); sgray_images=gresh(gray_images)
pd.DataFrame([simages.shape,sgray_images.shape,
              cbrands.shape,cproducts.shape,
              ctargets.shape])

# Color Images / Brand 
x_train1,x_valid1,x_test1,\
y_train1,y_valid1,y_test1=tts(images,cbrands)
# Grayscaled Images / Brand 
x_train2,x_valid2,x_test2,\
y_train2,y_valid2,y_test2=tts(gray_images,cbrands)
# Color Images / Product 
x_train3,x_valid3,x_test3,\
y_train3,y_valid3,y_test3=tts(images,cproducts)
# Grayscaled Images / Product 
x_train4,x_valid4,x_test4,\
y_train4,y_valid4,y_test4=tts(gray_images,cproducts)
# Color Images / Multi-Label Target
x_train5,x_valid5,x_test5,\
y_train5,y_valid5,y_test5=tts(images,ctargets)
# Grayscaled Images / Multi-Label Target 
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

y_train5_list=[y_train5[:,:i7],y_train5[:,i7:]]
y_test5_list=[y_test5[:,:i7],y_test5[:,i7:]]
y_valid5_list=[y_valid5[:,:i7],y_valid5[:,i7:]]
y_train6_list=[y_train6[:,:i7],y_train6[:,i7:]]
y_test6_list=[y_test6[:,:i7],y_test6[:,i7:]]
y_valid6_list=[y_valid6[:,:i7],y_valid6[:,i7:]]

"""## ✒️&nbsp;Step 2. One-Label Classification Models"""

# Color Images / Brands
def model():
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train1.shape[i1:]))
    model.add(LeakyReLU(alpha=al))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr2))
    model.add(Conv2D(i196,(i5,i5)))
    model.add(LeakyReLU(alpha=al))   
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr2))   
    model.add(GlobalMaxPooling2D())     
    model.add(Dense(i512))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr5))    
    model.add(Dense(i7))
    model.add(Activation('softmax'))   
    model.compile(loss='categorical_crossentropy', 
                  optimizer='nadam', metrics=['accuracy'])   
    return model
model=model()
model.summary()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=model.fit(x_train1,y_train1,epochs=i128,batch_size=i128,verbose=i2,
                  validation_data=(x_valid1,y_valid1),
                  callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test1,y_test1)

# Color Images / Products
def model():
    model=Sequential()
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train3.shape[i1:]))
    model.add(LeakyReLU(alpha=al))   
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i196,(i5,i5)))
    model.add(LeakyReLU(alpha=al))   
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))  
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i512))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr5))     
    model.add(Dense(i10))
    model.add(Activation('softmax')) 
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])   
    return model
model=model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=model.fit(x_train3,y_train3,epochs=i128,batch_size=i128,verbose=i2,
                  validation_data=(x_valid3,y_valid3),
                  callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
model.load_weights(fw)
model.evaluate(x_test3,y_test3)

# Grayscaled Images / Brands 
def gray_model():
    model=Sequential()   
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train2.shape[i1:]))
    model.add(LeakyReLU(alpha=al))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i196,(i5,i5)))
    model.add(LeakyReLU(alpha=al))   
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))  
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i1024))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr25))     
    model.add(Dense(i128))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr25))    
    model.add(Dense(i7))
    model.add(Activation('softmax'))   
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])
    return model
gray_model=gray_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=gray_model.fit(x_train2,y_train2,epochs=i128,batch_size=i128,
                       verbose=i2,validation_data=(x_valid2,y_valid2),
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test2,y_test2)

# Grayscaled Images / Products
def gray_model():
    model=Sequential()   
    model.add(Conv2D(i32,(i5,i5),padding='same', 
                     input_shape=x_train4.shape[i1:]))
    model.add(LeakyReLU(alpha=al)) 
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))
    model.add(Conv2D(i128,(i5,i5)))
    model.add(LeakyReLU(alpha=al))    
    model.add(MaxPooling2D(pool_size=(i2,i2)))
    model.add(Dropout(dr25))  
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(i1024))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr25))    
    model.add(Dense(i128))
    model.add(LeakyReLU(alpha=al))
    model.add(Dropout(dr25))    
    model.add(Dense(i10))
    model.add(Activation('softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])
    return model
gray_model=gray_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=gray_model.fit(x_train4,y_train4,epochs=i128,batch_size=i128,verbose=i2,
                       validation_data=(x_valid4,y_valid4),
                       callbacks=[checkpointer,lr_reduction,estopping])

history_plot(history)
gray_model.load_weights(fw)
gray_model.evaluate(x_test4,y_test4)

"""## ✒️&nbsp;Step 3. Multi-Label Classification Models"""

# Color Images
def mmodel():    
    model_input=Input(shape=(i150,i150,i3))
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i5,i5),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)   
    x=Conv2D(i196,(i5,i5),padding='same')(x)       
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)              
    x=GlobalMaxPooling2D()(x)   
    x=Dense(i512)(x)
    x=LeakyReLU(alpha=al)(x)    
    x=Dropout(dr25)(x)    
    y1=Dense(i7,activation='softmax')(x)
    y2=Dense(i10,activation='softmax')(x)   
    model=Model(inputs=model_input,outputs=[y1, y2])    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
mmodel=mmodel()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=mmodel.fit(x_train5,y_train5_list, 
                   validation_data=(x_valid5,y_valid5_list), 
                   epochs=i128,batch_size=i128,verbose=i2, 
                   callbacks=[checkpointer,lr_reduction,estopping])

history_plot2(history)
mmodel.load_weights(fw)
scores=mmodel.evaluate(x_test5,y_test5_list)
print("Scores: \n",(scores))
print("The Brand Label. Accuracy: %.2f%%"%(scores[i3]*i100))
print("The Product Label. Accuracy: %.2f%%"%(scores[i4]*i100))

# Grayscaled Images
def gray_mmodel():    
    model_input=Input(shape=(i150,i150,i1))
    x=BatchNormalization()(model_input)
    x=Conv2D(i32,(i5,i5),padding='same')(model_input)
    x=LeakyReLU(alpha=al)(x)
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)    
    x=Conv2D(i256,(i5,i5),padding='same')(x)
    x=LeakyReLU(alpha=al)(x)       
    x=MaxPooling2D(pool_size=(i2,i2))(x)    
    x=Dropout(dr25)(x)             
    x=GlobalMaxPooling2D()(x)    
    x=Dense(i1024)(x)
    x=LeakyReLU(alpha=al)(x)   
    x=Dropout(dr25)(x)   
    x=Dense(i256)(x)
    x=LeakyReLU(alpha=al)(x)    
    x=Dropout(dr25)(x)    
    y1=Dense(i7,activation='softmax')(x)
    y2=Dense(i10,activation='softmax')(x)       
    model=Model(inputs=model_input,outputs=[y1,y2])
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',metrics=['accuracy'])   
    return model
gray_mmodel=gray_mmodel()

checkpointer=ModelCheckpoint(filepath=fw,verbose=i2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i5,
                               verbose=i2,factor=fr)
estopping=EarlyStopping(monitor='val_loss',patience=i16,verbose=i2)
history=gray_mmodel.fit(x_train6,y_train6_list, 
                        validation_data=(x_valid6,y_valid6_list), 
                        epochs=i128,batch_size=i128,verbose=i2, 
                        callbacks=[checkpointer,lr_reduction,estopping])

history_plot2(history)
gray_mmodel.load_weights(fw)
scores=gray_mmodel.evaluate(x_test6,y_test6_list)
print("Scores: \n",(scores))
print("The Brand Label. Accuracy: %.2f%%"%(scores[i3]*i100))
print("The Product Label. Accuracy: %.2f%%"%(scores[i4]*i100))

"""## ✒️ &nbsp; Step 4. Keras Applications"""

from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input as resnet50pi
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as inceptionv3pi
from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input as xceptionpi
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 \
import preprocess_input as inceptionresnetv2pi
def resh(x):
    y=[resize(el,(224,224,3),
              anti_aliasing=True) for el in x]
    return np.array(y).astype('float32')

resize_x_train1=resh(x_train1)
resize_x_valid1=resh(x_valid1)
resize_x_test1=resh(x_test1)
resnet50_base_model=ResNet50(weights='imagenet',include_top=False)
pvx_train1=resnet50_base_model.predict(resize_x_train1)
pvx_valid1=resnet50_base_model.predict(resize_x_valid1)
pvx_test1=resnet50_base_model.predict(resize_x_test1)

sh=pvx_train1.shape[1:]
def resnet50_model():
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
    model.add(Dense(7,activation='softmax'))    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
resnet50_model=resnet50_model()

checkpointer=ModelCheckpoint(filepath=fw,verbose=2,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=5,
                               verbose=2,factor=.75)
estopping=EarlyStopping(monitor='val_loss',patience=25,verbose=2)
history=\
resnet50_model.fit(pvx_train1,y_train1,
                   validation_data=(pvx_valid1,y_valid1),
                   epochs=200,batch_size=128,verbose=2,
                   callbacks=[checkpointer,lr_reduction,estopping]);

history_plot(history)
resnet50_model.load_weights(fw)
resnet50_scores=resnet50_model.evaluate(pvx_test1,y_test1)
print("Accuracy: %.2f%%"%(resnet50_scores[1]*100))
resnet50_scores