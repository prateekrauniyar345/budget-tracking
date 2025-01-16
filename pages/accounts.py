import dash
from dash import html

dash.register_page(__name__, path='/accounts')

layout = html.Div([
    html.H1('Accounts Page'),
    html.Div('This page will display your accounts.'),
])
