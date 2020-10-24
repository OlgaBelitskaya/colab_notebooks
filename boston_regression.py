# -*- coding: utf-8 -*-
"""boston_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1atPu92jNJ-qBsFpbOiMojHGXCu6gJWYW

# 📑 &nbsp; Deep Learning. P1: Neural Networks for Regression

<a href="https://olgabelitskaya.github.io/README.html">&#x1F300; &nbsp; Home Page &nbsp; &nbsp; &nbsp;</a> 
<a href="https://www.instagram.com/olga.belitskaya/">&#x1F300; &nbsp; Instagram Posts &nbsp; &nbsp; &nbsp;</a>  <a href="https://www.pinterest.ru/olga_belitskaya/code-style/">&#x1F300; &nbsp; Pinterest Posts &nbsp; &nbsp; &nbsp;</a><br/>
In this project, we'll evaluate the performance and predictive power of neural networks in the sphere of regression tasks. Models will be trained and tested on data collected from homes in suburbs of Boston, Massachusetts.

Origin: This dataset was taken from the StatLib library which is maintained at Carnegie Mellon University.

Creators: Harrison, D. and Rubinfeld, D.L.

Data Set Information: Concerns housing values in suburbs of Boston.

Attribute Information:

- CRIM: per capita crime rate by town
- ZN: proportion of residential land zoned for lots over 25,000 sq.ft.
- INDUS: proportion of non-retail business acres per town
- CHAS: Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
- NOX: nitric oxides concentration (parts per 10 million)
- RM: average number of rooms per dwelling
- AGE: proportion of owner-occupied units built prior to 1940
- DIS: weighted distances to five Boston employment centres
- RAD: index of accessibility to radial highways
- TAX: full-value property-tax rate per 10,000 USD
- PTRATIO: pupil-teacher ratio by town
- B: 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
- LSTAT: % lower status of the population
- MEDV: Median value of owner-occupied homes in 1000 USD
"""

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <style>
# @import url('https://fonts.googleapis.com/css?family=Akronim|Ruthie');
# </style>
# <table style="width:60%; background-color:black; 
#               font-family:Ruthie; font-size:200%;">
# <tr style="color:white; font-family:Akronim;">
#   <th> Attribute </th><th> Description </th></tr>
# <tr><td style="color:#F898C8;"><center> CRIM </center></td>
# <td style="color:#F898C8;"><left>per capita crime rate by town</left></td></tr>
# <tr><td style="color:#E91E63;"><center> ZN </center></td>
# <td style="color:#E91E63;"><left>proportion of residential 
#   land zoned for lots over 25,000 sq.ft.</left></td></tr>
# <tr><td style="color:#D62518;"><center> INDUS </center></td>
# <td style="color:#D62518;"><left>proportion of non-retail 
#   business acres per town</left></td></tr>
# <tr><td style="color:#AD0000;"><center> CHAS </center></td>
# <td style="color:#AD0000;"><left>Charles River dummy variable 
#   (= 1 if tract bounds river; 0 otherwise)</left></td></tr>
# <tr><td style="color:#FA7A00;"><center> NOX </center></td>
# <td style="color:#FA7A00;"><left>nitric oxides concentration 
#   (parts per 10 million)</left></td></tr> 
# <tr><td style="color:#FED85D;"><center> RM </center></td>
# <td style="color:#FED85D;"><left>average number of rooms 
#   per dwelling</left></td></tr> 
#   <tr><td style="color:#91E351;"><center> AGE </center></td>
# <td style="color:#91E351;"><left>proportion of 
#   owner-occupied units built prior to 1940</left></td></tr> 
# <tr><td style="color:#00D8A0;"><center> DIS </center></td>
# <td style="color:#00D8A0;"><left>weighted distances to 
#   five Boston employment centres</left></td></tr> 
# <tr><td style="color:#1CAC78;"><center> RAD </center></td>
# <td style="color:#1CAC78;"><left>index of accessibility 
#   to radial highways</left></td></tr>
#   <tr><td style="color:#004C71;"><center> TAX </center></td>
# <td style="color:#004C71;"><left>full-value property-tax rate 
#   per 10,000 USD</left></td></tr>
# <tr><td style="color:#1AADE0;"><center> PTRATIO </center></td>
# <td style="color:#1AADE0;"><left>pupil-teacher ratio by town</left></td></tr>
# <tr><td style="color:#0069BD;"><center> B </center></td>
# <td style="color:#0069BD;"><left>1000(Bk - 0.63)^2 where Bk 
#   is the proportion of blacks by town</left></td></tr>
# <tr><td style="color:#333399;"><center> LSTAT </center></td>
# <td style="color:#333399;"><left>% lower status of the population</left></td></tr> 
# <tr><td style="color:#7851A9;"><center> MEDV </center></td>
# <td style="color:#7851A9;"><left>Median value of owner-occupied homes 
#   in 1000 USD</left></td></tr>
# </table>

"""The Boston housing data was collected in 1978 and each of the 

506 entries represents aggregated data about 14 features for homes from various suburbs.
## ✒️ &nbsp;Step 0. Import Libraries and Define Helpful Functions
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import pandas as pd,numpy as np,sqlite3
import seaborn as sn,pylab as pl
import keras as ks,tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import datasets,linear_model,svm
from sklearn.metrics import mean_squared_error,median_absolute_error,\
mean_absolute_error,r2_score,explained_variance_score
from sklearn.tree import DecisionTreeRegressor,ExtraTreeRegressor
from sklearn.ensemble import BaggingRegressor,RandomForestRegressor,\
AdaBoostRegressor,GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor,RadiusNeighborsRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis,\
QuadraticDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.kernel_ridge import KernelRidge
from sklearn.cross_decomposition import PLSRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel,RationalQuadratic,RBF
from sklearn.semi_supervised import LabelPropagation,LabelSpreading
from sklearn.isotonic import IsotonicRegression
from keras.datasets import boston_housing
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential,load_model
from keras.layers import Dense,LSTM,GlobalAveragePooling1D
from keras.layers import Activation,Flatten,Dropout,BatchNormalization
from keras.layers import Conv1D,MaxPooling1D,GlobalMaxPooling1D
from keras.layers.advanced_activations import PReLU,LeakyReLU

def connect_to_db(dbf):
    sqlconn=None
    try:
        sqlconn=sqlite3.connect(dbf)
        return sqlconn
    except Error as err:
        print(err)
        if sqlconn is not None:
            sqlconn.close()
connection=connect_to_db('boston.db')
if connection is not None:
    cursor=connection.cursor()

def history_plot(fit_history,n):
    pl.figure(figsize=(12,10))    
    pl.subplot(211)
    pl.plot(fit_history.history['loss'][n:],
            color='slategray',label='train')
    pl.plot(fit_history.history['val_loss'][n:],
            color='#348ABD',label='valid')
    pl.xlabel('Epochs'); pl.ylabel('Loss')
    pl.legend(); pl.title('Loss Function')      
    pl.subplot(212)
    pl.plot(fit_history.history['mean_absolute_error'][n:],
            color='slategray',label='train')
    pl.plot(fit_history.history['val_mean_absolute_error'][n:],
            color='#348ABD',label='valid')
    pl.xlabel('Epochs'); pl.ylabel('MAE')    
    pl.legend(); pl.title('Mean Absolute Error')
    pl.show()

def predpl(y1,y2,y3,ti):
    pl.figure(figsize=(12,6))
    pl.scatter(range(n),y_test[:n],marker='*',s=100,
               color='black',label='Real data')
    pl.plot(y1[:n],label='MLP')
    pl.plot(y2[:n],label='CNN')
    pl.plot(y3[:n],label='RNN')
    pl.xlabel("Data Points")
    pl.ylabel("Predicted and Real Target Values")
    pl.legend(); pl.title(ti); pl.show()

"""## ✒️ &nbsp;Step 1. Load and Explore the Data"""

boston_data=datasets.load_boston()
columns=boston_data.feature_names
boston_df=pd.DataFrame(boston_data.data,columns=columns)
boston_df['MEDV']=boston_data.target
boston_df.to_sql('main',con=connection,if_exists='replace')
boston_df.head(7)

pearson=boston_df.corr(method='pearson')
corr_with_prices=pearson.iloc[-1][:-1]
pd.DataFrame(corr_with_prices[abs(corr_with_prices)\
             .argsort()[::-1]]).T

pd.read_sql_query('''
SELECT ZN,
       AVG(LSTAT),
       AVG(RM),
       AVG(PTRATIO),
       AVG(INDUS),
       AVG(TAX)
FROM main
GROUP BY ZN;
''',con=connection)\
.set_index('ZN').head(7)

n=int(51)
(x_train,y_train),(x_test,y_test)=boston_housing.load_data()
x_valid,y_valid=x_test[:n],y_test[:n]
x_test,y_test=x_test[n:],y_test[n:]
pd.DataFrame([["Training feature's shape:",x_train.shape],
              ["Training target's shape",y_train.shape],
              ["Validating feature's shape:",x_valid.shape],
              ["Validating target's shape",y_valid.shape],
              ["Testing feature's shape:",x_test.shape],
              ["Testing target's shape",y_test.shape]])

pl.style.use('seaborn-whitegrid')
pl.figure(1,figsize=(12,4))
pl.subplot(121)
sn.distplot(y_train,color='#348ABD',bins=30)
pl.ylabel("Distribution"); pl.xlabel("Prices")
pl.subplot(122)
sn.distplot(np.log(y_train), color='#348ABD',bins=30)
pl.ylabel("Distribution"); pl.xlabel("Logarithmic Prices")
pl.suptitle('Boston Housing Data',fontsize=15)
pl.show()

"""## ✒️ &nbsp;Step 2. Build Neural Networks with Keras Py
<p>Multilayer Perceptron (MLP)</p><br/>
"""

i0,i1,i2,i10,i13,i104,i1024=\
int(0),int(1),int(2),int(10),int(13),int(104),int(1024)
def mlp_model():
    model=Sequential() 
    model.add(Dense(i1024,input_dim=i13))
    model.add(LeakyReLU(alpha=float(.025)))   
    model.add(Dense(i104))     
    model.add(LeakyReLU(alpha=float(.025)))   
    model.add(Dense(i1,kernel_initializer='normal'))    
    model.compile(loss='mse',optimizer='rmsprop',metrics=['mae'])
    return model
mlp_model=mlp_model()

epochs=int(600); batch_size=int(24)
fw='weights.boston.mlp.hdf5'
mlp_checkpointer=ModelCheckpoint(filepath=fw,verbose=i0,
                                 save_best_only=True)
mlp_lr_reduction=ReduceLROnPlateau(monitor='val_loss',patience=i10,
                                   verbose=i0,factor=float(.75))
mlp_history=mlp_model.fit(x_train,y_train,batch_size=batch_size, 
                          validation_data=(x_valid,y_valid),
                          epochs=epochs,verbose=i0, 
                          callbacks=[mlp_checkpointer,mlp_lr_reduction])

history_plot(mlp_history,i2)

mlp_model.load_weights(fw)
y_train_mlp=mlp_model.predict(x_train)
y_valid_mlp=mlp_model.predict(x_valid)
y_test_mlp=mlp_model.predict(x_test)
score_train_mlp=r2_score(y_train,y_train_mlp)
score_valid_mlp=r2_score(y_valid,y_valid_mlp)
score_test_mlp=r2_score(y_test,y_test_mlp)
pd.DataFrame([['Train R2 score:',score_train_mlp],
              ['Valid R2 score:',score_valid_mlp],
              ['Test R2 score:',score_test_mlp]])

"""#### Convolutional Neural Network (CNN)"""

i1,i2,i3,i5,i10,i13,i16,i128=\
int(1),int(2),int(3),int(5),int(10),int(13),int(16),int(128)
def cnn_model():
    model=Sequential()       
    model.add(Conv1D(i13,i5,padding='valid',
                     input_shape=(i13,i1)))
    model.add(LeakyReLU(alpha=float(.025)))
    model.add(MaxPooling1D(pool_size=i2))   
    model.add(Conv1D(i128,i3,padding='valid'))
    model.add(LeakyReLU(alpha=float(.025)))
    model.add(MaxPooling1D(pool_size=i2))   
    model.add(Flatten())      
    model.add(Dense(i16,activation='relu',
                    kernel_initializer='normal'))
    model.add(Dropout(float(.1)))  
    model.add(Dense(i1,kernel_initializer='normal'))  
    model.compile(loss='mse',optimizer='nadam',metrics=['mae'])
    return model
cnn_model=cnn_model()

epochs=int(500); batch_size=int(14)
fw='weights.boston.cnn.hdf5'
cnn_checkpointer=ModelCheckpoint(filepath=fw,verbose=i0,save_best_only=True)
cnn_lr_reduction=ReduceLROnPlateau(monitor='val_loss', 
                                   patience=i10,verbose=i0,factor=float(.75))
cnn_history=cnn_model.fit(x_train.reshape(-i1,i13,i1),y_train, 
                          validation_data=(x_valid.reshape(-i1,i13,i1),y_valid),
                          epochs=epochs,batch_size=batch_size,verbose=i0, 
                          callbacks=[cnn_checkpointer,cnn_lr_reduction])

history_plot(cnn_history,i2)

cnn_model.load_weights(fw)
y_train_cnn=cnn_model.predict(x_train.reshape(-1,13,1))
y_valid_cnn=cnn_model.predict(x_valid.reshape(-1,13,1))
y_test_cnn=cnn_model.predict(x_test.reshape(-1,13,1))
score_train_cnn=r2_score(y_train,y_train_cnn)
score_valid_cnn=r2_score(y_valid,y_valid_cnn)
score_test_cnn=r2_score(y_test,y_test_cnn)
pd.DataFrame([['Train R2 score:',score_train_cnn],
              ['Valid R2 score:',score_valid_cnn],
              ['Test R2 score:',score_test_cnn]])

"""#### Recurrent Neural Network (RNN)"""

i1,i2,i13,i104=int(1),int(2),int(13),int(104)
def rnn_model():
    model=Sequential()   
    model.add(LSTM(i104,return_sequences=True,
                   input_shape=(i1,i13)))
    model.add(LSTM(i104,return_sequences=True))
    model.add(LSTM(i104,return_sequences=False))   
    model.add(Dense(i1))
    model.compile(optimizer='rmsprop',loss='mse',metrics=['mae'])       
    return model
rnn_model=rnn_model()

epochs=int(200); batch_size=int(14)
fw='weights.boston.rnn.hdf5'
rnn_checkpointer=ModelCheckpoint(filepath=fw,verbose=i0,
                                 save_best_only=True)
rnn_lr_reduction=ReduceLROnPlateau(monitor='val_loss', 
                                  patience=i10,verbose=i0,factor=float(.75))
rnn_history=rnn_model.fit(x_train.reshape(-i1,i1,i13),y_train, 
                          validation_data=(x_valid.reshape(-i1,i1,i13),y_valid),
                          epochs=epochs,batch_size=batch_size,verbose=i0, 
                          callbacks=[rnn_checkpointer,rnn_lr_reduction])

history_plot(rnn_history,i2)

rnn_model.load_weights(fw)
y_train_rnn=rnn_model.predict(x_train.reshape(-i1,i1,i13))
y_valid_rnn=rnn_model.predict(x_valid.reshape(-i1,i1,i13))
y_test_rnn=rnn_model.predict(x_test.reshape(-i1,i1,i13))
score_train_rnn=r2_score(y_train,y_train_rnn)
score_valid_rnn=r2_score(y_valid,y_valid_rnn)
score_test_rnn=r2_score(y_test,y_test_rnn)
pd.DataFrame([['Train R2 score:',score_train_rnn],
              ['Valid R2 score:',score_valid_rnn],
              ['Test R2 score:',score_test_rnn]])

"""## ✒️ &nbsp;Step 3. Display Predictions of Keras Algorithms Py"""

ti="Train Set; Neural Network Predictions vs Real Data"
y1,y2,y3=y_train_mlp,y_train_cnn,y_train_rnn
predpl(y1,y2,y3,ti)

ti="Validation Set; Neural Network Predictions vs Real Data"
y1,y2,y3=y_valid_mlp,y_valid_cnn,y_valid_rnn
predpl(y1,y2,y3,ti)

ti="Test Set; Neural Network Predictions vs Real Data"
y1,y2,y3=y_test_mlp,y_test_cnn,y_test_rnn
predpl(y1,y2,y3,ti)

"""## ✒️  Step 4. Compare with Sklearn Algorithms Py"""

def regressor_fit_score(regressor,regressor_name,dataset,
                        x_train,x_test,y_train,y_test,n=6):
    regressor_list.append(str(regressor))
    regressor_names.append(regressor_name)
    reg_datasets.append(dataset)    
    regressor.fit(x_train,y_train)
    y_reg_train=regressor.predict(x_train)
    y_reg_test=regressor.predict(x_test)    
    r2_reg_train=round(r2_score(y_train,y_reg_train),n)
    r2_train.append(r2_reg_train)
    r2_reg_test=round(r2_score(y_test,y_reg_test),n)
    r2_test.append(r2_reg_test)    
    ev_reg_train=round(explained_variance_score(y_train,y_reg_train),n)
    ev_train.append(ev_reg_train)
    ev_reg_test=round(explained_variance_score(y_test, y_reg_test),n)
    ev_test.append(ev_reg_test)    
    mse_reg_train=round(mean_squared_error(y_train,y_reg_train),n)
    mse_train.append(mse_reg_train)
    mse_reg_test=round(mean_squared_error(y_test,y_reg_test),n)
    mse_test.append(mse_reg_test)
    mae_reg_train=round(mean_absolute_error(y_train,y_reg_train),n)
    mae_train.append(mae_reg_train)
    mae_reg_test=round(mean_absolute_error(y_test,y_reg_test),n)
    mae_test.append(mae_reg_test)
    mdae_reg_train=round(median_absolute_error(y_train,y_reg_train),n)
    mdae_train.append(mdae_reg_train)
    mdae_reg_test=round(median_absolute_error(y_test,y_reg_test),n)
    mdae_test.append(mdae_reg_test)    
    return [y_reg_train,y_reg_test,r2_reg_train,r2_reg_test,
            ev_reg_train,ev_reg_test,
            mse_reg_train,mse_reg_test,mae_reg_train,mae_reg_test,
            mdae_reg_train,mdae_reg_test]
def get_regressor_results():
    return pd.DataFrame({'regressor':regressor_list,
                         'regressor_name':regressor_names,
                         'dataset':reg_datasets,
                         'r2_train':r2_train,'r2_test':r2_test,
                         'ev_train':ev_train,'ev_test':ev_test,
                         'mse_train':mse_train,'mse_test':mse_test,
                         'mae_train':mae_train,'mae_test':mae_test,
                         'mdae_train':mdae_train,'mdae_test':mdae_test})

(x_train,y_train),(x_test,y_test)=boston_housing.load_data()
regressor_list,regressor_names,reg_datasets=[],[],[]
r2_train,r2_test,ev_train, ev_test,mse_train,mse_test,mae_train,\
mae_test,mdae_train,mdae_test=[],[],[],[],[],[],[],[],[],[]
df_list=['regressor_name','r2_train','r2_test','ev_train','ev_test',
         'mse_train','mse_test','mae_train','mae_test',
         'mdae_train','mdae_test']
reg=[linear_model.LinearRegression(),
     linear_model.Ridge(),linear_model.RidgeCV(),
     linear_model.Lasso(),linear_model.LassoLarsCV(),
     linear_model.RANSACRegressor(),
     linear_model.BayesianRidge(),linear_model.ARDRegression(),
     linear_model.HuberRegressor(),linear_model.TheilSenRegressor(),
     PLSRegression(),DecisionTreeRegressor(),ExtraTreeRegressor(),
     BaggingRegressor(),AdaBoostRegressor(),
     GradientBoostingRegressor(),RandomForestRegressor(),
     linear_model.PassiveAggressiveRegressor(max_iter=1000,tol=0.001),
     linear_model.ElasticNet(),
     linear_model.SGDRegressor(max_iter=1000,tol=0.001),
     svm.SVR(),KNeighborsRegressor(),
     RadiusNeighborsRegressor(radius=1.5),GaussianProcessRegressor()]

listreg=['LinearRegression','Ridge','RidgeCV',
         'Lasso','LassoLarsCV','RANSACRegressor',
         'BayesianRidge','ARDRegression','HuberRegressor',
         'TheilSenRegressor','PLSRegression','DecisionTreeRegressor',
         'ExtraTreeRegressor','BaggingRegressor','AdaBoostRegressor',
         'GradientBoostingRegressor','RandomForestRegressor']
yreg=[]
for i in range(len(listreg)):
    yreg.append(regressor_fit_score(reg[i],listreg[i],'Boston',
                                    x_train,x_test,
                                    y_train,y_test)[:2])
[[y_train101,y_test101],[y_train102,y_test102],[y_train103,y_test103],
 [y_train104,y_test104],[y_train105,y_test105],[y_train106,y_test106],
 [y_train107,y_test107],[y_train108,y_test108],[y_train109,y_test109],
 [y_train110,y_test110],[y_train111,y_test111],[y_train112,y_test112],
 [y_train113,y_test113],[y_train114,y_test114],[y_train115,y_test115],
 [y_train116,y_test116],[y_train117,y_test117]]=yreg

df_regressor_results=get_regressor_results()
df_regressor_results.to_csv('regressor_results.csv')
df_regressor_results[df_list].sort_values('r2_test',ascending=False)

pl.figure(figsize=(12,6)); n=30; x=range(n)
pl.scatter(x,y_test[:n],marker='*',s=100,
           color='black',label='Real data')
pl.plot(x,y_test116[:n],lw=2,label='Gradient Boosting')
pl.plot(x,y_test117[:n],lw=2,label='Random Forest')
pl.plot(x,y_test114[:n],lw=2,label='Bagging')
pl.plot(x,y_test115[:n],lw=2,label='Ada Boost')
pl.plot(x,y_test113[:n],lw=2,label='ExtraTree')
pl.xlabel('Observations'); pl.ylabel('Targets')
pl.title('Regressors. Test Results. Boston')
pl.legend(loc=2,fontsize=10); pl.show()

"""## ✒️  Step 5. Neural Networks R"""

import warnings; warnings.filterwarnings('ignore')
from IPython import display
import rpy2.robjects as ro,pylab as pl,pandas as pd
from rpy2.robjects.packages import importr
grdevices=importr('grDevices')
grdevices.png(file="Rpy2.png",width=1000,height=600)
ro.r('library("MASS"); library("nnet"); '+\
     'data(Boston); n<-dim(Boston)[1]')
ro.r('model<-nnet(as.matrix(Boston[1:430,-14]),'+\
     'as.matrix(Boston[1:430,14]),'+\
     'size=52,trace=F,maxit=10^3,linout=T,decay=.1^5); '+\
     'predictions<-predict(model,'+\
     'as.matrix(Boston[431:n,-14]),type="raw")')
ro.r('plot(as.matrix(Boston[431:n,14]),col="black",type="o",'+\
     'xlab="",ylab="",yaxt="n"); par(new=T); '+\
     'plot(predictions,col="#36ff36",type="o",'+\
     'cex=1.3,ylab="Targets & Predictions"); grid();')   
grdevices.dev_off()
display.Image('/content/Rpy2.png')

"""```
%%r
library('MASS'); library('nnet')
data(Boston); n<-dim(Boston)[1];
svg(filename="Rplots.svg",width=10,height=6,
    pointsize=12,onefile=T,family="times",bg="white",
    antialias=c("default","none","gray","subpixel"))
model<-nnet(as.matrix(Boston[1:430,-14]),
            as.matrix(Boston[1:430,14]),
            size=65,trace=F,maxit=10^3,
            linout=T,decay=.1^5)
predictions<-predict(model,as.matrix(Boston[431:n,-14]),
                     type="raw")
plot(as.matrix(Boston[431:n,14]),col="black",type="o",
     xlab='',ylab='',yaxt='n'); par(new=T)
plot(predictions,col="#ff3636",type="o",
     cex=1.3,ylab='Targets & Predictions')
grid(); dev.off()
```

## ✒️  Addition. Combine R & Python
"""

import warnings as wr; wr.filterwarnings('ignore')
from sklearn import datasets
from IPython import display
import rpy2.robjects as ro,pylab as pl,pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter as lc
from rpy2.robjects import r,pandas2ri
pandas2ri.activate()
base=importr('base'); grdevices=importr('grDevices')
bd=datasets.load_boston()
bd=pd.DataFrame(bd.data,columns=bd.feature_names)
#the 1th method
bd[['PTRATIO','LSTAT','RAD']]\
.plot(kind='line',figsize=(10,4)); pl.show()
with lc(ro.default_converter+pandas2ri.converter):
    print(base.summary(bd))

#the 2nd method
rbd=pandas2ri.py2ri(bd)
utils=importr('utils')
utils.write_table(rbd,file='rbd.csv',
                  sep=",",row_names=False)
print(base.summary(rbd))
grdevices=importr('grDevices')
grdevices.png(file="Rpy2.png",width=600,height=500)
ro.r('rbd<-read.csv("rbd.csv")')
ro.r('matplot(c(1:506),rbd[,c(9,11,13)],type="l")')
ro.r('grid()')
grdevices.dev_off()
display.Image("/content/Rpy2.png")

ll='/home/sc_work/.sage/local/lib/r3.6.2/site-packages/'
lp='https://cran.r-project.org/'+\
   'bin/macosx/el-capitan/contrib/3.5/'
fp='ggplot2_3.2.1.tgz'
import urllib,os
from rpy2.robjects.packages import importr
input_file=urllib.request.urlopen(lp+fp)
output_file=open(fp,'wb')
output_file.write(input_file.read())
output_file.close(); input_file.close()
ggplot2=importr('ggplot2',lib_loc='/content/')