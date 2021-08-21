import dash_bootstrap_components as dbc

font_size_items = '1.2em'
font_size_bar = '1.2em'
font_family = 'Maven Pro'
style_bar = {'font-size': font_size_bar, 'padding': 0, 'margin': 0, 'list-style': 'none',
             'overflow': 'none', 'vertical-align': 'middle', #'text-transform':'uppercase',
             'font-family':"'Maven Pro', sans-serif", 'cursor':'pointer', 'margin-right':'10px'}
style_items = {'font-size': font_size_items, 'font-family':"'Maven Pro', sans-serif"}

def get_navbar(page="Introduction", page_ref="/"):
    items = [
        dbc.DropdownMenuItem("More pages", header=True, style={'font-size': font_size_items}),
        dbc.DropdownMenuItem("Introduction", href="/", external_link=True, style={'font-size': font_size_items}),
        dbc.DropdownMenuItem("Covid-19 cases", href="/covid_cases", external_link=True,
                             style=style_items),
        dbc.DropdownMenuItem("Greenhouse gas data", href="/greenhouse_gases", external_link=True,
                             style=style_items),
        dbc.DropdownMenuItem("CO2 Emissions by Sector", href="/sector_emissions", external_link=True,
                             style=style_items),
        dbc.DropdownMenuItem("Model pipeline description", href="/model_pipeline", external_link=True,
                             style=style_items),
        dbc.DropdownMenuItem("Final Results", href="/conclusion", external_link=True,
                             style=style_items),
        dbc.DropdownMenuItem("About us", href="/about_us", external_link=True,
                             style=style_items)
    ]
    for i in range(len(items)-1):
        if items[i+1].href == page_ref:
            items.pop(i+1)
            break

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page, href=page_ref, disabled=True),
                        style=style_bar, className="active", active=True),
            dbc.DropdownMenu(
                children=items,
                right=True,
                nav=True,
                in_navbar=True,
                label="More",
                style=style_bar
            ),
        ],
        brand="Impacts of Covid-19 on CO2 emissions",
        brand_href="/",
        brand_external_link=True,
        brand_style=style_bar,
        color="black",
        dark=True,
        fluid=True,
        sticky="top",
        style=style_bar
    )
    return navbar
