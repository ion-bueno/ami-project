import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
import matplotlib
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

from app import app
from apps.navbar import get_navbar
from apps.mpl_to_plotly import get_plotly_figure
from prediction.co2_covid.sectors_combination import get_demo as get_combined_emission_demo
from apps.footer import footer
from loader.results_loader import ResultsLoader

matplotlib.use('agg')

cur_dir = os.getcwd()
os.chdir("prediction/co2_covid")
ax = get_combined_emission_demo("EU")
change_rate = get_plotly_figure(ax, True)
os.chdir(cur_dir)

res = ResultsLoader()
res.load()
[ax_cases, ax_deaths] = res.get_result_plots()
comparison = get_plotly_figure(ax_cases, True)

colorscale = [[0, 'black'], [1, 'white']]
font_colors = ['white', 'black']
countries_correlation = ["Canada", "China", "Japan", "Russia", "Brazil", "India", "United States", "EU"]
indices = ["Overall emissions", "Construction industry", "Transport sector", "Power industry", "Other industries"]
pearson = pd.read_csv('prediction/co2_no_covid/zied/pearson.csv').T.iloc[1:].replace(np.nan, 10).round(2).replace(10, np.nan).values
pearson_values = np.absolute(pearson)
spearman = pd.read_csv('prediction/co2_no_covid/zied/spearman.csv').T.iloc[1:].replace(np.nan, 10).round(2).replace(10, np.nan).values
spearman_values = np.absolute(spearman)
correlation = ff.create_annotated_heatmap(z=pearson_values, annotation_text=pearson, x=countries_correlation, y=indices, colorscale=colorscale, font_colors=font_colors)
correlation.layout.margin.update({
        "l": 50,
        "r": 50,
        "b": 20,
        "t": 20,
        "pad": 4
})
for i in range(len(correlation.layout.annotations)):
    if np.absolute(float(correlation.layout.annotations[i].text)) < 0.5:
        correlation.layout.annotations[i].font.color = 'white'
    else:
        correlation.layout.annotations[i].font.color = 'black'


navbar = get_navbar("Conclusion", "/conclusion")

countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

div_width = '768px'
bottom_margin = '50px'
margin_right = '40px'

layout = html.Div([
    navbar,
    html.Br(),
    html.H1(
        children="Final Results",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin, 'margin-right': margin_right}, children=[
        html.H2(
            children='CO2 Emission change rate since January 2020',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Label('Country'),
        dcc.Dropdown(
            id='change_rate-type',
            options=[{'label': i, 'value': i} for i in countries],
            value='EU',
            style={'width': '100%'}
            # labelStyle={'display': 'block', 'padding': '1px 10px', 'white-space':'normal'}
        ),

        html.Div([
            dcc.Graph(id='change_rate', figure=change_rate)
        ]),
        html.Div(style={'text-align': 'justify', 'text-align-last': 'left', 'white-space': 'pre-line'}, children=[
            html.P(
                """This figure shows the emission change rate compared to the expected emissions in the time interval from January to June 2020.
                You can select between the most important countries."""),
        ])
    ]),
    html.Div(style={'backgroundColor': colors['background'], 'width': div_width, 'float': 'left', 'margin': '20px', 'margin-bottom': '60px'}, children=[
        html.H2(
            children='Emission drop in relation to Covid-19',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dbc.FormGroup([
            dbc.Label('Information Type'),
            dbc.RadioItems(
                id='comparison-type',
                options=[
                    {'label': 'Cases', 'value': 'cases'},
                    {'label': 'Deaths', 'value': 'deaths'}],
                value='cases',
                inline=True,
                custom=False,
                labelStyle={'margin-right': '12px'}
            ),
        ]),

        html.Div([
            dcc.Graph(id='comparison', figure=comparison)
        ]),
        html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
            dcc.Markdown(
                """This figure shows the average emission drop in the months from January to June 2020 for the most important countries plotted over Covid-19 statistics.
                Either Covid-19 related case numbers or death numbers can be taken into consideration."""),
        ])
    ]),
    html.Div(style={'backgroundColor': colors['background'], 'width': '1536px', 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
        html.H2(
            children='Correlation of Covid-19 development with CO2 emissions',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dbc.FormGroup([
            dbc.Label('Correlation Type',
                      style={'textAlign': 'center',
                            'color': colors['text']}),
            dbc.RadioItems(
                id='correlation-type',
                options=[
                    {'label': 'Pearson Correlation', 'value': 'pearson'},
                    {'label': 'Spearman Correlation', 'value': 'spearman'}],
                value='pearson',
                inline=True,
                custom=False,
                labelStyle={'margin-right': '12px'},
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
        ]),

        html.Div([
            dcc.Graph(id='correlation', figure=correlation)
        ]),

        html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
            dcc.Markdown(
                """This table shows the correlation of the time series development of Covid-19 cases with CO2 emissions in total and by sector.
                It can be chosen between using either the pearson or the spearman correlation. A value of 0 means no correlation, -1 represents the maximal negative correlation and +1 represents the maximal positive correlation. The heatmap displays strong correlations in white and no correlations in black."""),
        ])
    ]),
    html.Div(style={'backgroundColor': colors['background'], 'width': '1536px', 'clear': 'both', 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
        html.H2(
            children='Conclusion and Answer to the Research Question',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(style={'text-align': 'justify', 'white-space': 'pre-line'}, children=[
            dcc.Markdown(
                """From the integrated sector trends, we can see a drop in CO2 emissions. This can be directly attributed to the manifold effects of the pandemic. 
                We tried to quantify the effect and correlate emission drops to active cases of COVID-19. On a time-series, we could not find a direct relation, especially not for all countries. We thus decided to look at the integrated emission drops and case numbers/deaths. However, one can not deduce a general trend from these two plots either. We therefore conclude that we have to discuss each country by its own.
                Still, we have to answer our research question with these results. As we can see from the bubble plot of the Paris climate goals, most countries will miss the 1.5° goal. We want to estimate from the plot how much the emission drop helps each country to reach its goal.
                Due to the pandemic, most countries see an emission drop by over 15% for the first half of 2020. Of course, we cannot say much about how the CO2 emissions will behave in the next ten years and quantifying the effect of the pandemic on countries reaching their climate goals is difficult. We want to do these calculations exemplary with Japan, as it is the country with highest gap to the 1.5° goal. We see that Japan would need to further reduce its emissions by roughly 15%. This means, that Japan needs to reduce its emissions on average by 15% every year. We see from the total average emission drop plot that Japan reduced its emission by 22.5% during the first half of 2020. This is just slightly more than Japan would need to reduce the emissions at least. We can do the same assessment for every country. We conclude that for every country, the emissions would need to stay permanently on a similar level as in the first half of 2020, every year, until 2030."""),
        ])
    ]),
    footer
])


@app.callback(
    Output('change_rate', 'figure'),
    [Input('change_rate-type', 'value')], prevent_initial_call=True)
def update_change_rate_graph(country):
    cur_dir = os.getcwd()
    os.chdir("prediction/co2_covid")
    axes = get_combined_emission_demo(country)
    os.chdir(cur_dir)
    return get_plotly_figure(axes, True)

@app.callback(
    Output('comparison', 'figure'),
    [Input('comparison-type', 'value')], prevent_initial_call=True)
def update_comparison_graph(comparison_type):
    if comparison_type == "cases":
        axes = res.get_result_plots()[0]
    else:
        axes = res.get_result_plots()[1]
    return get_plotly_figure(axes, True)


@app.callback(
    Output('correlation', 'figure'),
    [Input('correlation-type', 'value')], prevent_initial_call=True)
def update_correlation_graph(statistics):
    if statistics == "pearson":
        csv = pd.read_csv('prediction/co2_no_covid/zied/pearson.csv').T.iloc[1:].replace(np.nan, 10).round(2).replace(10, np.nan).values
    else:
        csv = pd.read_csv('prediction/co2_no_covid/zied/spearman.csv').T.iloc[1:].replace(np.nan, 10).round(2).replace(10, np.nan).values
    csv_values = np.absolute(csv)
    fig = ff.create_annotated_heatmap(z=csv_values, annotation_text=csv, x=countries_correlation,
                                              y=indices, colorscale=colorscale, font_colors=font_colors)
    fig.layout.margin.update({
        "l": 50,
        "r": 50,
        "b": 20,
        "t": 20,
        "pad": 4
    })
    for i in range(len(fig.layout.annotations)):
        if np.absolute(float(fig.layout.annotations[i].text)) < 0.5:
            fig.layout.annotations[i].font.color = 'white'
        else:
            fig.layout.annotations[i].font.color = 'black'
    return fig
