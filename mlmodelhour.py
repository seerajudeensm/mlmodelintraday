# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:09:00 2020

@author: e3005132
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from os import path
from stockList import getStockList
result_dict = {}

def k_neighbor_fn(x_train,y_train):

    model = KNeighborsClassifier(n_neighbors=25,weights='uniform')
    model.fit(x_train,y_train)
    return model

def build_model(classifier_fn,
                name_of_y_col,
                names_of_x_cols,
                dataset,
                test_frac=0.001,stockName  = '',type = '20d',execute = False):
    X=dataset[names_of_x_cols]
    Y=dataset[name_of_y_col]
    
    if (execute):
        model = classifier_fn(X,Y)
        if (type=='20d'):
            day_dfex = pd.read_csv(r'outputdayex/'+stockName+'.CSV')
        elif (type=='15m'):
            day_dfex = pd.read_csv(r'outputfifex/'+stockName+'.CSV')
        else:
            day_dfex = pd.read_csv(r'outputex/'+stockName+'.CSV')
        features = list(day_dfex.columns)
        x_pred = day_dfex[features]
        y_pred = model.predict(x_pred)
        x_test = x_pred
        y_test = y_pred
#        print(stockName)
#        print(y_pred)
#        print(x_pred)
        
    else:
        x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=test_frac)
        model = classifier_fn(x_train,y_train)
        y_pred = model.predict(x_test)

    if (1 in y_pred):
        print(stockName,name_of_y_col)
        print(y_pred)
        print(y_test)
        print(x_test)

    return 

def tuneHyperParam():
    #stocksList=['ACC','ADANIENT']
    #25/5/3
    #25/5  25 is no of occurences divided by 5 is min oocurance in csv and /3 is n_neighbour
#    total=0
    #for stockName in stocksList:
    
    #    day_df = pd.read_csv(r'../outputfifteen/'+stockName+'.CSV')
    #    count = day_df['sharename'].loc[day_df['abovexp']==1].count()
    #    if (count>=6):
    #        total+=1
    #    count = day_df['sharename'].loc[day_df['belowxp']==1].count()
    #    if (count>=6):
    #        total+=1
    #    
    #print("total is",total)  
    return


def process(type = '20d',execute=False):
    
    stocksList=['ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','AUROPHARMA','BALKRISIND','BATAINDIA','BERGEPAINT','BEL','BHARATFORG','BPCL','BHARTIARTL','INFRATEL','BHEL','BIOCON','BOSCHLTD','BRITANNIA','CADILAHC','CENTURYTEX','CESC','CIPLA','COALINDIA','COLPAL','CONCOR','CUMMINSIND','DABUR','DIVISLAB','DLF','DRREDDY','EICHERMOT','ESCORTS','EXIDEIND','GAIL','GLENMARK','GMRINFRA','GODREJCP','GRASIM','HAVELLS','HCLTECH','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','IOC','IGL','INFY','INDIGO','ITC','JINDALSTEL','JSWSTEEL','JUBLFOOD','JUSTDIAL','L&TFH','LT','LUPIN','MGL','M&M','MARICO','MARUTI','MFSL','MINDTREE','MOTHERSUMI','MRF','NATIONALUM','NCC','NESTLEIND','NIITTECH','NMDC','NTPC','ONGC','OIL','PAGEIND','PETRONET','PIDILITIND','PEL','PFC','POWERGRID','RELIANCE','RECLTD','SHREECEM','SIEMENS','SRF','SBIN','SAIL','SUNPHARMA','SUNTV','TATACHEM','TCS','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','TVSMOTOR','ULTRACEMCO','UBL','UPL','VEDL','VOLTAS','WIPRO','ZEEL']
    stocksList = getStockList()
    for stockName in stocksList:
#        print("processing...",stockName)
        if (type=='20d'):
            
            if path.exists(r'../outputday/'+stockName+'.CSV'):
                day_df = pd.read_csv(r'../outputday/'+stockName+'.CSV')
                features = list(day_df.columns[6:])
                mincount = 15
                toCheckValue = day_df.columns[4]
#                print(toCheckValue )
        elif (type=='30m'):
            day_df = pd.read_csv(r'../output/'+stockName+'.CSV')
            features = list(day_df.columns[8:])
            mincount = 5
        elif (type=='15m'):
            day_df = pd.read_csv(r'../outputfifteen/'+stockName+'.CSV')
            features = list(day_df.columns[8:])
            mincount = 5


        day_df = day_df.dropna()
#        features = list(day_df.columns[8:])
    #    print("Processing ...",stockName)
#        print(day_df.head())
        count = day_df['sharename'].loc[day_df['abovexp']==1].count()
        count0 = day_df['sharename'].loc[day_df['abovexp']==0].count()
        totalRecords = count + count0
#        print(count)
        
        if ((count>=mincount) and (day_df[toCheckValue][0]>=1) and (totalRecords > 170)):
#            print(1)
            result_dict['abovexp - kneighbor'] = build_model(k_neighbor_fn,
                                                           'abovexp',
                                                           features,
                                                           day_df,
                                                           stockName =stockName,
                                                           execute = execute
                                                           )
        if (type!='20d'):
            count = day_df['sharename'].loc[day_df['belowxp']==1].count()
            if (count>=mincount):
                result_dict['belowxp - kneighbor'] = build_model(k_neighbor_fn,
                                                               'belowxp',
                                                               features,
                                                               day_df,
                                                               stockName =stockName ,
                                                               execute=execute
                                                               )
    return
#process()
process(execute = True)
