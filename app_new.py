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
from dash import Dash, html, dash_table, dcc, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
import app_data_new
import datetime as dt
from datetime import date
from datetime import datetime
pio.renderers.default='browser'

#To-do: Add titles to mygraphs!!! Make graph that shows total gen every day for a month or so.

#%%  Dash stuff
# datte = '2024-01-06' # Placeholder value
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])
app.title = 'AESO Energy Dash'
app.layout = html.Div([
    html.Div([html.H1(children='AESO Energy Dash',style={'textAlign': 'center', 'fontSize':48}),
    html.Br(),
    html.Div(children=
             """*Disclaimer: This web-dash and contents are in no way 
             affiliated with the AESO and serves only as a personal project to 
             improve my data science and data viz skillset with respect to grid
             data. For questions, comments or improvement ideas, please contact
             me at: akirkey2@gmail.com with the subject line 'AESO dash project'.
             Thank you for your interest!"""),
    html.Br(),
    html.Br(),
    html.Div(children='Show AESO Generation Data from: ',style={'fontSize': 20}),
    dcc.DatePickerSingle(  # This is a drop-down calendar that updates the elements on the page
            id='date-picker-single',
            min_date_allowed=date(2024, 1, 1),
            max_date_allowed=date(2024, 6, 30),
            initial_visible_month=date(2024, 1, 1),
            date=date(2024, 1, 1),
            display_format='Y-M-D'),
    html.Br(),
    html.Br(),
    html.Div(children = 'Date chosen: ',style={'fontSize': 20}), # Visual feedback on page displaying date
    dcc.Markdown(id='date_display',children = '')]),
    html.Br(),
    
    # This Div contains a table and a title and is left adjusted beside following Div
    html.Div(children=[
        html.Div(children='Contribution on the grid (MW)',style={'fontSize': 22,'font-weight':'bold','textAlign':'center'}),
        dash_table.DataTable(
                            id='summary_table', 
                            page_size=24,
                            css=[{'selector': 'table', 'rule': 'width: 800px; height: 300px; margin: 0 auto; overflow: auto;'},
                                 {'selector': 'td', 'rule': 'font-size: 12px;'},  # Adjusting font size for table cells
                                 {'selector': 'th', 'rule': 'font-size: 12px; font-weight: bold;'}
                                 ]
                            )
                        ],
                        style={'display':'inline-block','width': '49%', 'verticalAlign': 'top', 'textAlign': 'center'}),


    # This Div contains a table and a title and is right adjusted beside previous Div
    html.Div(children=[
        html.Div(children='% Contribution on the grid',style={'fontSize': 22,'font-weight':'bold','textAlign':'center'}),
        dash_table.DataTable(
                            id='percent_table',
                            page_size=24,
                            css=[{'selector': 'table', 'rule': 'width: 800px; height: 300px; margin: 0 auto; overflow: auto;'},
                                 {'selector': 'td', 'rule': 'font-size: 12px;'},  # Adjusting font size for table cells
                                 {'selector': 'th', 'rule': 'font-size: 12px; font-weight: bold;'}
                                 ]
                            )
                        ],
                        style={'display':'inline-block','width': '49%', 'verticalAlign': 'top', 'textAlign': 'center'}),
    
    html.Br(),
    html.Br(),
    
    #This Div is a graph with title, left adjusted beside the following Div
    html.Div(children=[
        html.Div(children='Hourly generation on AESO by asset & fuel type',style={'fontSize': 22,'font-weight':'bold','textAlign':'center'}),
        html.Div(dcc.Graph(id='asset_gen'),
                         style={'display': 'inline-block', 'width': '100%', 'textAlign': 'center'})
                        ],
                        style={'display':'inline-block','width': '50%', 'verticalAlign': 'top', 'textAlign': 'center'}),
    
    #This Div is a graph with title, right adjusted beside the previous Div
    html.Div(children=[
        html.Div(children='% Generation from Renewable vs. Fossil Fuel sources',style={'fontSize': 22,'font-weight':'bold','textAlign':'center'}),
        html.Div(dcc.Graph(id='clean_fossil_gen'),
                 style={'display': 'inline-block', 'width': '100%', 'textAlign': 'center'})
                        ],
                        style={'display':'inline-block','width': '50%', 'verticalAlign': 'top', 'textAlign': 'center'}),
              ])



#This callback updates the elements on the page to reflect the date chosen by the user
@callback(Output(component_id='date_display',component_property ='children'),
           Output('summary_table', component_property='data'),
           Output('percent_table','data'),
           Output('asset_gen', 'figure'),
           Output('clean_fossil_gen','figure'),

    Input(component_id='date-picker-single', component_property ='date'))


#Calls functions with updated date to make dash reactive to selected date
def update_date(user_selected):    
    print(user_selected) #The function argument comes from the component property of the Input
    summary_data = app_data_new.df_summary(user_selected).to_dict('records')
    percent_data = app_data_new.df_percent(user_selected).to_dict('records')
    asset_gen_fig = px.area(app_data_new.df_date_restrict(user_selected), x='Date (MST)', y="Volume", color="Fuel Type")
    clean_ff_fig = px.line(app_data_new.df_percent(user_selected),x='Date (MST)',y=['RENEWABLE','FOSSIL FUEL'])
    return user_selected, summary_data, percent_data, asset_gen_fig, clean_ff_fig # The returned object is assigned to the component property of the Output

if __name__ == '__main__':
    app.run_server(port=2222)
    