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
from apps.navbar import get_navbar
from apps.footer import footer

matplotlib.use('agg')


from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

bottom_margin = '50px'

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

navbar = get_navbar("Model pipeline description", "/model_pipeline")

layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    navbar,
    html.Br(),
    html.H1(
        children="Model pipeline description",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(style={'backgroundColor': colors['background'], 'width': '100%', 'height': '80vh', 'float': 'left', 'margin': '0px', 'margin-bottom': bottom_margin}, children=[
        html.Iframe(id='model_pipeline', src='static/model_pipeline_description.pdf', width="100%", height="100%",
                    style={
                        'margin': '0px',
                        'border': '0',
                        'padding': '0px',
                        'frameborder': '0',
                        'overflow': 'False',
                        'border-width': '0px'
                    }
        )
    ]),
    footer
])


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)