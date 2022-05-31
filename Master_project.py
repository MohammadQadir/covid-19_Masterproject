# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 16:48:59 2022

@author: mujta
"""
#Importing all the necessary libraries/Packages

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

#Importing Bankruptdata 
BankruptData = pd.read_csv('Bankruptdata.csv', sep = ',', encoding=('utf-8'),)

#Creating graph for the data
fig = px.area(BankruptData, x="time", y="Total number of bankruptcies", 
              width = 600, height = 120)
fig.update_traces(line_color='#3498DB', line_width=2)

#Importing Unemployment Data
UnemploymentData = pd.read_csv('Unemploymentdata.csv', sep = ',', encoding=('utf-8'),)

#Creating graph for the data
fig1 = px.area(UnemploymentData, x="time", y="unemployment", 
               width = 600, height = 120)
fig1.update_traces(line_color='#1ABC9C', line_width=2)

#Importing GDP Data 
GDPData = pd.read_csv('BNPdata.csv', sep = ',', encoding = ('utf-8'),)

#Creating graph for the data
fig2 = px.line(GDPData, x ='time', y = 'BNP' ,width = 600, height = 120,
               range_y = [0,660] )
fig2.update_traces(line_color='#2ECC71', line_width=2)

#Importing Data regarding decisions/Events 
EventsData = pd.read_csv('Decision_Event_data.csv', sep = ',', encoding = ('utf-8'),)

#Creating graph for the data
fig3 = px.scatter(EventsData, x = 'Date', y = 'Number', size = 'occurance',
                  hover_name = 'Event', title = 'Decisions/Events',)

#Updating the layout for the graph
fig3.update_xaxes(tickfont_size=8)
fig3.update_yaxes(visible = False)
fig3.update_layout(
        width = 600,
        height = 129,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(
            size=8,
        ))

#Importing compensation data 
compensationData = pd.read_csv('compensationdata.csv', sep = ',', encoding = ('utf-8'),)

#Preparing the Data
y = compensationData['Industry']
x1 = compensationData['Number of companies who used salarycompensation']
x2 = compensationData['Number of companies who used compensation'] *-1
z = compensationData['time']

#Creating instance of the figure
fig4 = go.Figure()

#Adding Salarycompensation data to the figure
fig4.add_trace(go.Bar(y = y, x = x1, name = 'Salarycompensation',
                     orientation = 'h', hovertext = z, 
                     marker=dict(color = '#A04000')))

#Adding compensation data to the figure
fig4.add_trace(go.Bar(y =y, x = x2, name = 'Compensation',
                      orientation = 'h', hovertemplate = '%{customdata}', 
                      customdata = compensationData['Number of companies who used compensation'],
                      marker=dict(color = '#F7DC6F')))

#Updating the layout for the graph
fig4.update_xaxes(tickfont_size=10)
fig4.update_yaxes(tickfont_size= 10)
fig4.update_layout(
     legend=dict(font=dict(size= 10)),
     barmode = 'relative',
     bargap = 0.0,
     bargroupgap = 0,
     width = 600,
     height = 230,
     margin = dict(l=0, r=0, t=0, b=0),
     xaxis = dict(
         tickvals = [-12000,-10000,-8000,-6000,-4000,-2000,0,2000,4000,6000,8000,10000,12000],
         ticktext = ['12k','10k','8k','6k','4k','2k','0','2k','4k','6k','8k','10k','12k'],
         title = 'Pyramidchart showing Total number of companies who used compensation',
         title_font_size = 10
     )   
)

#Getting the traces from each graph created above and store them in an array
fig_traces = []
fig1_traces = []
fig2_traces = []

for trace in range(len(fig["data"])):
    fig_traces.append(fig["data"][trace])
for trace in range(len(fig1["data"])):
    fig1_traces.append(fig1["data"][trace])
for trace in range(len(fig2["data"])):
    fig2_traces.append(fig2["data"][trace])

#Creating a 3x1 subplot
this_figure = sp.make_subplots(rows=3, cols=1, shared_xaxes = True) 

#Adding the traces to the proper plot within the subplot
for traces in fig_traces:
    this_figure.append_trace(traces, row=1, col=1)
for traces in fig1_traces:
    this_figure.append_trace(traces, row=2, col=1)
for traces in fig2_traces:
    this_figure.append_trace(traces, row=3, col=1)
 
#Updating the layout for the subplot
this_figure.update_xaxes(tickfont_size=8)
this_figure.update_yaxes(tickfont_size= 8)
this_figure.update_layout(
    hovermode = "x unified",
    margin=dict(l=0, r=0, t=0, b=0), width = 600, height = 300,
    font=dict(
        size=8,
    ))

#Importing Stockmarket data, and preparing the data
StockData = pd.read_csv('Stockdata.csv', sep = ',', encoding= ('utf-8'),)
types = StockData['Industry_type'].unique()
type_options=[{'value':'All Industry Types', 'label': 'All Industry Types'}]
type_options.extend([{'value':i,'label':i} for i in types])

#Creating the Application
app = dash.Dash()


app.layout = html.Div([
    html.H1(children="Dashboard of Covid-19 Pandemic in Denmark",
            style={'textAlign': 'center', 'fontFamily': 'Roboto, sans-serif',}),
    
    html.Div([
        html.Div([
            dcc.Graph(
            id = 'Eventplot',
            figure = fig3,
            ),
            dcc.Graph(
            id = 'subplots',
            figure = this_figure,
            config={
                'displayModeBar': False,
                'watermark' : False,
                },
            ),
            dcc.Graph(
            id = 'Stockchart',
            config={
                'displayModeBar': False,
                'watermark' : False,
                },
            ),
                      
        ], style={'width': '50%', 'display': 'inline-block','verticalAlign': 'top', "margin": "-2px"}),
        
        html.Div([
            dcc.Dropdown(
                id='Industry_types',
                options=type_options,
                value=['All Industry Types'],
                multi = True,
                style={'width':'100%', 'display':'inline-block'}
            ),
            dcc.Graph(
                id = 'compensationchart',
                figure = fig4
            ),
            dcc.Graph(
                id = 'piechart',
                
            ),
            
        ], style={'width': '50%', 'display': 'inline-block','verticalAlign': 'top', "margin": "-2px"}),  
    
          
    
    ], style = {'width': '1320px', 'height': '1000px'}),
 
      
])    

#Connecting the Dropdown values to the linechart
@app.callback(
    Output(component_id='Stockchart', component_property='figure'),
    Input(component_id='Industry_types', component_property='value'),
)
def update_Stockchart(Industry_types):
    mydata = StockData
    print(Industry_types)
        
    mydata = StockData[StockData['Industry_type'].isin(Industry_types)]
    
    fig5 = px.line(mydata, x = 'Date', y = 'Stock_price', color = 'Industry_type')
    fig5.update_xaxes(tickfont_size=8)
    fig5.update_yaxes(tickfont_size= 8)
    fig5.update_layout(title_font_size = 8,margin=dict(l=0, r=0, t=0, b=0), width = 600, height = 140, yaxis_title = None,
                       font=dict(size=8),showlegend = False,
                       )
    
    return fig5

#Connecting the Dropdown values to the piechart
@app.callback(
    Output(component_id='piechart', component_property='figure'),
    Input(component_id='Industry_types', component_property='value'),
)
def update_piechart(Industry_types):
    
    mydata = StockData
    print(Industry_types)
    mydata = StockData[StockData['Industry_type'] != "All Industry Types"]
    if len(Industry_types) == 1 and Industry_types[0] == "All Industry Types":
        pass
    else:
        mydata = mydata[mydata['Industry_type'].isin(Industry_types)]
    mydata.sort_values(by=['Industry_type'])
    
    names = mydata['Industry_type']

    fig6 = px.pie(mydata, values = 'Stock_price', names = names)
    fig6.update_layout(
        margin = dict(l=0, r=0, t=0, b=0),
        width = 600, height = 290,
        )
       
    return fig6

if __name__ == '__main__':
    app.run_server(port=8080)