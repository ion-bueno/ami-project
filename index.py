import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import landing_page, sector_emissions, covid_cases, greenhouse_gases, model_pipeline, conclusion, group_presentation

app.layout = html.Div([
        dcc.Location(id='url', refresh=True),
        #dcc.Loading(color='black', type='circle', fullscreen=True, children=[ #className="dash_loading-callback",
        html.Div(id='page-content')
        #])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return landing_page.layout
    elif pathname == '/covid_cases':
        return covid_cases.layout
    elif pathname == '/greenhouse_gases':
        return greenhouse_gases.layout
    elif pathname == '/sector_emissions':
        return sector_emissions.layout
    elif pathname == '/model_pipeline':
        return model_pipeline.layout
    elif pathname == '/conclusion':
        return conclusion.layout
    elif pathname == '/about_us':
        return group_presentation.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)