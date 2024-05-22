#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:38:59 2024

@author: aaronkirkey
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
#file_path = 'C:\\Users\\Aaron Kirkey\\Documents\\GitHub\\AESO-data\\CSD Generation (Hourly) - 2024-01.csv'
file_path = '/home/aaronkirkey/GitRepositories/AESO-data/CSD Generation (Hourly) - 2024-01.csv'
df = pd.read_csv(file_path)
#%%
substr = '2024-01-0'
dftw  = df.loc[(df['Date (MST)'].str.contains(substr))]
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
# plt.show()
df1 = df_temp_2
df1['T2'] = dftotal['Volume']
df1 = df1.reset_index()
df1 = df1.round(decimals = 0)
df1['TOTAL'] = df1[['OTHER', 'WIND', 'GAS', 'HYDRO', 'SOLAR',
       'ENERGY STORAGE', 'COAL', 'DUAL FUEL']].sum(axis=1)
#%% Make the columns that represent the percent contribution to total!!! 
df1
#%%  Dash stuff
app = Dash()
app.title = 'AESO Energy Dash'
app.layout = [html.Div(children=f'AESO Generation Data on: {substr}'),
              dash_table.DataTable(data=df1.iloc[:,0:11].to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
              dash_table.DataTable(data=df1..iloc[:,11:]to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
              dcc.Graph(figure=px.area(dftw, x="Date (MST)", y="Volume", color="Fuel Type", line_group='Asset Name'),
                        style={'width': '180vh', 'height': '90vh'})
              # dcc.Graph(figure=)
              ]

if __name__ == '__main__':
    app.run(debug=True)