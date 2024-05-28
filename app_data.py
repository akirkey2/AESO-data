# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:52:32 2024

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
from dash import Dash, html, dash_table, dcc
import dash
pio.renderers.default='browser'
mpl.rcParams.update(mpl.rcParamsDefault)
plt.rc('axes', axisbelow=True)
mpl.interactive(True)
mpl.rcParams['lines.markersize'] = 5

#%% Dataframe setup
# file_path = 'C:\\Users\\Aaron Kirkey\\Documents\\GitHub\\AESO-data\\CSD Generation (Hourly) - 2024-01.csv'
file_path = 'CSD Generation (Hourly) - 2024-01.csv'
df = pd.read_csv(file_path)
#%%
date_range = '2024-01-0' #This will eventaully be a callback to a calendar on the dash
def df_date_restrict():
    
    df_date_range = df.loc[(df['Date (MST)'].str.contains(date_range))]
    # dftotal = df_date_range.groupby(['Date (MST)']).sum()
    # dftotal.index = pd.to_datetime(dftotal.index)
    return df_date_range #dftotal, 

#%%
def df_transform():

    df_temp_2 = pd.DataFrame()
    
    for i in df['Fuel Type'].unique():
        df_temp = df.loc[(df['Fuel Type'].str.contains(i))] 
        df_temp = df_temp.groupby(['Date (MST)'])[['Date (MST)','Volume']].sum()
        df_temp_2[i] = df_temp["Volume"]
        df_temp.index = pd.to_datetime(df_temp.index)
    df_temp_2 = df_temp_2.reset_index()
    df_temp_2 = df_temp_2.round(decimals = 0)
    df_temp_2['TOTAL'] = df_temp_2[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
           'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
    return df_temp_2
    
#%% Make the columns that represent the percent contribution to total!!!
def df_percent(): 
    
    df_temp = df_transform()
    df1p = pd.DataFrame()
    df1p['Date (MST)'] = df_temp['Date (MST)']
    
    for i in df_temp.columns[1:9]:
        df1p[f'{i}'] = (df_temp[f'{i}'] / df_temp['TOTAL'])*100
    df1p['TOTAL'] = df1p[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
           'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
    df1p['RENEWABLE'] = df1p[['WIND','HYDRO','SOLAR','ENERGY STORAGE']].sum(axis=1)
    df1p['FOSSIL FUEL'] = df1p[['COAL','GAS','DUAL FUEL']].sum(axis=1)
    df1p = df1p.round(decimals = 2)
    return df1p

