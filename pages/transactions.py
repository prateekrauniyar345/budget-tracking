import dash
from dash import html

dash.register_page(__name__, path='/transactions')

layout = html.Div([
    html.H1('Transactions Page'),
    html.Div('This page will display your transactions.'),
])