import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Create a SQLAlchemy declarative base object called Base to be used in the models (Python classes)
class Base(DeclarativeBase):
    pass


# Create a SQLAlchemy object called db, the Base object is passed to the SQLAlchemy object
db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    # create the Flask app
    # You can specify a specific instance path also using `instance_path=your_instance_path`
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Set the location of the database file called paralympics.db which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics.db'),
        SQLALCHEMY_ECHO=False
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
    # Make sure you already defined SQLALCHEMY_DATABASE_URI in the app.config
    db.init_app(app)

    with app.app_context():
        # Optionally, create the database tables
        # This will only work once the models are defined

        # This imports the models
        from flask_para import models
        # If the database file does not exist, it will be created
        # If the tables do not exist, they will be created but does not overwrite or update existing tables
        db.create_all()

        # Import and use the function to add the data to the database only if it is empty
        # If query of the Events returns None, then the database is assumed empty
        if db.session.execute(db.select(models.Event).limit(1)).first() is None:
            from flask_para.add_data import add_all_data
            add_all_data()

        # Register the blueprint
        from flask_para.paralympics import main
        app.register_blueprint(main)

    # return the app
    return app
