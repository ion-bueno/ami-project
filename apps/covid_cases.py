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


from app import app
from apps.footer import footer

matplotlib.use('agg')

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader
from loader.results_loader import ResultsLoader

from apps.mpl_to_plotly import get_plotly_figure
from apps.navbar import get_navbar

bl = BingCovidLoader()
#bl.load(True)
#bl.save_all_figures()

rl = ResultsLoader()
rl.load()
ax = rl.get_time_series_cases("EU")
covid_time_series = get_plotly_figure(ax, False)

# Covid Worldmap
covid_infos = ['cases', 'case rate', 'case change', 'deaths', 'death rate', 'death change', 'recovered', 'recovered rate', 'recovered change']

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

div_width = '768px'
bottom_margin = '50px'
right_margin = '40px'

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

navbar = get_navbar("Covid-19 Cases", "/covid_cases")

countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]

layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    navbar,
    html.Br(),
    html.H1(
        children="Covid-19 cases (Bing Dataset)",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px',
                    'margin-bottom': bottom_margin, 'margin-right': right_margin}, children=[
        html.H2(
            children='Covid-19 Worldmap',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dbc.FormGroup([
            html.Label('Information Type'),
            dcc.Dropdown(
                id='covid_worldmap-type',
                options=[{'label': i, 'value': i} for i in covid_infos],
                value='cases',
                style={'width': '100%'}
                #labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
            )
        ]),
        html.Img(id='covid_worldmap'),
        html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
            dcc.Markdown(
                """Worlwide maps which show the impact of the Covid-19 pandemic. You can select between infected people (cases), deaths and recoveries. In each category, you can see the total number of cases, the rate (which represents the number of cases per 100k people) and the change (new cases cases in the last day).
                The data used to plot those pictures is obtained from a free access API. It is daily updated with the current data.
                The plots give us an intuition about the current situation of Covid-19 in the whole world and how it is affecting the different countries."""),
        ])
    ]),

    html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px',
                    'margin-bottom': bottom_margin}, children=[
        html.H2(
            children='Time series Covid-19 statistics',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dbc.FormGroup([
            dbc.Label('Country'),
            dcc.Dropdown(
                id='covid_time_series-type',
                options=[{'label': i, 'value': i} for i in countries],
                value='EU',
                style={'width': '100%'}
            ),
        ]),

        html.Div([
            dcc.Graph(id='covid_time_series', figure=covid_time_series)
        ]),
        html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
            dcc.Markdown(
                """Those figures show the Covid-19 development as time series information for each of the 8 most important countries (regarding their CO2 emissions). In particular, confirmed cases, active cases (confirmed minus recovered) and deaths can be seen. Notice that accumulated data is plotted instead of the new cases. Drops in curves can mean a change in the tracking strategy of some countries."""),
        ])
    ]),
    footer
])


# Bing Covid Worldmap
@app.callback(
    Output('covid_worldmap', 'src'),
    [Input('covid_worldmap-type', 'value')])
def update_covid_worldmap_src(info_type):
    image_path = './results/covid/' + info_type + '.png'
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

# Bing Covid Time Series
@app.callback(
    Output('covid_time_series', 'figure'),
    [Input('covid_time_series-type', 'value')])
def update_covid_time_series_graph(country):
    axes = rl.get_time_series_cases(country)
    return get_plotly_figure(axes, False)


@app.server.route('/results/covid/<resource>')
def serve_covid_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


@app.server.route('/datasets/Covid19/<resource>')
def serve_covid_datasets_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)