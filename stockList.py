# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 16:02:51 2019

@author: e3005132
"""
import DBCommand as dba
#from datetime import timedelta

def getRecord(sqlstmt='',whereQueryInList='',selectCount=1):
    dbc = dba.DBCommand()
    
    output = dbc.selectDBSQL(sqlstmt,whereQueryInList,selectCount)
#    print(output)
    return output


def getStockList(type='nonintraday'):
    myList = []
    if (type=='nonintraday'):
    
        sqlstmt = "select distinct stocksymbol from stockhist"
        output = getRecord(sqlstmt,[],10000)
    
        #print(output)
        for data in output:
            #    print(data[0])
            if data[0][-3:]==".NS":
                myList.append(data[0][:-3])
        myList.remove('GAYAHWS')
        myList.remove('SUJANAUNI')
        myList.remove('SMPL')
    elif(type=='intraday'):
        myList=['ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AMARAJABAT','AMBUJACEM','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','AUROPHARMA','BALKRISIND','BATAINDIA','BERGEPAINT','BEL','BHARATFORG','BPCL','BHARTIARTL','INFRATEL','BHEL','BIOCON','BOSCHLTD','BRITANNIA','CADILAHC','CENTURYTEX','CESC','CIPLA','COALINDIA','COLPAL','CONCOR','CUMMINSIND','DABUR','DIVISLAB','DLF','DRREDDY','EICHERMOT','ESCORTS','EXIDEIND','GAIL','GLENMARK','GMRINFRA','GODREJCP','GRASIM','HAVELLS','HCLTECH','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','IOC','IGL','INFY','INDIGO','ITC','JINDALSTEL','JSWSTEEL','JUBLFOOD','JUSTDIAL','L&TFH','LT','LUPIN','MGL','M&M','MARICO','MARUTI','MFSL','MINDTREE','MOTHERSUMI','MRF','NATIONALUM','NCC','NESTLEIND','NIITTECH','NMDC','NTPC','ONGC','OIL','PAGEIND','PETRONET','PIDILITIND','PEL','PFC','POWERGRID','RELIANCE','RECLTD','SHREECEM','SIEMENS','SRF','SBIN','SAIL','SUNPHARMA','SUNTV','TATACHEM','TCS','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','RAMCOCEM','TITAN','TORNTPHARM','TORNTPOWER','TVSMOTOR','ULTRACEMCO','UBL','UPL','VEDL','VOLTAS','WIPRO','ZEEL']
    else:
        myList = ['PEL']
    myList.sort()
    return myList
    
