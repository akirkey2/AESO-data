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
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'
mpl.rcParams.update(mpl.rcParamsDefault)
plt.rc('axes', axisbelow=True)
mpl.interactive(True)
mpl.rcParams['lines.markersize'] = 5

#https://edmontonsun.com/opinion/columnists/gunter-so-called-green-energy-cant-meet-demands-of-today-or-the-foreseeable-future
#%% Dataframe setup
windows_file_path = 'C:\\Users\\Aaron Kirkey\\Documents\\GitHub\\AESO-data\\CSD Generation (Hourly) - 2024-01.csv'
ubuntu_file_path = ''
df = pd.read_csv(windows_file_path)
#%%
dftw  = df.loc[(df['Date (MST)'].str.contains('2024-01-01'))]
dftotal = dftw.groupby(['Date (MST)']).sum()
dftotal.index = pd.to_datetime(dftotal.index)
#%%
lst = []
df_temp_2 = pd.DataFrame()
for i in df['Fuel Type'].unique():
    print(i)
    lst.append(i)
    df_temp = dftw.loc[(df['Fuel Type'].str.contains(i))] 
    df_temp = df_temp.groupby(['Date (MST)'])[['Date (MST)','Volume']].sum()
    df_temp['Time'] = df_temp.index.str.slice(11,16)
    df_temp_2[i] = df_temp["Volume"]
    df_temp.index = pd.to_datetime(df_temp.index)
    plt.plot(df_temp.index,df_temp['Volume'],label = i)
plt.plot(dftotal.index,dftotal['Volume'],label = 'Total', color = 'black')
plt.xticks(rotation = 45)
plt.title('Hourly Generation on AESO Jan 2024')
plt.legend(loc = 1)
plt.show()

#%%
fig = px.area(dftw, x="Date (MST)", y="Volume", color="Fuel Type", line_group='Asset Name')
fig.show()
