# -*- coding: utf-8 -*-
"""image_generator5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZT6ujInkGn_U0cqkPLsoOW8KzTmGQzFi
"""

# Commented out IPython magic to ensure Python compatibility.
from IPython import display
def dhtml(st):
    display.display(display.HTML("""<style>
    @import url('https://fonts.googleapis.com/css?family=Roboto|Orbitron&effect=3d');      
    </style><p class='font-effect-3d' onclick='setStyle(this,"#ff6600")'
    style='font-family:Roboto; font-size:25px; color:#ff355e;'>
#     %s</p>"""%st+"""<script>
    function setStyle(element,c) {
     var docs=document.getElementsByClassName('font-effect-3d');
     for (var i=0; i<docs.length; i++) {
         docs[i].style='font-family:Orbitron; font-size:22px;'; 
         docs[i].style.color=c;}; };
    </script>"""))
dhtml('Code Modules & Parameters')

!pip install git+https://github.com/tensorflow/docs

import numpy as np,pylab as pl,pandas as pd
import sys,h5py,urllib,zipfile,imageio,PIL
import tensorflow as tf
import tensorflow_hub as th
from tensorflow_docs.vis import embed

seed_size=16; noise_dim=196; epochs=120
buffer_size=60000; batch_size=256
norm_img=tf.random.normal([1,noise_dim])
seed_imgs=tf.random.normal([seed_size,noise_dim])

dhtml('Data')

(x,y),(_, _)=tf.keras.datasets.mnist.load_data()
x=x.reshape(x.shape[0],28,28,1).astype('float32')
x=(x-127.5)/127.5
digits=tf.data.Dataset.from_tensor_slices(x)\
.shuffle(buffer_size).batch(batch_size)

dhtml('Deep Convolutional Generative Adversarial Network')

def tfgenerator():
    model=tf.keras.Sequential()
    model.add(tf.keras.layers\
    .Dense(7*7*256,use_bias=False,input_shape=(noise_dim,)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Reshape((7,7,256)))
    model.add(tf.keras.layers\
    .Conv2DTranspose(256,(7,7),strides=(1,1),
                     padding='same',use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers\
    .Conv2DTranspose(16,(7,7),strides=(2,2),
                     padding='same',use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers\
    .Conv2DTranspose(1,(7,7),strides=(2,2),
                     padding='same',use_bias=False,
                     activation='tanh'))
    return model
tfgenerator=tfgenerator()

def tfdiscriminator():
    model=tf.keras.Sequential()
    model.add(tf.keras.layers\
    .Conv2D(16,(7,7),strides=(2,2),
            padding='same',input_shape=[28,28,1]))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Dropout(.2))
    model.add(tf.keras.layers\
    .Conv2D(256,(7,7),strides=(2,2),padding='same'))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Dropout(.2))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(1))
    return model
tfdiscriminator=tfdiscriminator()

generated_img=tfgenerator(norm_img,training=False)
pl.imshow(generated_img[0,:,:,0],cmap=pl.cm.bone)
pl.title(generated_img.shape)
tfdiscriminator(generated_img)

cross_entropy=tf.keras.losses.BinaryCrossentropy(from_logits=True)
def discriminator_loss(real_output,fake_output):
    real_loss=cross_entropy(tf.ones_like(real_output),real_output)
    fake_loss=cross_entropy(tf.zeros_like(fake_output),fake_output)
    total_loss=real_loss+fake_loss
    return total_loss
def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output),fake_output)
generator_optimizer=tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer=tf.keras.optimizers.Adam(1e-4)
checkpoint=tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                               discriminator_optimizer=discriminator_optimizer,
                               generator=tfgenerator,
                               discriminator=tfdiscriminator)

dhtml('Training')

@tf.function
def train_step(imgs):
    random_imgs=tf.random.normal([batch_size,noise_dim])
    with tf.GradientTape() as gen_tape,tf.GradientTape() as disc_tape:
        generated_imgs=tfgenerator(random_imgs,training=True)
        real_output=tfdiscriminator(imgs,training=True)
        fake_output=tfdiscriminator(generated_imgs,training=True)
        gen_loss=generator_loss(fake_output)
        disc_loss=discriminator_loss(real_output,fake_output)
        gradients_of_generator=\
        gen_tape.gradient(gen_loss,tfgenerator.trainable_variables)
        gradients_of_discriminator=\
        disc_tape.gradient(disc_loss,tfdiscriminator.trainable_variables)
        generator_optimizer\
        .apply_gradients(zip(gradients_of_generator,
                             tfgenerator.trainable_variables))
        discriminator_optimizer\
        .apply_gradients(zip(gradients_of_discriminator,
                             tfdiscriminator.trainable_variables))

def generate_images(model,epoch,test_input):
    predictions=model(test_input,training=False)
    fig=pl.figure(figsize=(4,4))
    for i in range(predictions.shape[0]):
        pl.subplot(4,4,i+1)
        pl.imshow(predictions[i,:,:,0]*127.5+127.5,
                  cmap=pl.cm.bone)
        pl.axis('off')
    pl.savefig('epoch_{:04d}.png'.format(epoch+1))
    pl.suptitle('Epoch: %04d'%(epoch+1),
                color='#ff355e',fontsize=20)
    pl.show()

def train(data,epochs):
    for epoch in range(epochs):
        for image_batch in data:
            train_step(image_batch)
 #           display.clear_output(wait=True)
        if (epoch+1)%10==0:
            generate_images(tfgenerator,epoch,seed_imgs)
#        if (epoch+1)%10==0:
#            checkpoint.save(file_prefix='')
#            display.clear_output(wait=True)
#            generate_images(tfgenerator,epochs,seed_imgs)

train(digits,epochs)

PIL.Image.open('epoch_{:04d}.png'.format(60))

dhtml('Interpolation')

def animate(images):
    converted_images=np.clip(images*255,0,255)\
    .astype(np.uint8)
    imageio.mimsave('animation.gif',converted_images)
    return embed.embed_file('animation.gif')

def interpolate_hypersphere(v1,v2,steps):
    v1norm=tf.norm(v1)
    v2norm=tf.norm(v2)
    v2normalized=v2*(v1norm/v2norm)
    vectors=[]
    for step in range(steps):
        interpolated=v1+(v2normalized-v1)*step/(steps-1)
        interpolated_norm=tf.norm(interpolated)
        interpolated_normalized=\
        interpolated*(v1norm/interpolated_norm)
        vectors.append(interpolated_normalized)
    return tf.stack(vectors)

def interpolate_between_vectors(steps):
    tf.random.set_seed(1)
    v1=tf.random.normal([noise_dim])
    v2=tf.random.normal([noise_dim])
    vectors=interpolate_hypersphere(v1,v2,steps)
    interpolated_imgs=tfgenerator(vectors,training=False)
    interpolated_imgs=\
    tf.image.resize(interpolated_imgs,[128,128])
    return interpolated_imgs

imgs=interpolate_between_vectors(120)
animate(imgs)

dhtml('Parameters 2 & Data 2')

seed_size=16; noise_dim=256; img_size=42
epochs=150; buffer_size=11000; batch_size=128
norm_img=tf.random.normal([1,noise_dim])
seed_imgs=tf.random.normal([seed_size,noise_dim])

fpath='https://olgabelitskaya.github.io/'
zf='LetterColorImages_123.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb'); 
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys()); print(keys)
x=np.array(f[keys[1]],dtype='float32')
x=tf.image.resize(x,[img_size,img_size]).numpy()
x=np.dot(x,[.299,.587,.114])
x=x.reshape(-1,img_size,img_size,1)
y=np.array(f[keys[2]],dtype='int32')\
.reshape(-1,1)-1
N=len(y); n=int(.1*N)
shuffle_ids=np.arange(N)
np.random.RandomState(23).shuffle(shuffle_ids)
x,y=x[shuffle_ids],y[shuffle_ids]

x=(x-127.5)/127.5
pl.imshow((255-x[0]).reshape(img_size,img_size),
          cmap=pl.cm.bone)
pl.title(x[0].shape)
letters=tf.data.Dataset.from_tensor_slices(x)\
.shuffle(buffer_size).batch(batch_size)

dhtml('DCGAN 2')

def tfgenerator2():
    model=tf.keras.Sequential()
    model.add(tf.keras.layers\
    .Dense(7*7*256,use_bias=False,input_shape=(noise_dim,)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Reshape((7,7,256)))
    model.add(tf.keras.layers\
    .Conv2DTranspose(256,(7,7),strides=(3,3),
                     padding='same',use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers\
    .Conv2DTranspose(32,(7,7),strides=(2,2),
                     padding='same',use_bias=False))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers\
    .Conv2DTranspose(1,(7,7),strides=(1,1),
                     padding='same',use_bias=False,
                     activation='tanh'))
    return model
tfgenerator2=tfgenerator2()

def tfdiscriminator2():
    model=tf.keras.Sequential()
    model.add(tf.keras.layers\
    .Conv2D(32,(7,7),strides=(2,2),padding='same',
            input_shape=[img_size,img_size,1]))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Dropout(.2))
    model.add(tf.keras.layers\
    .Conv2D(256,(7,7),strides=(2,2),padding='same'))
    model.add(tf.keras.layers.LeakyReLU())
    model.add(tf.keras.layers.Dropout(.2))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(1))
    return model
tfdiscriminator2=tfdiscriminator2()

generated_img=tfgenerator2(norm_img,training=False)
pl.imshow(generated_img[0,:,:,0],cmap=pl.cm.bone)
pl.title(generated_img.shape);
tfdiscriminator2(generated_img)

cross_entropy=tf.keras.losses.BinaryCrossentropy(from_logits=True)
def discriminator_loss(real_output,fake_output):
    real_loss=cross_entropy(tf.ones_like(real_output),real_output)
    fake_loss=cross_entropy(tf.zeros_like(fake_output),fake_output)
    total_loss=real_loss+fake_loss
    return total_loss
def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output),fake_output)
generator_optimizer2=tf.keras.optimizers.Adam(1e-3)
discriminator_optimizer2=tf.keras.optimizers.Adam(1e-3)

dhtml('Training')

@tf.function
def train_step2(imgs):
    random_imgs=tf.random.normal([batch_size,noise_dim])
    with tf.GradientTape() as gen_tape,tf.GradientTape() as disc_tape:
        generated_imgs=tfgenerator2(random_imgs,training=True)
        real_output=tfdiscriminator2(imgs,training=True)
        fake_output=tfdiscriminator2(generated_imgs,training=True)
        gen_loss=generator_loss(fake_output)
        disc_loss=discriminator_loss(real_output,fake_output)
        gradients_of_generator=\
        gen_tape.gradient(gen_loss,tfgenerator2.trainable_variables)
        gradients_of_discriminator=\
        disc_tape.gradient(disc_loss,tfdiscriminator2.trainable_variables)
        generator_optimizer2\
        .apply_gradients(zip(gradients_of_generator,
                             tfgenerator2.trainable_variables))
        discriminator_optimizer2\
        .apply_gradients(zip(gradients_of_discriminator,
                             tfdiscriminator2.trainable_variables))

def generate_images2(model,epoch,test_input):
    predictions=model(test_input,training=False)
    fig=pl.figure(figsize=(4,4))
    for i in range(predictions.shape[0]):
        pl.subplot(4,4,i+1)
        pl.imshow(127.5-predictions[i,:,:,0]*127.5,
                  cmap=pl.cm.bone)
        pl.axis('off')
    pl.savefig('epoch_{:04d}.png'.format(epoch+1))
    pl.suptitle('Epoch: %04d'%(epoch+1),
                color='#ff355e',fontsize=20)
    pl.show()

def train2(data,epochs):
    for epoch in range(epochs):
        for image_batch in data:
            train_step2(image_batch)
        if (epoch+1)%10==0:
            generate_images2(tfgenerator2,epoch,seed_imgs)

train2(letters,epochs)

PIL.Image.open('epoch_{:04d}.png'.format(130))

def interpolate_between_vectors2(steps):
    tf.random.set_seed(123)
    v1=tf.random.normal([noise_dim])
    v2=tf.random.normal([noise_dim])
    vectors=interpolate_hypersphere(v1,v2,steps)
    interpolated_imgs=tfgenerator2(vectors,training=False)
#    interpolated_imgs=127.5-interpolated_imgs*127.5
    interpolated_imgs=\
    tf.image.resize(interpolated_imgs,[128,128])
    return interpolated_imgs

imgs=interpolate_between_vectors2(180)
animate(imgs)