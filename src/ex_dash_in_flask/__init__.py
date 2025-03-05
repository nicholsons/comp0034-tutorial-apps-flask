from flask import Flask, g
import pandas as pd
from ex_dash_in_flask import simpledash


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