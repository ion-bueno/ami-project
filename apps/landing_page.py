import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps.navbar import get_navbar
from apps.footer import footer

navbar = get_navbar("Introduction", "/")

bottom_margin = '50px'

card_covid_cases = dbc.Card(
    [
        dbc.CardImg(src="/static/cases.png", top=True),
        dbc.CardBody(
            [
                html.H4("Covid-19 cases", className="card_covid_cases-title"),
                html.P(
                    "This section shows the Covid-19 pandemic development in regard to "
                    "case numbers, deaths and recover rates.",
                    className="card_covid_cases-text",
                ),
                dbc.Button("Covid cases", color="primary", href="/covid_cases", external_link=True, size="lg"),
            ]
        ),
    ],
)

card_greenhouse_gases = dbc.Card(
    [
        dbc.CardImg(src="/static/greenhouse_gases.PNG", top=True),
        dbc.CardBody(
            [
                html.H4("Greenhouse gases", className="card_greenhouse_gases-title"),
                html.P([
                    "This section provides insights into greenhouse gas measurements "
                    "for CO", html.Sub('2'), ", CH", html.Sub('4'), ", N", html.Sub('2'), "O and SF", html.Sub('6'), "."],
                    className="card_greenhouse_gases-text",
                ),
                dbc.Button("Greenhouse gases", color="primary", href="/greenhouse_gases", external_link=True, size="lg"),
            ]
        ),
    ],
)

card_model_pipeline = dbc.Card(
    [
        dbc.CardImg(src="/static/model_pipeline.png", top=True),
        dbc.CardBody(
            [
                html.H4("Model pipeline", className="card_model_pipeline-title"),
                html.P(
                    "This section describes the entire model pipeline we used to "
                    "tackle the research question in a graphical way.",
                    className="card_model_pipeline-text",
                ),
                dbc.Button("Model pipeline", color="primary", href="/model_pipeline", external_link=True, size="lg"),
            ]
        ),
    ],
)

card_sector_emissions = dbc.Card(
    [
        dbc.CardImg(src="/static/pie_chart_sectors.png", top=True),
        dbc.CardBody(
            [
                html.H4("Sector emissions", className="card_sector_emissions-title"),
                html.P(
                    "Here, indicators for every sector can be found together with "
                    "emissions data for the most important countries.",
                    className="card_sector_emissions-text",
                ),
                dbc.Button("Sector emissions", color="primary", href="/sector_emissions", external_link=True, size="lg"),
            ]
        ),
    ],
)

card_conclusion = dbc.Card(
    [
        dbc.CardImg(src="/static/result.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Conclusion", className="card_conclusion-title"),
                html.P(
                    "This concluding section provides insights into the final result "
                    "of our research.",
                    className="card_conclusion-text",
                ),
                dbc.Button("Conclusion", color="primary", href="/conclusion", external_link=True, size="lg"),
            ]
        ),
    ],
)

card_about_us = dbc.Card(
    [
        dbc.CardImg(src="/static/about_us.png", top=True),
        dbc.CardBody(
            [
                html.H4("About us", className="about_us-title"),
                html.P(
                    "Check out this page if you want to get more insights into who we are.",
                    className="about_us-text",
                ),
                dbc.Button("About us", color="primary", href="/about_us", external_link=True, size="lg"),
            ]
        ),
    ],
)

cards = html.Div(style={'width': 'auto', 'display': 'flex', 'justify-content': 'center',
                        'align-items': 'flex-end', 'flex-direction': 'row', 'margin-bottom': bottom_margin},
                 children=[
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_covid_cases]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_greenhouse_gases]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_sector_emissions]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_model_pipeline]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_conclusion]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_about_us])
                ])

layout = html.Div([
    navbar,
    html.Br(),
    html.H1(
        children="Impacts of COVID-19 on CO2 emissions",
        style={
            'textAlign': 'center'
        }
    ),
    html.H2(
        children="To what extent will the Covid-19 pandemic contribute towards reaching goals stated in international agreements like the Paris Climate Agreement?",
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(style={'width': 'auto', 'float': 'left', 'margin': '20px', 'margin-bottom': bottom_margin}, children=[
        dcc.Markdown('''
            The Paris Agreement got a lot of publicity when it got ratified by most countries of the world.
            It thus resembles the first global, legally binding agreement to fight global warming.
            When the US under president Trump decided to leave the agreement and climate activists started the Fridays for Future movement, 
            the problem of global warming got more attention worldwide. However, as the COVID-19 pandemic began, 
            more urgent problems arose and global warming only came in second. We now want to investigate how the ongoing 
            pandemic affected global greenhouse gas emission and see how this could actually help fulfilling the ambitious goals of the Paris Agreement.
        '''),
        cards
    ]),
    footer
])
