import os

from flask import Flask


def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'paralympics.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise the database
    # See https://flask.palletsprojects.com/en/stable/tutorial/database/#register-with-the-application
    from . import db
    db.init_app(app)

    # Register the blueprint
    from flask_para_sq3.paralympics import main
    app.register_blueprint(main)

    # return the app
    return app
