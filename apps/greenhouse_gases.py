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

matplotlib.use('agg')


from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader

from apps.mpl_to_plotly import get_plotly_figure
from apps.navbar import get_navbar
from apps.footer import footer


gl = GreenhouseLoader()
gl.load()

# All greenhouse gases
ax = gl.gg_global_ann_increase_demo()[0]
gg = get_plotly_figure(ax, True)
gg.update_layout()

# CO2
ax = gl.co2_global_weekly_demo()[0]
co2 = get_plotly_figure(ax, True)
co2.update_layout(margin=dict(t=60, b=30, l=0, r=0))

# Other greenhouse gases
ax = gl.ch4_country_demo()[0]
divers = get_plotly_figure(ax, True)

# CO2 goals
goals_loader = Co2Goals()
goals_loader.load()
ax = goals_loader.demo()
goals = get_plotly_figure(ax, False)

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

div_width = '768px'
bottom_margin = '50px'
right_margin = '40px'

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

navbar = get_navbar("Greenhouse gas data", "/greenhouse_gases")

layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    navbar,
    html.Br(),
    html.H1(
        children="Greenhouse gas data",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Tabs(style={'margin-bottom': bottom_margin}, children=[
        dcc.Tab(label='CO2 Goals Data', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': 'auto', 'text-align': 'center', 'margin': '20px'}, children=[
                html.Div(style={'width': div_width, 'text-align': 'left', 'display': 'inline-block', 'margin-bottom': bottom_margin}, children=[
                    html.H2(
                        children='CO2 Goals',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }
                    ),

                    dbc.FormGroup([
                        dbc.Label('Plotting Type'),
                        dbc.RadioItems(
                            id='goals-type',
                            options=[
                                {'label': 'Line plot', 'value': 'lines'},
                                {'label': 'Bubble plot', 'value': 'bubbles'}],
                            value='lines',
                            inline=True,
                            custom=False,
                            labelStyle={'margin-right': '12px'}
                        ),
                    ]),

                    dcc.Graph(id='goals', figure=goals),
                    html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                        dcc.Markdown(
                            """These plots show the Paris Climate Agreement greenhouse gas emission reduction goals of the 8 Biggest Contributors.
                            Selecting the option of "lines", we can see how it would be developed a linear reduction per country to reach the estimated goal. By selecting "bubbles", final goals are compared with a straight line which represents the 1.5ºC goal. This means the average temperature on the final date should be as much as 1.5ºC bigger than the initial date (dates depend on the country). If bubbles are above this line, the goal will be fulfilled.
                            These graphs are finally used to compare with our obtained results and to answer the research question."""),
                    ])
                ])
            ]),
        ]),

        dcc.Tab(label='Greenhouse Gas Measurements', children=[
            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='Global Greenhouse Gas Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    html.Label('Information Type'),
                    dbc.RadioItems(
                        id='gg-type',
                        options=[
                            {'label': 'Annual absolute', 'value': 'annual_absolute'},
                            {'label': 'Annual increase', 'value': 'annual_increase'},
                            {'label': 'Monthly absolute', 'value': 'monthly_absolute'}],
                        value='annual_increase',
                        inline=True,
                        custom=False,
                        labelStyle={'margin-right': '12px'}
                    ),
                ]),

                html.Div([
                    dcc.Graph(id='gg', figure=gg)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """It is shown the evolution in the concentration of the main greenhouse gases: CO2, CH4, N2O and SF6. You can select between annual or monthly resolution paired with absolute concentrations or annual increase. Notice that each gas has its own range in units, since they are measured in mole fraction.
                        These measurements are used to study how the concentrations evolved in time and to predict them in future years."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-right': right_margin}, children=[
                html.H2(
                    children='CO2 Data',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Information Type'),
                    dbc.RadioItems(
                        id='co2-type',
                        options=[
                            {'label': 'Global and weekly', 'value': 'global_weekly'},
                            {'label': 'Per country and yearly', 'value': 'country'}],
                        value='global_weekly',
                        inline=True,
                        custom=False,
                        labelStyle={'margin-right': '12px'}
                    ),
                ]),

                html.Div(
                    dcc.Graph(id='co2', figure=co2)
                ),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Plots which show how the CO2 concentration evolved with a weekly resolution. The concentration is measured in micro/mol. It can also be seen the emissions of CO2 by the 8 biggest contributors of greenhouse gas emissions. Emissions are measured in Megatons per year.
                        These data are used to predict how CO2 emissions are going to evolve, if they tend to increase or decrease which shows how they would be if Covid-19 would not have appeared."""),
                ])
            ]),

            html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
                html.H2(
                    children='Other Greenhouse Gases',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                dbc.FormGroup([
                    dbc.Label('Information Type'),
                    dbc.RadioItems(
                        id='divers-type',
                        options=[
                            {'label': 'CH4', 'value': 'ch4'},
                            {'label': 'N2O', 'value': 'n2o'}],
                        value='ch4',
                        inline=True,
                        custom=False,
                        labelStyle={'margin-right': '12px'}
                    ),
                ]),

                html.Div([
                    dcc.Graph(id='divers', figure=divers)
                ]),
                html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
                    dcc.Markdown(
                        """Emissions of CH4 and N2O by the 8 biggest contributors of greenhouse gas emissions. Emissions are measured in Kilotons per year."""),
                ])
            ]),
        ]),
    ]),
    footer
])

# All greenhouse gases
@app.callback(
    Output('gg', 'figure'),
    [Input('gg-type', 'value')], prevent_initial_call=True)
def update_gg_graph(info_type):
    if info_type == "annual_absolute":
        axes, data = gl.gg_global_annual_demo()
        fig = get_plotly_figure(axes, False)
    elif info_type == "annual_increase":
        axes, data = gl.gg_global_ann_increase_demo()
        fig = get_plotly_figure(axes, False)
    else:
        axes, data = gl.gg_global_monthly_demo()
        fig = get_plotly_figure(axes, True)
    return fig

# CO2
@app.callback(
    Output('co2', 'figure'),
    [Input('co2-type', 'value')], prevent_initial_call=True)
def update_co2_graph(info_type):
    if info_type == "global_weekly":
        axes, data = gl.co2_global_weekly_demo()
    elif info_type == "country":
        axes, data = gl.co2_country_demo()
    else:
        axes, data = gl.co2_country_sector_demo()
    fig = get_plotly_figure(axes, True)
    fig.update_layout(margin=dict(t=60, b=30, l=0, r=0))
    return fig

# Other greenhouse gases
@app.callback(
    Output('divers', 'figure'),
    [Input('divers-type', 'value')], prevent_initial_call=True)
def update_divers_graph(info_type):
    if info_type == "ch4":
        axes, data = gl.ch4_country_demo()
    else:
        axes, data = gl.n2o_country_demo()
    fig = get_plotly_figure(axes, True)
    return fig

# Paris agreement goals
@app.callback(
    Output('goals', 'figure'),
    [Input('goals-type', 'value')], prevent_initial_call=True)
def update_goals_graph(info_type):
    if info_type == "lines":
        axes = goals_loader.demo("lines")
        plotly_fig = get_plotly_figure(axes, False)
    else:
        axes = goals_loader.demo("bubbles")
        plotly_fig = get_plotly_figure(axes, False)
        # Get legend labels from matplotlib and add to plotly, since this doesn't work automatically
        # First entry is the line, which should not be labeled
        handles, labels = axes.get_legend_handles_labels()
        for i in range(len(labels)):
            plotly_fig.data[i].name = labels[i]
    plotly_fig.update_layout(showlegend=True)
    return plotly_fig