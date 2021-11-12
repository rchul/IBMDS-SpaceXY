# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:26:35 2021

@author: rjull
"""
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id = 'site-dropdown', 
                                                      options = [{'label':'All', 'value':'All'},
                                                                 {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                                 {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                                 {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                                 {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}],
                                                      value = 'All',
                                                      placeholder = 'Select a Launch Site Here',
                                                      searchable = True)),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([], id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id = 'payload-slider',
                                                         min = 0,
                                                         max = 10000,
                                                         step = 1000,
                                                         value = [min_payload, max_payload],
                                                         tooltip={"placement": "bottom", "always_visible": True})),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([], id='success-payload-scatter-chart')
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output('success-pie-chart', 'children'), Output('success-payload-scatter-chart', 'children')],
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])

def getPie(dd,sli):
    dfP = spacex_df
    fil = dfP[(dfP['Payload Mass (kg)'] >= sli[0]) & (dfP['Payload Mass (kg)'] <= sli[1])]
    if dd == 'All':
        pie = px.pie(fil,
               values = 'class',
               names = 'Launch Site',
               title = 'Total Success Launches by Site')
        scatter = px.scatter(fil,
                             x = 'Payload Mass (kg)',
                             y = 'class',
                             color = 'Booster Version Category',
                             title = 'Correlation Between Payload and Success for all site')
        return [dcc.Graph(figure=pie), 
                dcc.Graph(figure=scatter)]
    
    else:
        fil2 = fil[fil['Launch Site'] == dd]
        pDf = fil2.groupby(['Launch Site','class']).size().reset_index(name = 'class count')
        pie = px.pie(pDf,
                     values = 'class count',
                     names = 'class',
                     title = f'Total Success Launches for {dd}')
        scatter = px.scatter(fil2,
                             x = 'Payload Mass (kg)',
                             y = 'class',
                             color = 'Booster Version Category',
                             title = f'Correlation between Payload and Success for {dd}')
        return [dcc.Graph(figure=pie), 
                dcc.Graph(figure=scatter)]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()