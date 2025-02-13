import dash
from dash import html

dash.register_page(__name__, path='/logout')

def layout():
    layout = html.Div([
        html.H1('Logout Page'),
        html.Div('This page will display your logout setting.'),
    ])
    return layout
