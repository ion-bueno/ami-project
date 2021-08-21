import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# -*- coding: utf-8 -*-

#footer = html.Footer(className="container", children=[#, style={'display': 'flex', 'justify-content': 'center', 'background-color': 'grey', 'padding': '5px'}, children=[
#        html.Div([html.Br(), html.Hr(className="my-2"), html.Br(), html.P(children="Provided to you by eight students @TUM as part of the course Applied Machine Intelligence")])
#])

footer = html.Div(className="footer", style={'position': 'fixed', 'bottom': 0, 'text-align': 'center',
                                                   'background-color': 'white', 'width': '100%'},
                  children=[
                          html.Footer(children=[
                                html.Hr(className="my-2"),
                                html.Span(children="Brought to you by eight students @TUM as part of the course Applied Machine Intelligence \U000021D2 "),
                                html.A("About us", href="/about_us")
                        ])
                ])