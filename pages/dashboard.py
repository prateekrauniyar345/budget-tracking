import dash
from dash import html

dash.register_page(__name__, path='/dashboard')

layout = html.Div([
    html.H1('This is our dashbaord page'),
    html.Div('This is our dashbaord page content.'),
])