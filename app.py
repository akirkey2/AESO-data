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
from datetime import date
pio.renderers.default='browser'



#%%  Dash stuff
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])
app.title = 'AESO Energy Dash'
app.layout = html.Div(
    [html.Div(children=f'AESO Generation Data on: {app_data.date_range}'),
    dash_table.DataTable(data=app_data.df_transform().to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
    html.Div(children=f'% Contribution to total grid supply on: {app_data.date_range}'),
    dash_table.DataTable(data=app_data.df_percent().to_dict('records'), page_size=25,css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],),
    dcc.Graph(figure=px.area(app_data.df_date_restrict(), x="Date (MST)", y="Volume", color="Fuel Type", line_group='Asset Name'),style={'width': '180vh', 'height': '90vh'}),
    dcc.Graph(figure=px.line(app_data.df_percent(),x='Date (MST)',y=['RENEWABLE','FOSSIL FUEL']))
              ])
"""
[dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2024, 1, 1),
        max_date_allowed=date(2024, 1, 31),
        initial_visible_month=date(2024, 1, 1),
        date=date(2024, 1, 1)),
    html.Div(id='output-container-date-picker-single')],

@callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string"""


if __name__ == '__main__':
    app.run(debug=True)
    