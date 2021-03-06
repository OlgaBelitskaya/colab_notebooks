# -*- coding: utf-8 -*-
"""tensorflow_cookbook8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W_YCeU8nOFmIYzYelXnkPU9vlie7iECx

## ✒️ Code Modules
"""

from IPython.display import display,HTML,Image
from IPython.core.magic import register_line_magic
import tensorflow as tf,tensorflow_hub as hub
import os,h5py,urllib,imageio
import pandas as pd,numpy as np,pylab as pl
file_path='https://raw.githubusercontent.com/'+\
           'OlgaBelitskaya/data_kitchen/main/'
file_name='HorseBreeds160.h5'
img_size=96

"""## ✒️  Image Data"""

def get_data(file_path,file_name,img_size=160):
    input_file=urllib.request.urlopen(file_path+file_name)
    output_file=open(file_name,'wb')
    output_file.write(input_file.read())
    output_file.close(); input_file.close()
    with h5py.File(file_name,'r') as f:
        keys=list(f.keys())
        print('file keys: '+', '.join(keys))
        images=np.array(f[keys[0]])
        images=tf.image.resize(images,[img_size,img_size]).numpy()
        labels=np.array(f[keys[1]])
        names=[el.decode('utf-8')for el in f[keys[2]]]
        f.close()
    return images,labels,names
images,labels,names=get_data(file_path,file_name,img_size)

"""## ✒️ Data Processing"""

N=labels.shape[0]; n=int(.1*N)
num_classes=len(names); start=int(100) 
shuffle_ids=np.arange(N)
np.random.RandomState(12).shuffle(shuffle_ids)
images=images[shuffle_ids]; labels=labels[shuffle_ids]
x_test,x_valid,x_train=images[:n],images[n:2*n],images[2*n:]
y_test,y_valid,y_train=labels[:n],labels[n:2*n],labels[2*n:]
df=pd.DataFrame(
    [[x_train.shape,x_valid.shape,x_test.shape],
     [x_train.dtype,x_valid.dtype,x_test.dtype],
     [y_train.shape,y_valid.shape,y_test.shape],
     [y_train.dtype,y_valid.dtype,y_test.dtype]],
    columns=['train','valid','test'],
    index=['image shape','image type','label shape','label type'])
def display_imgs(images,labels,names,start):
    fig=pl.figure(figsize=(12,6)); n=np.random.randint(0,start-1)
    for i in range(n,n+6):
        ax=fig.add_subplot(2,3,i-n+1,xticks=[],yticks=[])
        ax.set_title(
            names[labels[i]],color='slategray',fontdict={'fontsize':'large'})
        ax.imshow((images[i]))
    pl.tight_layout(); pl.show()
display_imgs(images,labels,names,start); display(df)

"""## ✒️ Super Resolution"""

def esrgantf2_superresolution(img,img_size=int(50)):
    model=hub.load('https://tfhub.dev/captain-pool/esrgan-tf2/1')
    func=model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
    func.inputs[int(0)].set_shape([int(1),img_size,img_size,int(3)])
    converter=tf.lite.TFLiteConverter.from_concrete_functions([func])
    converter.optimizations=[tf.lite.Optimize.DEFAULT]
    tflite_model=converter.convert()
    with tf.io.gfile.GFile('ESRGAN.tflite','wb') as f:
        f.write(tflite_model)
    esrgan_model_path='./ESRGAN.tflite'
    if img.mean()<float(1): img=img*float(255)
    lr=tf.image.resize(img,[img_size,img_size])
    lr=tf.expand_dims(lr.numpy()[:,:,:int(3)],axis=int(0))
    lr=tf.cast(lr,tf.float32)
    interpreter=tf.lite.Interpreter(model_path=esrgan_model_path)
    interpreter.allocate_tensors()
    input_details=interpreter.get_input_details()
    output_details=interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'],lr)
    interpreter.invoke()
    output_data=interpreter.get_tensor(output_details[int(0)]['index'])
    sr=tf.squeeze(output_data,axis=0)
    sr=tf.clip_by_value(sr,0,255)
    sr=tf.round(sr); sr=tf.cast(sr,tf.uint8)
    lr=tf.cast(tf.squeeze(lr,axis=0),tf.uint8)
    return lr,sr
lr,sr=esrgantf2_superresolution(images[0],img_size)

def low2super_bicubic_contrast(lr,sr):
    pl.figure(figsize=(12,6)); pl.title('LR')
    pl.imshow(lr.numpy()); pl.show()
    pl.figure(figsize=(12,6))
    pl.subplot(1,2,1); pl.title('ESRGAN x4')
    pl.imshow(sr.numpy())
    img_size=lr.shape[1]
    bicubic=tf.image.resize(
        lr,[img_size*4,img_size*4],
        tf.image.ResizeMethod.BICUBIC)
    bicubic_contrast=tf.image.adjust_contrast(bicubic,.8)
    bicubic_contrast=tf.cast(bicubic_contrast,tf.uint8)
    pl.subplot(1,2,2); pl.title('Bicubic & Contrast')
    pl.imshow(bicubic_contrast.numpy())
    pl.tight_layout(); pl.show()
low2super_bicubic_contrast(lr,sr)

"""## ✒️ Color Interpolation"""

def interpolate_hypersphere(v1,v2,steps):
    v1norm=tf.norm(v1); v2norm=tf.norm(v2)
    v2normalized=v2*(v1norm/v2norm)
    vectors=[]
    for step in range(steps):
        interpolated=v1+(v2normalized-v1)*step/(steps-1)
        interpolated_norm=tf.norm(interpolated)
        interpolated_normalized=interpolated*(v1norm/interpolated_norm)
        vectors.append(interpolated_normalized)
    return tf.stack(vectors).numpy()

lr1,sr1=esrgantf2_superresolution(x_train[0],img_size)
lr2,sr2=esrgantf2_superresolution(x_train[1],img_size)

steps=30
img1=sr1.numpy()/255; img2=sr2.numpy()/255
imgs=np.vstack([interpolate_hypersphere(img1,img2,steps),
                interpolate_hypersphere(img2,img1,steps)])

file_name='pic.gif'
imgs=np.clip(imgs*255,0,255)
imgs=np.array(imgs,dtype=np.uint8)
imageio.mimsave(file_name,imgs)
Image(open('pic.gif','rb').read())