import dash
from dash import html

dash.register_page(__name__, path='/settings')

def layout():
    layout = html.Div([
        html.H1('Setting Page'),
        html.Div('This page will display your setting.'),
    ])
    return layout
