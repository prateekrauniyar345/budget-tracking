import dash
from dash import html

dash.register_page(__name__, path='/profile')

def layout():
    layout = html.Div([
        html.H1('Profile Page'),
        html.Div('This page will display your profile.'),
    ])
    return layout
