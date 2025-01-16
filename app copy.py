
# # Define the app layout
# dash_app.layout = dbc.Container(
#     [
#         dbc.Row(
#             dbc.Alert(heading, color="primary")
#         ), 
#         dbc.Row(
#             [
#                 dbc.Col(navbar, width=2, style={
#                     'padding' : '1rem',
#                     'border' : '1px solid black',
#                 }),  # Place the vertical navbar in the left column
#                 dbc.Col(
#                     html.Div("This is the ongoing Budget Management project.", ),
#                     width=10,  # Content occupies the remaining space
#                     style={
#                     'border' : '0.8px solid black',   
#                     'padding' : '1rem',
#                 }
#                 ),
                
#             ], 
#         ),
#     ],
#     fluid=True,  # Make the container full-width
# )



# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc

# # Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Define the layout
# app.layout = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 # Left Sidebar (Navigation)
#                 dbc.Col(
#                     [
#                         html.H3("Navigation", style={"text-align": "center"}),
#                         dbc.Nav(
#                             [
#                                 dbc.NavLink("Home", href="#", active="exact"),
#                                 dbc.NavLink("About", href="#", active="exact"),
#                                 dbc.NavLink("Services", href="#", active="exact"),
#                                 dbc.NavLink("Contact", href="#", active="exact"),
#                             ],
#                             vertical=True,  # Makes the nav vertical
#                             pills=True,     # Adds pill styling
#                         ),
#                     ],
#                     width=3,  # Adjust the width of the left column (out of 12)
#                     style={"background-color": "#f8f9fa", "padding": "20px"},
#                 ),
#                 # Main Content Area
#                 dbc.Col(
#                     [
#                         html.H2("Content Window"),
#                         html.P("This is the main content area where different pages will appear."),
#                         dcc.Graph(
#                             id="example-graph",
#                             figure={
#                                 "data": [
#                                     {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
#                                     {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "NYC"},
#                                 ],
#                                 "layout": {"title": "Example Graph"},
#                             },
#                         ),
#                     ],
#                     width=9,  # Adjust the width of the right column (out of 12)
#                     style={"padding": "20px"},
#                 ),
#             ]
#         )
#     ],
#     fluid=True,  # Makes the container take the full width of the page
# )

# # Run the app
# if __name__ == "__main__":
#     app.run_server(debug=True)






from flask import Flask
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dcc

# Initialize Flask app
app = Flask(__name__)

# Initialize Dash app linked with Flask
dash_app = dash.Dash(
    __name__,
    server=app,  # Pass the Flask app instance to Dash
    external_stylesheets=[dbc.themes.FLATLY, "/assets/custom.css"],
    url_base_pathname='/dashboard/',  # Set base path for the Dash app
    use_pages=True  # Enable page support in Dash
)

# Register pages
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.H3("Dashboard Page"),
])

# Function to get user pages
def get_user_pages():
    # Use dash_app.page_registry to get all registered pages
    pages = [page for page in dash_app.page_registry.values()]
    print("Pages are:", pages)
    return pages

# Call function to check registered pages
get_user_pages()

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
