import dash
from dash import html

dash.register_page(__name__, path='/goals')

def layout():
    layout = html.Div([
        html.H1('Goals Page'),
        html.Div('This page will help you set and track your goals.'),
    ])
    return layout