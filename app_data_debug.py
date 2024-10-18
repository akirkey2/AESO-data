#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:12:44 2024

@author: aaronkirkey
"""

#%% Environment setup - General package use
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

#%% Data loading from AESO database ()

file = 'Gen Chart_Full Data_data.csv'
raw_data = pd.read_csv(file)
df = raw_data.copy()

df['Date - MST'] = pd.to_datetime(df['Date - MST'],format='%m/%d/%Y %I:%M:%S %p')
df = df.drop(['Date', 'Hourly Profile', 'Date (MPT)'],axis=1)
df = df.rename(columns={'Date - MST':'Datetime'})

#%% Dataframe restricting to date

output_date = '2024-06-01'
start_date = '2024-06-01' #Format: %Y/%m/%d
end_date = '2024-06-02' #Stand-in date for a callback

df1 = df[df['Datetime'].dt.date == pd.to_datetime(output_date).date()]
# df_temp2 = df[(df['Datetime'] >= start_date) & (df['Datetime'] < end_date)]
df1 = df1.sort_values(['Fuel Type','Datetime'])
#%% Creating a summary table

df_temp = df1.copy()
df_temp2 = pd.DataFrame()
df_gen_table = pd.DataFrame()
df_temp = df_temp.set_index(['Datetime'])

for i in df_temp['Fuel Type'].unique():
    print(i)
    df_temp2 = df_temp.loc[df_temp['Fuel Type'] == i]
    df_gen_table[i] = df_temp2['Total Generation']
df_gen_table['Total'] = df_gen_table.iloc[:,:].sum(axis=1)
df_gen_table = df_gen_table.round(decimals = 0)
df_gen_table['Gas'] = df_gen_table[['Combined Cycle','Gas Fired Steam','Simple Cycle','Cogeneration']].sum(axis=1)
df_gen_table = df_gen_table.drop(columns =['Combined Cycle','Gas Fired Steam','Simple Cycle','Cogeneration'])
df_gen_table =df_gen_table[['Coal','Gas', 'Dual Fuel',
       'Hydro', 'Solar', 'Storage',
       'Wind','Other', 'Total']]
    
#%%
df_temp_2[i] = df_temp['Total Generation']
df_temp.index = pd.to_datetime(df_temp.index)
df_temp_2 = df_temp_2.reset_index()
df_temp_2 = df_temp_2.round(decimals = 0)
df_temp_2['TOTAL'] = df_temp_2[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
       'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)



#%% Function to create the table summarizing generation by source by %, by hour.

df_temp = df_transform()
df1percent = pd.DataFrame()
df1percent['Datetime'] = df_temp['Datetime']

for i in df_temp.columns[1:9]:
    df1percent[f'{i}'] = (df_temp[f'{i}'] / df_temp['TOTAL'])*100
    
df1percent['TOTAL'] = df1percent[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
       'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
df1percent['RENEWABLE'] = df1percent[['WIND','HYDRO','SOLAR','ENERGY STORAGE']].sum(axis=1)
df1percent['FOSSIL FUEL'] = df1percent[['COAL','GAS','DUAL FUEL']].sum(axis=1)
df1percent = df1percent.round(decimals = 2)


#%%
dft = df.loc[(df['Date (MST)'].str.contains('2024-0'))]
df_temp_2 = pd.DataFrame()

for i in df['Fuel Type'].unique():
    df_temp = dft.loc[(dft['Fuel Type'].str.contains(i))] 
    df_temp = df_temp.groupby(['Date (MST)'])[['Date (MST)','Volume']].sum()
    df_temp_2[i] = df_temp["Volume"]
    df_temp.index = pd.to_datetime(df_temp.index)
df_temp_2 = df_temp_2.reset_index()
df_temp_2 = df_temp_2.round(decimals = 0)
df_temp_2['TOTAL'] = df_temp_2[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
       'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
df_temp_2 = df_temp_2[['Date (MST)','COAL','GAS','DUAL FUEL','HYDRO','SOLAR','WIND','ENERGY STORAGE','OTHER','TOTAL']]
df_temp = df_temp_2
df1p = pd.DataFrame()
df1p['Date (MST)'] = df_temp['Date (MST)']

for i in df_temp.columns[1:9]:
    df1p[f'{i}'] = (df_temp[f'{i}'] / df_temp['TOTAL'])*100
df1p['TOTAL'] = df1p[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
       'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
df1p['RENEWABLE'] = df1p[['WIND','HYDRO','SOLAR','ENERGY STORAGE']].sum(axis=1)
df1p['FOSSIL FUEL'] = df1p[['COAL','GAS','DUAL FUEL']].sum(axis=1)
df1p = df1p.round(decimals = 1)
px.line(df1p,x='Date (MST)',y=['RENEWABLE','FOSSIL FUEL'])
