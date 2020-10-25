# -*- coding: utf-8 -*-
"""tensorflow_cookbook2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RoHGrTJz4KOiHN1W-UCGzzY5abV3pXLg
"""

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import display,HTML
def dhtml(str):
    display(HTML("""<style>
    @import url('https://fonts.googleapis.com/css?family=Ewert&effect=3d');      
    </style><h1 class='font-effect-3d' style='font-family:Ewert; color:#ff355e'>
#     %s</h1>"""%str))

dhtml('Code Modules & Helpful Functions')

!pip install --upgrade neural_structured_learning --user

path='/root/.local/lib/python3.6/site-packages'
import sys; sys.path.append(path)
import warnings; warnings.filterwarnings('ignore')
import h5py,urllib,zipfile
import pylab as pl,pandas as pd
import numpy as np,tensorflow as tf
import neural_structured_learning as nsl
from sklearn.model_selection import train_test_split

fpath='https://olgabelitskaya.github.io/'
def prepro(x_train,y_train,x_test,y_test,n_class):
    n=int(len(x_test)/2)    
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    cy_train=tf.keras.utils.to_categorical(y_train,n_class) 
    cy_valid=tf.keras.utils.to_categorical(y_valid,n_class)
    cy_test=tf.keras.utils.to_categorical(y_test,n_class)
    df=pd.DataFrame([[x_train.shape,x_valid.shape,x_test.shape],
                     [y_train.shape,y_valid.shape,y_test.shape],
                     [cy_train.shape,cy_valid.shape,cy_test.shape]],
                    columns=['train','valid','test'],
                    index=['images','labels','encoded labels'])
    display(df)
    return [[x_train,x_valid,x_test],
            [y_train,y_valid,y_test],
            [cy_train,cy_valid,cy_test]]

dhtml('Data Loading & Preprocessing')

(x_train1,y_train1),(x_test1,y_test1)=\
tf.keras.datasets.mnist.load_data()
[[x_train1,x_valid1,x_test1],
 [y_train1,y_valid1,y_test1],
 [cy_train1,cy_valid1,cy_test1]]=\
prepro(x_train1/255,y_train1.reshape(-1,1),
       x_test1/255,y_test1.reshape(-1,1),10)

(x_train2,y_train2),(x_test2,y_test2)=\
tf.keras.datasets.cifar10.load_data()
[[x_train2,x_valid2,x_test2],
 [y_train2,y_valid2,y_test2],
 [cy_train2,cy_valid2,cy_test2]]=\
prepro(x_train2/255,y_train2,x_test2/255,y_test2,10)

zf='LetterColorImages_123.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb'); 
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys()); keys
images=np.array(f[keys[1]])/255
labels=np.array(f[keys[2]]).astype('int').reshape(-1,1)-1
x_train3,x_test3,y_train3,y_test3=\
train_test_split(images,labels,test_size=.2,random_state=1)
del images,labels
[[x_train3,x_valid3,x_test3],
 [y_train3,y_valid3,y_test3],
 [cy_train3,cy_valid3,cy_test3]]=\
prepro(x_train3,y_train3,x_test3,y_test3,33)

zf='FlowerColorImages.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb'); 
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys())
images=np.array(f[keys[0]])/255
labels=np.array(f[keys[1]]).astype('int').reshape(-1,1)
x_train4,x_test4,y_train4,y_test4=\
train_test_split(images,labels,test_size=.2,random_state=1)
del images,labels
[[x_train4,x_valid4,x_test4],
 [y_train4,y_valid4,y_test4],
 [cy_train4,cy_valid4,cy_test4]]=\
prepro(x_train4,y_train4,x_test4,y_test4,10)

dhtml('Models with Adversarial Regularization')
dhtml('MLP Base')

batch_size=64; img_size=28; n_class=10; epochs=7
base_model=tf.keras.Sequential([
    tf.keras.Input((img_size,img_size),name='input'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128,activation=tf.nn.relu),
    tf.keras.layers.BatchNormalization(),    
    tf.keras.layers.Dense(256,activation=tf.nn.relu),
    tf.keras.layers.Dense(n_class,activation=tf.nn.softmax)
])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train1=tf.data.Dataset.from_tensor_slices(
    {'input':x_train1,'label':y_train1}).batch(batch_size)
valid1=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid1,'label':y_valid1}).batch(batch_size)
valid_steps=x_valid1.shape[0]//batch_size
adv_model.fit(train1,validation_data=valid1,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test1,'label':y_test1})

batch_size=64; img_size=32; n_class=10; epochs=10
base_model=tf.keras.models.Sequential([
        tf.keras.Input((img_size,img_size,3),name='input'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(256,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(512,activation='relu'),
        tf.keras.layers.BatchNormalization(),   
        tf.keras.layers.Dense(1024,activation='relu'),
        tf.keras.layers.Dense(10,activation='softmax')
    ])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train2=tf.data.Dataset.from_tensor_slices(
    {'input':x_train2,'label':y_train2}).batch(batch_size)
valid2=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid2,'label':y_valid2}).batch(batch_size)
valid_steps=x_valid2.shape[0]//batch_size
adv_model.fit(train2,validation_data=valid2,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test2,'label':y_test2})

batch_size=128; img_size=32; n_class=33; epochs=100
base_model=tf.keras.models.Sequential([
        tf.keras.Input((img_size,img_size,3),name='input'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(256,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(512,activation='relu'),
        tf.keras.layers.BatchNormalization(),   
        tf.keras.layers.Dense(1024,activation='relu'),
        tf.keras.layers.Dense(33,activation='softmax')
    ])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train3=tf.data.Dataset.from_tensor_slices(
    {'input':x_train3,'label':y_train3}).batch(batch_size)
valid3=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid3,'label':y_valid3}).batch(batch_size)
valid_steps=x_valid3.shape[0]//batch_size
adv_model.fit(train3,validation_data=valid3,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test3,'label':y_test3})

batch_size=16; img_size=128; n_class=10; epochs=50
base_model=tf.keras.models.Sequential([
        tf.keras.Input((img_size,img_size,3),name='input'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.BatchNormalization(),    
        tf.keras.layers.Dense(1024,activation='relu'),
        tf.keras.layers.BatchNormalization(),   
        tf.keras.layers.Dense(1024,activation='relu'),
        tf.keras.layers.Dense(10,activation='softmax')
    ])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train4=tf.data.Dataset.from_tensor_slices(
    {'input':x_train4,'label':y_train4}).batch(batch_size)
valid4=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid4,'label':y_valid4}).batch(batch_size)
valid_steps=x_valid4.shape[0]//batch_size
adv_model.fit(train4,validation_data=valid4,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test4,'label':y_test4})

dhtml('CNN Base')

batch_size=128; img_size=28; n_class=10; epochs=7
base_model=tf.keras.Sequential([
    tf.keras.Input((img_size,img_size,1),name='input'),
    tf.keras.layers.Conv2D(32,(5,5),padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Conv2D(196,(5,5)),
    tf.keras.layers.Activation('relu'),    
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.GlobalMaxPooling2D(),    
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Dense(128),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Dense(10,activation='softmax')    
])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train1=tf.data.Dataset.from_tensor_slices(
    {'input':x_train1.reshape(x_train1.shape[0],28,28,1),
     'label':y_train1}).batch(batch_size)
valid1=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid1.reshape(x_valid1.shape[0],28,28,1),
     'label':y_valid1}).batch(batch_size)
valid_steps=x_valid1.shape[0]//batch_size
adv_model.fit(train1,validation_data=valid1,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test1.reshape(x_test1.shape[0],28,28,1),
                    'label':y_test1})

batch_size=64; img_size=32; n_class=10; epochs=10
base_model=tf.keras.Sequential([
    tf.keras.Input((img_size,img_size,3),name='input'),
    tf.keras.layers.Conv2D(32,(5,5),padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Conv2D(96,(5,5)),
    tf.keras.layers.Activation('relu'),    
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.GlobalMaxPooling2D(),    
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Dense(10,activation='softmax')
])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train2=tf.data.Dataset.from_tensor_slices(
    {'input':x_train2,'label':y_train2}).batch(batch_size)
valid2=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid2,'label':y_valid2}).batch(batch_size)
valid_steps=x_valid2.shape[0]//batch_size
adv_model.fit(train2,validation_data=valid2,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test2,'label':y_test2})

batch_size=128; img_size=32; n_class=33; epochs=200
base_model=tf.keras.Sequential([
    tf.keras.Input((img_size,img_size,3),name='input'),
    tf.keras.layers.Conv2D(32,(5,5),padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Conv2D(196,(5,5)),
    tf.keras.layers.Activation('relu'),    
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.GlobalMaxPooling2D(),    
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Dense(33,activation='softmax')
])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train3=tf.data.Dataset.from_tensor_slices(
    {'input':x_train3,'label':y_train3}).batch(batch_size)
valid3=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid3,'label':y_valid3}).batch(batch_size)
valid_steps=x_valid3.shape[0]//batch_size
adv_model.fit(train3,validation_data=valid3,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test3,'label':y_test3})

batch_size=16; img_size=128; n_class=10; epochs=100
base_model=tf.keras.Sequential([
    tf.keras.Input((img_size,img_size,3),name='input'),
    tf.keras.layers.Conv2D(32,(5,5),padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Conv2D(196,(5,5)),
    tf.keras.layers.Activation('relu'),    
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.GlobalMaxPooling2D(),    
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(.25),
    tf.keras.layers.Dense(10,activation='softmax')
])
adv_config=nsl.configs\
.make_adv_reg_config(multiplier=.2,adv_step_size=.05)
adv_model=nsl.keras\
.AdversarialRegularization(base_model,adv_config=adv_config)
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train4=tf.data.Dataset.from_tensor_slices(
    {'input':x_train4,'label':y_train4}).batch(batch_size)
valid4=tf.data.Dataset.from_tensor_slices(
    {'input':x_valid4,'label':y_valid4}).batch(batch_size)
valid_steps=x_valid4.shape[0]//batch_size
adv_model.fit(train4,validation_data=valid4,verbose=2,
              validation_steps=valid_steps,epochs=epochs)

adv_model.evaluate({'input':x_test4,'label':y_test4})