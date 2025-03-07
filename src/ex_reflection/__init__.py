import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Create a SQLAlchemy declarative base object called Base to be used in the models (Python classes)
class Base(DeclarativeBase):
    pass


# Create a SQLAlchemy object called db, the Base object is passed to the SQLAlchemy object
db = SQLAlchemy(model_class=Base)


def create_app():
    # create the Flask app
    # You can specify a specific instance path also using `instance_path=your_instance_path`
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.dirname(os.path.abspath(__file__)))
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Set the location of the database file called paralympics.db which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'recycling_data.db'),
        SQLALCHEMY_ECHO=False
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise the database
    # Make sure you already defined SQLALCHEMY_DATABASE_URI in the app.config
    db.init_app(app)

    with app.app_context():
        db.reflect()

        # Register the blueprint
        from ex_reflection.routes import main
        app.register_blueprint(main)

    # return the app
    return app
