# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:19:24 2020

@author: e3005132
"""

import pandas as pd
#import matplotlib.pyplot as plt

acc_data = pd.read_csv('../output/ACC.CSV')
#print(acc_data.head())
#print(acc_data.sample(5))
#print(acc_data.shape)
acc_dropedna = acc_data.dropna()
acc_datap = acc_dropedna
#print(acc_dropedna.shape)
#print(acc_dropedna.describe())
#print(acc_dropedna["prevClose"].unique())
