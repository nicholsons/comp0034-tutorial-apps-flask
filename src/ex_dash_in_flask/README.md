# Dash as a route in Flask demonstrator

Uses the Direct Hosting on Dash method described in the blog post
https://ploomber.io/blog/dash-in-flask/

## Change made to the Dash app

1. Create a function `def init_callbacks(app)` and move the callback decorators into this.

    ```python
    def update_graph(value):
        dff = df[df.country == value]
        return px.line(dff, x="year", y="pop")
    
    
    def init_callbacks(app):
        app.callback(
            Output("graph-content", "figure"),
            Input("dropdown-selection", "value")
        )(update_graph)
    ```

2. Create a function called `def init_app()` and move the code to create the Dash app into this. Add to this code after the layout a call to `init_callbacks(app)` (i.e. the function you just created).

    ```python
    from dash import Dash, html, dcc
    import dash_bootstrap_components as dbc
    from flask import g
    
    
    def init_app(url_path, server=None):
        global df    
        app = Dash(server=g.cur_app, url_base_pathname=url_path, external_stylesheets=[dbc.themes.BOOTSTRAP])
        df = g.df  # Access the variables defined in the main Flask instance using g object.
        app.title = "Dashboard"
        app.layout = dbc.Container(
            [
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
    ```
   
Note that Dash app isn't in a Flask template so the navbar is manually created here as well as in the Flask app.

## Changes made to the Flask app

Modify the create_app() to run the Dash app on the Flask instance.

```python
def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    with app.app_context():
        # Register the Flask routes
        from ex_dash_in_flask import simpleflask

        # Define Flask context variables to be used in apps.
        # In this case, we define the dataframe used in the Population app (df)
        # and the Flask instance to be passed to the app (cur_app)
        g.df = pd.read_csv(
            "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
        )

        g.cur_app = app

        # Add Dash app to Flask context. Specify the app's url path and pass the flask server to your data
        app = simpledash.init_app("/dashboard/")

    return app
```

To run the Flask app: `flask --app ex_dash_in_flask run --debug`