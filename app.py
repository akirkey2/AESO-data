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
import dash_bootstrap_components as dbc
import app_data
S
pio.renderers.default='browser'
mpl.rcParams.update(mpl.rcParamsDefault)
plt.rc('axes', axisbelow=True)
mpl.interactive(True)
mpl.rcParams['lines.markersize'] = 5


#%%  Dash stuff
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])
app.title = 'AESO Energy Dash'
app.layout = html.Div([html.Div(children=f'AESO Generation Data on: {app_data.date_range}'),
              # dash_table.DataTable(data=df1.iloc[:,0:11].to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
              # html.Div(children=f'% Contribution to total grid supply on: {substr}'),
              # dash_table.DataTable(data=df1p.to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
              dcc.Graph(figure=px.area(app_data.df_date_restrict(), x="Date (MST)", y="Volume", color="Fuel Type", line_group='Asset Name'),style={'width': '180vh', 'height': '90vh'}),
              #dcc.Graph(figure=px.line(df1pm,x='Date (MST)',y='Percent',color='Fuel Type'))
              ])

if __name__ == '__main__':S
    app.run(debug=True)