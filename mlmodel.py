# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:09:00 2020

@author: e3005132
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier


result_dict = {}

def summarize_classification(y_test,y_pred):

    acc = accuracy_score(y_test,y_pred,normalize=True)
    num_acc = accuracy_score(y_test,y_pred,normalize=False)
    prec = precision_score(y_test,y_pred)
    recall = recall_score(y_test,y_pred)
    
    return {'accuracy':acc,
            'precision':prec,
            'recall':recall,
            'accuracy_count':num_acc}

def linear_svc_fn(x_train,y_train,C=1.0, max_iter=1000,tol=1e-3):
    model = LinearSVC(C=C,max_iter=max_iter,tol=tol, dual=False)
    model.fit(x_train,y_train)
    return model
    
def build_model(classifier_fn,
                name_of_y_col,
                names_of_x_cols,
                dataset,
                test_frac=0.2):
    X=dataset[names_of_x_cols]
    Y=dataset[name_of_y_col]
    
    x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=test_frac)
    model = LinearSVC(C=1.0,max_iter=1000,tol=1e-3, dual=False)
    model.fit(x_train,y_train)
    y_pred = model.predict(x_test)
#    print(y_pred)
    print(y_test)
#    model = classifier_fn(x_train,y_train)
#    y_pred = model.predict(x_test)
#    y_pred_train = model.predict(x_train)
#    print(y_pred,y_test) 
#    return
#    train_summary = summarize_classification(y_train,y_pred_train)
#    test_summary = summarize_classification(y_test,y_pred)
#    
#    pred_results = pd.DataFrame({'y_test':y_test,
#                                 'y_pred':y_pred})
#    model_crosstab = pd.crosstab(pred_results.y_pred,pred_results.y_test)
#    
#    return {'training':train_summary,
#            'test':test_summary,
#            'sonfusion_matrix':model_crosstab}
    

        

day_df = pd.read_csv(r'../output/ACC.CSV')
#print(day_df.head())
features = list(day_df.columns[8:])
print(day_df.columns)
result = 'above7p'
print(result)
X=day_df[features]
Y=day_df['above7p']
#Y=day_df['below7p']
print(X)
print(Y)
x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)
model = LinearSVC(C=1.0,max_iter=1000,tol=1e-3, dual=False)
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
print(y_test,y_pred)
#print(features)

#result_dict['above7p - linearsvc'] = build_model(linear_svc_fn,'above7p',features,day_df)