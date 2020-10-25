# -*- coding: utf-8 -*-
"""letter_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19B40eERSKfVO5zsizehxPOLdhLs5YcUT

# 📑   Deep Learning. P2: Multi-Label Classification. Letter Generator
## ✒️ &nbsp; Importing Libraries and Defining Helpful Functions
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import h5py,urllib,zipfile
import pandas as pd,numpy as np,pylab as pl
import keras as ks,tensorflow as tf
import warnings; warnings.filterwarnings('ignore')
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint,ReduceLROnPlateau
from keras.optimizers import Adam,Nadam
from keras.models import Sequential,load_model,Model
from keras.layers import Input,Activation,Dense,LSTM
from keras.layers import Flatten,Dropout,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D,GlobalMaxPooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers.advanced_activations import PReLU,LeakyReLU
i0,i1,i2,i3,i4,i5,i6,i7,i8=\
int(0),int(1),int(2),int(3),int(4),int(5),int(6),int(7),int(8)
i32,i128,i255,i1024=int(32),int(128),int(255),int(1024)
np.set_printoptions(precision=8); il=10**2
from keras import __version__
print('keras version:',__version__)
print('tensorflow version:',tf.__version__)

def preprocess(x):    
    x=(x-.5)*2
    return np.clip(x,-i1,i1)
def deprocess(x):
    x=(x/2+.5)*255
#    np.place(x,x>int(220),i255)
    x=np.clip(x,i0,i255)
    x=np.uint8(x)
    return x.reshape(i32,i32)
def latent_samples(n_samples,sample_size):
    return np.random.normal(loc=i0,scale=i1,
                            size=(n_samples,sample_size))
latent_sample1024=latent_samples(i1,i1024)
latent_sample128=latent_samples(i1,i128)
def display_images(generated_images):
    n_images=len(generated_images)
    rows=i4; cols=n_images//rows    
    pl.figure(figsize=(cols,rows))
    for i in range(n_images):
        img=deprocess(generated_images[i])
        pl.subplot(rows,cols,i+i1)
        pl.imshow(img,cmap=pl.cm.Greys)
        pl.xticks([]); pl.yticks([])
    pl.tight_layout(); pl.show()

"""## ✒️ &nbsp; Loading & Preprocessing the Data"""

fpath='https://olgabelitskaya.github.io/'
zf='LetterColorImages2.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb')
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys())
letters=u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
images=np.array(f[keys[1]])/255
labels=np.array(f[keys[2]])
pl.figure(figsize=(2,3))
pl.title('Label: %s \n'%letters[labels[il]-i1],
         fontsize=18)
pl.imshow(images[il]); pl.show()

gray_images=np.dot(images[...,:3],[.299,.587,.114])
N=int(5000); gray_images=gray_images[:N]
gray_images=gray_images.reshape(-i1,i32*i32)
pl.figure(figsize=(2,3))
pl.title('Label: %s \n'%letters[labels[il]-i1],fontsize=18)
img=np.array(gray_images[il].reshape(32,32))
pl.imshow(img.astype(float),
          cmap=pl.cm.Greys); pl.show()
del images
gray_images.shape,gray_images.dtype

pl.figure(figsize=(2,3))
img0=np.squeeze(latent_sample1024).reshape(i32,i32)
pl.imshow(img0,cmap=pl.cm.Greys); pl.show()

X_train_real,X_test_real=\
train_test_split(gray_images,test_size=.1)
X_train_real=preprocess(X_train_real)
X_test_real=preprocess(X_test_real)
display_images(X_train_real[:i32])
X_train_real.shape,X_test_real.shape

"""## ✒️ &nbsp; Keras GAN
[`"Using GAN for Generating Hand-written Digit Images" by Naoki Shibuya`](https://github.com/naokishibuya/deep-learning/blob/master/python/gan_mnist.ipynb)

#### A Simple Example
"""

discriminator=Sequential([Dense(i128,input_shape=(i1024,)),
                          LeakyReLU(alpha=.01),
                          Dense(i1),Activation('sigmoid')], 
                         name='discriminator')
discriminator.summary()

fig=pl.figure(figsize=(4,3))
ax=fig.add_subplot(121)
img=X_train_real[il].reshape(i1,i1024)
ax.set_title(discriminator.predict(img))
ax.imshow(img.reshape(i32,i32),cmap=pl.cm.Greys)
ax=fig.add_subplot(122)
ax.set_title(discriminator.predict(img0.reshape(i1,i1024)))
ax.imshow(img0,cmap=pl.cm.Greys); pl.show()

generator=Sequential([Dense(i1024,input_shape=(i128,)),
                      LeakyReLU(alpha=.01),
                      Dense(i1024),Activation('tanh')], 
                     name='generator')
generator.summary()

pl.figure(figsize=(2,3))
generated_latent_sample=generator.predict(latent_sample128)
pl.title(discriminator.predict(generated_latent_sample))
pl.imshow(generated_latent_sample.reshape(i32,i32),
           cmap=pl.cm.Greys); pl.show()

gan=Sequential([generator,discriminator])
gan.summary()

"""#### Building the GAN Model"""

def trainable(model,trainable):
    for layer in model.layers:
        layer.trainable=trainable
def simple_GAN(sample_size, 
               g_hidden_size, 
               d_hidden_size, 
               leaky_alpha, 
               g_learning_rate,
               d_learning_rate):    
    ks.backend.clear_session()    
    generator=Sequential([Dense(g_hidden_size,input_shape=(sample_size,)),
                          LeakyReLU(alpha=leaky_alpha),
                          Dense(i1024),Activation('tanh')], 
                         name='generator')    
    discriminator=Sequential([Dense(d_hidden_size,input_shape=(i1024,)),
                              LeakyReLU(alpha=leaky_alpha),
                              Dense(i1),Activation('sigmoid')], 
                             name='discriminator')        
    gan=Sequential([generator,discriminator])    
    discriminator.compile(optimizer=Adam(lr=d_learning_rate), 
                          loss='binary_crossentropy')
    gan.compile(optimizer=Adam(lr=g_learning_rate), 
                loss='binary_crossentropy')   
    return gan,generator,discriminator

sample_size    =i128     
g_hidden_size  =i1024  # generator
d_hidden_size  =i128   # discriminator
leaky_alpha    =.02
g_learning_rate=.0001    # generator
d_learning_rate=.0007   # discriminator
epochs         =int(1000)
batch_size     =int(128)      
valid_size     =int(16)     
smooth         =.08
def real_fake_labels(size):
    return np.ones([size,i1]),np.zeros([size,i1])
y_real5,y_fake5=real_fake_labels(5)
print('Real\n',y_real5,'\nFake\n',y_fake5)
y_train_real,y_train_fake=real_fake_labels(batch_size)
y_valid_real,y_valid_fake=real_fake_labels(valid_size)
gan,generator,discriminator=\
simple_GAN(sample_size,g_hidden_size,d_hidden_size,
           leaky_alpha,g_learning_rate,d_learning_rate)

losses=[]
for e in range(epochs):
    for i in range(len(X_train_real)//batch_size):
        # real images
        X_batch_real=X_train_real[i*batch_size:(i+1)*batch_size]        
        # latent samples and generated letter images
        batch_latent_samples=latent_samples(batch_size,sample_size)
        X_batch_fake=generator.predict_on_batch(batch_latent_samples)        
        # train the discriminator to detect real and fake images
        trainable(discriminator,True)
        discriminator.train_on_batch(X_batch_real,y_train_real*(1.-smooth))
        discriminator.train_on_batch(X_batch_fake,y_train_fake)
        # train the generator via GAN
        trainable(discriminator,False)
        gan.train_on_batch(batch_latent_samples,y_train_real)    
    # evaluate
    X_valid_real=X_test_real[np.random.choice(len(X_test_real), 
                                              valid_size,replace=False)]    
    valid_latent_samples=latent_samples(valid_size,sample_size)
    X_valid_fake=generator.predict_on_batch(valid_latent_samples)
    d_loss=discriminator.test_on_batch(X_valid_real,y_valid_real)
    d_loss+=discriminator.test_on_batch(X_valid_fake,y_valid_fake)
    g_loss=gan.test_on_batch(valid_latent_samples,y_valid_real)     
    losses.append((d_loss,g_loss))
    st="Epoch: %d/%d | Discriminator Loss: %.4f | "+\
       "Generator Loss: %.4f | DL > GL: %s"
    if (e+i1)%int(10)==i0:
        print(st%((e+i1,epochs,d_loss,g_loss,d_loss>g_loss)))
        if ((g_loss<.9) and (d_loss>g_loss)):
            latent_examples=latent_samples(i32,sample_size)
            generated_letters=generator.predict(latent_examples)
            display_images(generated_letters)

def display_loss(losses,n):
    indices=[i*n for i in range(len(losses)//n)]
    n_losses=np.array(losses)[indices,:]    
    pl.figure(figsize=(12,6))
    pl.plot(n_losses.T[i0],'-o',c='#37c9e1',lw=i1,
            label='Discriminator')
    pl.plot(n_losses.T[1],'-o',c='#39d4be',lw=i1,
            label='Generator')
    pl.title("Training Loss Functions")
    pl.legend(); pl.show()
display_loss(losses,i4)