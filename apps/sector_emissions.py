# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly as py
import plotly.tools as tls
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly import offline
import base64
from flask import Flask
import flask, os
import dash_bootstrap_components as dbc
import time


from app import app
from apps.footer import footer

matplotlib.use('agg')


from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader
from prediction.co2_covid.construction_industry import ConstructionLoader
from prediction.co2_covid.mobility import demo as m_demo
from prediction.co2_covid.mobility import demo_driving as m_demo_driving
from prediction.co2_covid.mobility import demo_transit as m_demo_transit
from loader.other_industry_loader import OtherIndustryLoader
from prediction.co2_covid.power_industry import Power_Indicators
from loader.sector_emissions_loader import co2_demo
from loader.results_loader import ResultsLoader

from apps.mpl_to_plotly import get_plotly_figure
from apps.navbar import get_navbar

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

ml = MobilityLoader()
ml.load()

# Apple
ax, df = ml.apple_demo("driving")
apple = get_plotly_figure(ax, True)

# Google
ax, df = ml.google_demo()
google = get_plotly_figure(ax, True)

# Opensky
ax, df = ml.opensky_demo()
opensky = get_plotly_figure(ax)

# Flightradar
ax, df = ml.flightradar_demo()
flightradar = get_plotly_figure(ax)

gl = GreenhouseLoader()
gl.load()

# Construction Industry
const_loader = ConstructionLoader()
ax = co2_demo("Buildings")
const_em = get_plotly_figure(ax, False)

cur_dir = os.getcwd()
os.chdir("prediction/co2_covid/")
const_loader.load()
ax = const_loader.indicator_demo()[0]
const_ind = get_plotly_figure(ax, False)

ax = const_loader.prediction_demo("EU")
const_pred = get_plotly_figure(ax, False)
os.chdir(cur_dir)

# Mobility Indicators
ax = co2_demo("Transport")
trans_em = get_plotly_figure(ax, False)

ax = m_demo()
mobility_ind = get_plotly_figure(ax, False)

ax = m_demo_driving()
driving_ind_raw = get_plotly_figure(ax[0], False)
driving_ind_ma = get_plotly_figure(ax[1], False)

ax = m_demo_transit()
transit_ind_raw = get_plotly_figure(ax[0], False)
transit_ind_ma = get_plotly_figure(ax[1], False)

# Other industries
ax = co2_demo("Other industrial combustion")
other_em = get_plotly_figure(ax, False)

ol = OtherIndustryLoader()
ol.load()
ax = ol.ww_ax()
other_ind = get_plotly_figure(ax, False) # rises annotation error

# Power industry
ax = co2_demo("Power Industry")
power_em = get_plotly_figure(ax, False)

cur_dir = os.getcwd()
os.chdir('prediction/co2_covid/')
pl = Power_Indicators()
pl.clean_co2()
pl.clean_power_industry()
pl.select_indicator(False) # rises Degrees of freedom <= 0 for slice and divide by zero encountered in true_divide

ax = pl.get_demo("EU")
power_ind = get_plotly_figure(ax, False)

ax = pl.plot_sarima("EU")
power_pred = get_plotly_figure(ax, False)
os.chdir(cur_dir)

rl = ResultsLoader()
rl.load()
bar_plot = rl.get_bar_plot("EU")

pie_plot = rl.get_pie_plot("EU")

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

div_width = '768px'
bottom_margin = '50px'
right_margin = '40px'

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]

navbar = get_navbar("CO2 Emissions by Sector", "/sector_emissions")

layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    navbar,
    html.Br(),
    html.H1(
        children="CO2 Emissions by Sector",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Tabs(style={'margin-bottom': bottom_margin}, children=[
        dcc.Tab(label='Construction Industry', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Construction Industry CO2 Emissions',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='const_em', figure=const_em)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """CO2 emissions of the 8 biggest contributors due to construction sector. Emissions are measured in Megatons.
                        This sector refers to small scale non-industrial stationary combustion."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Indicators',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Information Type'),
                    dbc.RadioItems(
                        id='const_ind-type',
                        options=[
                            {'label': 'Steel price', 'value': 'steel_price'},
                            {'label': 'Concrete price', 'value': 'concrete_price'},
                            {'label': 'Concrete production', 'value': 'concrete_prod'},
                            {'label': 'Construction spending', 'value': 'const_spend'}],
                        value='steel_price',
                        custom=False,
                        inline=True,
                        labelStyle={'margin-right': '12px'},
                    ),
                ]),

                html.Div(
                    dcc.Graph(id='const_ind', figure=const_ind)
                ),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Indicators with montly resolution. They are used to predict the emission taking into account the possible effect of Covid-19. In this sector, the of steel and concrete are used, as well as the concrete production index and construction spending."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
                html.H2(
                    children='CO2 Emission Predictions',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.Label('Country'),
                dcc.Dropdown(
                    id='const_pred-type',
                    options=[{'label': i, 'value': i} for i in countries],
                    value='EU',
                    style={'width': '100%'}
                    # labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
                ),

                html.Div(
                    dcc.Graph(id='const_pred', figure=const_pred)
                ),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Predicted emissions with respect to the observed ones. Observed emissions have annual resolution, whereas predicted ones are monthly. Previous shown indicators provide this change in time resolution. You can select between the 8 biggest contributors of greenhouse gas emissions."""),
                ])
            ])
        ]),
        dcc.Tab(label='Power Industry', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Power Industry CO2 Emissions',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='power_em', figure=power_em)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """CO2 emissions of the 8 biggest contributors by power industry sector. Emissions are measured in Megatons.
                        This sector refers to power and heat generation plants (public & autoproducers)."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Power Industry Indicator',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Label('Country'),
                dcc.Dropdown(
                    id='power_ind-type',
                    options=[{'label': i, 'value': i} for i in countries],
                    value='EU',
                    style={'width': '100%'}
                    # labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
                ),

                html.Div([
                    dcc.Graph(id='power_ind', figure=power_ind)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """It is possible to select between the 8 biggest countries in terms of emissions. In this sector, depending on the country, different indicators are used. If the country is from Europe, 4 indicators are used, whereas if it is not, only 2 are used. All indicators have monthly resolution. In the legend, the name of the country represents the emissions in this sector. In the title, for each case it can be seen which indicator is more correlated with the emissions."""),
                ])
            ]),

            html.Div(
                style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin},
                children=[
                    html.H2(
                        children='CO2 Emission Predictions',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }
                    ),

                    html.Label('Country'),
                    dcc.Dropdown(
                        id='power_pred-type',
                        options=[{'label': i, 'value': i} for i in countries],
                        value='EU',
                        style={'width': '100%'}
                        # labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
                    ),

                    html.Div([
                        dcc.Graph(id='power_pred', figure=power_pred)
                    ]),
                    html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                        dcc.Markdown(
                            """Predicted indicator with respect to the observed one. The predicted one was calculated using a time series prediction from the moment on Covid-19 started, which provides us with the behaviour of the indicators if Covid-19 would not have appeared. The observed indicator represents the indicator taking into account the impact of Covid-19."""),
                    ])
                ])
        ]),
        dcc.Tab(label='Transport Industry', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Transport Industry CO2 Emissions',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='trans_em', figure=trans_em)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """CO2 emissions of the 8 biggest contributors by transport sector. Emissions are measured in Megatons.
                        This sector refers to mobile combustion (road & rail & ship & aviation)"""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin, 'margin-bottom': '50px'}, children=[
                html.H2(
                    children='Mobility Indicator',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='mobility_ind', figure=mobility_ind)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """This indicator for the 8 biggest contributors mainly results from the Apple mobility dataset."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': '1536px', 'float': 'left', 'margin': '20px'}, children=[
                html.H2(
                    children='Apple Mobility Dataset',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Information Type', style={'text-align':'center'}),
                    dbc.RadioItems(
                        id='apple-type',
                        options=[
                            {'label': 'Transit', 'value': 'transit'},
                            {'label': 'Driving', 'value': 'driving'}],
                        value='driving',
                        inline=True,
                        custom=False,
                        labelStyle={'margin-right': '12px'},
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }
                    ),
                ]),

                html.Div(className="row", style={'backgroundColor': colors['background'], 'width': 'auto', 'margin': '20px', 'display': 'inline-block'}, children=[
                    html.Div(className="six columns", children=[
                        dcc.Graph(id='apple', figure=driving_ind_raw)
                    ]),
                    html.Div(className="six columns", children=[dcc.Graph(id='apple_ma', figure=driving_ind_ma)])
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """These plots describe how the transit and the driving have evolved. On the left, this is explained using the change as percentage with respect to the baseline value of 2020-01-13. The graph at the right corresponds to a 7-day moving average of the same data. Five countries are used as example for transit, which you can select or deselect."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'clear':'both', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Google Mobility Dataset',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Information Type'),
                    dcc.Dropdown(
                        id='google-type',
                        options=[
                            {'label': 'Retail and recreation', 'value': 'retail_and_recreation_percent_change_from_baseline'},
                            {'label': 'Grocery and pharmacy', 'value': 'grocery_and_pharmacy_percent_change_from_baseline'},
                            {'label': 'Parks', 'value': 'parks_percent_change_from_baseline'},
                            {'label': 'Transit stations', 'value': 'transit_stations_percent_change_from_baseline'},
                            {'label': 'Workplaces', 'value': 'workplaces_percent_change_from_baseline'},
                            {'label': 'Residential', 'value': 'residential_percent_change_from_baseline'}],
                        value='workplaces_percent_change_from_baseline'
                    ),
                ]),

                html.Div([
                    dcc.Graph(id='google', figure=google)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """These plots show the evolution of different services. The percentage of change is taken with respect to the data stored in 2020-02-15. You can select between different points."""),
                ])

            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': '120px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Opensky Dataset: Flight hours per day',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='opensky', figure=opensky)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Graph which shows the total number of flight hours per day. The period which was studied starts in 2020-01-01."""),
                ])
            ]),
            html.Br(),
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
                html.H2(
                    children='Flightradar Dataset: Number of Flights',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='flightradar', figure=flightradar)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Number of flights per day. The period taken into account starts in 2020-01-01. We distinguish between the total number and commercial flights."""),
                ])
            ]),
        ]),
        dcc.Tab(label='Other Industries', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Other Industries CO2 Emissions',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='other_em', figure=other_em)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """CO2 emissions of the 8 biggest contributors by other industrial combustion. Emissions are measured in Megatons.
                        This sector refers to combustion for industrial manufacturing and fuel production."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
                html.H2(
                    children='Other Industry Indicator',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                html.Div([
                    dcc.Graph(id='other_ind', figure=other_ind)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """For the 8 biggest contributors, the seasonally adjusted steel production index is used as an indicator. This graph shows the normalized indicator. It is used in order to get a seasonality in CO2 emissions."""),
                ])
            ]),
        ]),
        dcc.Tab(label='Sector Overview', children=[
            html.Div(
                style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px',
                       'margin-bottom': bottom_margin, 'margin-right': right_margin}, children=[
                html.H2(
                    children='CO2 Emission Drop per Sector',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    html.Label('Country'),
                    dcc.Dropdown(
                        id='bar-type',
                        options=[{'label': i, 'value': i} for i in countries],
                        value='EU',
                        style={'width': '100%'}
                        # labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
                    )
                ]),
                html.Div([
                    dcc.Graph(id='bar_plot', figure=bar_plot)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """This figure shows the average emission drop in the time interval from January to June 2020 per sector.
                        You can select between the eight countries which contribute the most to CO2 emissions. Changing the country will synchronously also change the country for the pie chart to the right."""),
                ])
            ]),

            html.Div(
                style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px',
                       'margin-bottom': bottom_margin}, children=[
                html.H2(
                    children='CO2 Emissions Shares by Sector',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Country'),
                    dcc.Dropdown(
                        id='pie-type',
                        options=[{'label': i, 'value': i} for i in countries],
                        value='EU',
                        style={'width': '100%'}
                    ),
                ]),

                html.Div([
                    dcc.Graph(id='pie_plot', figure=pie_plot)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """This figure shows how the different sectors contribute to the overall CO2 emissions of a country. The most important eight countries can be selected.
                        Changing the country will synchronously also change the country for the bar plot to the left."""),
                ])
            ]),
        ]),
    ]),
    footer
])

# Apple mobility reports
@app.callback(
    [Output('apple', 'figure'), Output('apple_ma', 'figure')],
    [Input('apple-type', 'value')], prevent_initial_call=True)
def update_apple_graph(info_type):
    if info_type == "driving":
        axes = m_demo_driving()
    else:
        axes = m_demo_transit()
    return [get_plotly_figure(axes[0], False), get_plotly_figure(axes[1], False)]

# Google mobility reports
@app.callback(
    Output('google', 'figure'),
    [Input('google-type', 'value')], prevent_initial_call=True)
def update_google_graph(info_type):
    axes, data = ml.google_demo(information_type=info_type)
    return get_plotly_figure(axes, True)

# Construction indicators
@app.callback(
    Output('const_ind', 'figure'),
    [Input('const_ind-type', 'value')], prevent_initial_call=True)
def update_const_ind_graph(ind_name):
    cur_dir = os.getcwd()
    os.chdir("prediction/co2_covid/")
    axes, data = const_loader.indicator_demo(indicator_name=ind_name)
    os.chdir(cur_dir)
    return get_plotly_figure(axes, False)

@app.callback(
    Output('const_pred', 'figure'),
    [Input('const_pred-type', 'value')], prevent_initial_call=True)
def update_const_pred_graph(country):
    cur_dir = os.getcwd()
    os.chdir("prediction/co2_covid/")
    axes = const_loader.prediction_demo(country)
    os.chdir(cur_dir)
    return get_plotly_figure(axes, False)

@app.callback(
    Output('power_ind', 'figure'),
    [Input('power_ind-type', 'value')], prevent_initial_call=True)
def update_power_ind_graph(country):
    axes = pl.get_demo(country)
    return get_plotly_figure(axes, False)

@app.callback(
    Output('power_pred', 'figure'),
    [Input('power_pred-type', 'value')], prevent_initial_call=True)
def update_power_pred_graph(country):
    cur_dir = os.getcwd()
    os.chdir('prediction/co2_covid/')
    axes = pl.plot_sarima(country)
    os.chdir(cur_dir)
    return get_plotly_figure(axes, False)

@app.callback(
    [Output('bar_plot', 'figure'), Output('pie-type', 'value')],
    [Input('bar-type', 'value')], prevent_initial_call=True)
def update_bar_graph(country):
    return [rl.get_bar_plot(country), country]

@app.callback(
    [Output('pie_plot', 'figure'), Output('bar-type', 'value')],
    [Input('pie-type', 'value')], prevent_initial_call=True)
def update_pie_graph(country):
    return [rl.get_pie_plot(country), country]