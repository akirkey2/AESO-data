# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 09:39:12 2024

@author: Aaron Kirkey
"""

#%% Environment setup
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
import glob
import sys
from matplotlib import cm
import pathlib
import os
from sklearn import preprocessing
mpl.rcParams.update(mpl.rcParamsDefault)
plt.rc('axes', axisbelow=True)
mpl.interactive(True)
mpl.rcParams['lines.markersize'] = 5

#https://edmontonsun.com/opinion/columnists/gunter-so-called-green-energy-cant-meet-demands-of-today-or-the-foreseeable-future
#%% Dataframe setup
df = pd.read_csv('CSD Generation (Hourly) - 2024-01.csv')
#%%
print(df['Fuel Type'].unique())
#%%
dftw  = df.loc[(df['Date (MST)'].str.contains('2024-01'))]
#%%
for i in df['Fuel Type'].unique():
    print(i)
    df_temp = dftw.loc[(df['Fuel Type'].str.contains(i))] 
    df_temp = df_temp.groupby(['Date (MST)'])[['Date (MST)','Volume']].sum()
    df_temp['Time'] = df_temp.index.str.slice(11,16)
    df_temp.index = pd.to_datetime(df_temp.index)
    plt.plot(df_temp.index,df_temp['Volume'])
    plt.title('Hourly Generation on AESO on 2024-01-01')