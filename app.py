import dash
import dash_bootstrap_components as dbc


external_stylesheets = ['http://fonts.googleapis.com/css?family=Maven+Pro:400',
                        'https://codepen.io/chriddyp/pen/dZMMma',
                        'https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server