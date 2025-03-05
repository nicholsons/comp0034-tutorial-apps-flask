# Uses the Direct Hosting on Dash method described in the blog post
# https://ploomber.io/blog/dash-in-flask/
# Population app code
# Extra code added to demo a navbar
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from flask import g


def init_app(url_path, server=None):
    global df


    app = Dash(server=g.cur_app, url_base_pathname=url_path, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Access the variables defined in the main Flask instance using g object.
    df = g.df

    app.title = "Dashboard"

    app.layout = dbc.Container(
        [
            # Navbar is repeated in both Flask and Dash apps
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
                    dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard", external_link=True)),
                ],
                brand="Dash in Flask Example App",
                color="primary",
                dark=True,
                links_left=True,
            ),
            html.Br(),
            html.H4(children="Population by country"),
            dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
            dcc.Graph(id="graph-content"),
        ]
    )

    init_callbacks(app)
    return app.server


def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


def init_callbacks(app):
    app.callback(
        Output("graph-content", "figure"),
        Input("dropdown-selection", "value")
    )(update_graph)