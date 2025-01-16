from flask import Flask, url_for, request, redirect, render_template, flash, session
import psycopg2
from flask_bcrypt import Bcrypt
from auth_and_reg.auth_and_reg  import validate_login, validate_register
import os
from dotenv import load_dotenv
import pandas
from dash import Dash, html, dcc, callback, Output, Input, page_container, page_registry, register_page
import dash.dependencies as dd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate


# load the environment variables
load_dotenv()

app  = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/validate_login', methods = ['POST', 'GET'])
def validate_log():
    if request.method == 'POST':
        response, msg = validate_login()
        if response:
            # return render_template('home.html')
            return redirect('/home')
        else:
            return render_template('login.html', error=msg)
    return redirect(url_for('login'))

@app.route('/validate_register', methods = ['POST'])
def validate_reg():
    if request.method == 'POST':
        response, msg = validate_register()
        if response:
            return render_template('login.html')
        else:
            return render_template('register.html', error=msg)
    return redirect(url_for('register'))


@app.route('/home')
def home():
    return redirect('/home/dashboard')  # Redirect to a specific Dash page

# Initialize Dash app
dash_app = dash.Dash(__name__, 
                server=app, 
                external_stylesheets=[dbc.themes.FLATLY, "/assets/custom.css", ] ,
                url_base_pathname='/home/', 
                use_pages=True,
                )


# Define the vertical navbar
navbar = dbc.Nav(
    [
        dbc.NavLink("Dashboard", href="/home/dashboard", active="exact",  className="text-primary"),
        dbc.NavLink("Transactions", href="/home/transactions", active="exact", className="text-primary"),
        dbc.NavLink("Accounts", href="/home/accounts", active="exact" , className="text-primary"),
        dbc.NavLink("Goals", href="/home/goals", active="exact", className="text-primary"),
        html.Hr(),  # Add a horizontal rule to separate main options from user-related options
        dbc.NavLink("Profile", href="/home/profile", active="exact", className="text-primary"),
        dbc.NavLink("Settings", href="/home/settings", active="exact", className="text-primary"),
        dbc.NavLink("Logout", href="#", active="exact", className="text-danger"),  # Highlight logout for emphasis
    ],
    vertical=True,
    pills=True,
    style = {
        'font-size' : '1.1rem',
        # 'color' : 'black',
    }
)




dash_app.layout = dbc.Container(
    # dcc.Location to track the current URL
    children=[
        dcc.Location(id='url', refresh=True),
        dbc.Row(
            [
                # first column
                dbc.Col(
                    [
                        # Branding or title----
                        dbc.Alert(
                                [
                                    dcc.Link(
                                        html.Div(
                                        children=[
                                            # Logo image
                                            html.Img(
                                                src="assets/pictures/rich.png",  # Path to your logo file
                                                style={
                                                    "width": "40px",  # Adjust the size of the logo
                                                    "margin-right": "0px",  # Add space between the image and the title
                                                    "margin-bottom": "-3px", 
                                                    'padding' : '0px',
                                                },

                                            ),
                                            # App title
                                            html.H4(
                                                "Budget Buddy",
                                                className="alert-heading",
                                                style={
                                                       "font-weight": "bold", 
                                                       "margin": "0px 0px", 
                                                       'padding' : '0px', 
                                                       "display": "inline-block"
                                                       },
                                                n_clicks=0,
                                            ),
                                        ],
                                        style={
                                            "display": "flex",  # Use flexbox for alignment
                                            "align-items": "center",  # Vertically align image and text
                                            'cursor' : 'pointer',
                                            "margin-bottom": "0",  # Remove any bottom margin from the alert
                                            'padding' : '0px',
                                        },
                                    ),
                                    href="/home/dashboard",
                                    className='dcclink',
                                    style={
                                        'textDecoration' : 'none',
                                    }
                                    )
                                ],
                                color="primary",  # Adds a color to make the header stand out
                                style={
                                    "text-align": "left",
                                    "font-size": "1.5rem",
                                    "margin" : "0px",
                                    # 'border' : '1px solid red',
                                },
                            ),
                        # Navigation bar component
                        navbar,  # Replace with your actual navbar content
                    ],
                    width=2,  # Adjust sidebar width (out of 12)
                    style={
                        "background-color": "white", 
                        "padding": "0px",  # Adds some internal spacing
                        "text-align": "left",
                        "height": "100vh",  # Ensures the sidebar takes the full height of the viewport
                        "box-shadow": "2px 0 5px rgba(0,0,0,0.1)",  # Adds a subtle shadow for separation
                        # 'border' : '1px solid black',
                    },
                ),


                # second column  - Main content area
                dbc.Col(
                    [
                        dbc.Alert(
                            [
                                html.Div(
                                    children=[
                                        html.H4('Dashboard')
                                    ], 
                                    id = "dash_app_heading",
                                    className='dash_app_heading',
                                )
                            ], 
                            color = "primary", 
                            style={
                                    "text-align": "left",
                                    "font-size": "1.5rem",
                                    "margin-bottom": "10px",
                                    'border-left' : '2px solid black'
                                },

                        ),
                        html.Div(
                            children=[
                                page_container, 
                            ], 
                            style = {
                                'padding' : '0px 10px 10px 10px', # top, right, bottom, left 
                                # 'border' : '1px solid black',
                            }
                        ),
                    ],
                    width=10,  # Adjust the width of the right column (out of 12)
                    style={'padding' : '0px', },
                ),
            ]
        )
    ], style={
        'border' : '1px solid black',
        'min-width' : '1400px',
    }, 
    fluid=True,
    className='main_body',
)


# callbacks
dash_app.callback(
    Output('main_body', 'children'), 
    Input('alert-heading', 'n_clicks'),
    prevent_initial_call=True,
)
def click_heading_alert(click):
    if click is None:
        # PreventUpdate prevents ALL outputs updating
        raise PreventUpdate
    else:
        return "/dashboard"
    
@dash_app.callback(
    Output("dash_app_heading", "children"),  # Correct property to update
    Input("url", "pathname"),  # Correct input property
)
def change_dash_app_heading(url):
    if url == "/home/dashboard":
        return "Dashboard"
    elif url == "/home/transactions":
        return "Transactions"
    elif url == "/home/accounts":
        return "Accounts"
    elif url == "/home/goals":
        return "Goals"
    
    return "Welcome!"  # Default message






pages = [page for page in dash.page_registry.values()] 
# print("pages are : ", pages)


if __name__ ==  '__main__':
    app.run(debug=True)
   