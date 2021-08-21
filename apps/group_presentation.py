import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps.navbar import get_navbar
from apps.footer import footer

navbar = get_navbar("About us", "/about_us")

bottom_margin = '50px'

def create_personal_card(name, text, img):
    personal_card = dbc.Card(
        [
            dbc.CardImg(src="/static/{}".format(img), top=True, style={'display': 'block', 'width':'100.5%', 'object-fit':'cover'}),
            dbc.CardBody(
                [
                    html.H4(name, className="card_{}-title".format(name)),
                    html.P(text, className="card_{}-text".format(name))
                ]
            ),
        ],
    )
    return personal_card

card_philipp = create_personal_card("Philipp Krüger",
                                    "Hello there! Philipp is passionate about music production and physics.",
                                    "philipp.jpeg")

card_max = create_personal_card("Maximilian Egger",
                                    "Max really appreciates the challenge of diving into new projects while working together with highly motivated people.",
                                    "max.jpeg")

card_maxl = create_personal_card("Max-Emanuel Kern",
                                    "Maxl - studies physics, is sad when his beer is empty but happy if it's hoppy.",
                                    "maxl.jpeg")

card_daniel = create_personal_card("Daniel Martin Cruz",
                                    "Hi! My name is Daniel and I am a Spanish student that spent a very nice year in Munich. My main passions are films and Bavarian beer.",
                                    "daniel_4_3.jpeg")

card_ion = create_personal_card("Ion Bueno Ulacia",
                                    "Hallo! My name is Ion Bueno and I am studying in Spain. I love sports and trap music!",
                                    "Ion.jpeg")

card_aras = create_personal_card("Aras Bayrakceken",
                                    "“Ogres are like onions.” – Shrek",
                                    "aras.jpg")

card_damian = create_personal_card("Damian Tarasewicz",
                                    "",
                                    "dummy.jpeg")

card_zied = create_personal_card("Zied Belkhiria",
                                    "Hello, I study electrical engineering. I like programming and finding new solutions to solve problems.",
                                    "zied.jpeg")

cards = html.Div(style={'width': 'auto', 'display': 'flex', 'justify-content': 'center',
                        'align-items': 'flex-start', 'flex-direction': 'row', 'margin-bottom': bottom_margin},
                 children=[
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_philipp]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_max]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_maxl]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_daniel]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_ion]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_aras]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_damian]),
                    html.Div(style={'width' : '19.7%', 'padding': '10px'}, children=[card_zied])
                ])

jumbotron = dbc.Jumbotron([
    html.H1("Jumbotron", className="display-3"),
        html.P(
            "Use a jumbotron to call attention to "
            "featured content or information.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Jumbotrons use utility classes for typography and "
            "spacing to suit the larger container."
        ),
        html.P(dbc.Button("Learn more", color="primary"), className="lead"),
])

layout = html.Div([
    navbar,
    html.Br(),
    html.H1(
        children="About us",
        style={
            'textAlign': 'center'
        }
    ),
    html.H3(
        children='''We are a group of international students @TUM with different backgrounds and courses of study,
                 gathered together to apply their theoretical expertise in a practical project. Together we wanted to use
                 machine learning to find out if there exists a correlation between the Covid-19 pandemic and CO2 emissions.''',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(style={'width': 'auto', 'float': 'left', 'margin': '20px'}, children=[
    #    dcc.Markdown('''
    #        We are a group of international students @TUM with different backgrounds and courses of study,
    #        gathered together to apply their theoretical expertise in a practical project. Together we wanted to use
    #        machine learning to find out if there exists a correlation between the Covid-19 pandemic and CO2 emissions.
    #    '''),
    #    html.Br(),
        cards
    ]),
    footer
])
