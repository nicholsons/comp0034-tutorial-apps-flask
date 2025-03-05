from pathlib import Path
import logging
from flask import Flask
from flask_iris.create_ml_model import create_model
from flask_iris.config import app_config

def create_app(config_name=None):
    """Create and configure the Flask app

    Args:
    config_name: name of the configuration environment (see config.py)

    Returns:
    Configured Flask app

    """
    log_path = Path(__file__).parent.parent.parent.joinpath('iris_app.log')
    logging.basicConfig(filename=str(log_path), level=logging.DEBUG)

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])

    with app.app_context():
        from flask_iris import routes

    # If the ml model file isn't present, create it. Requires scikit-learn to be installed.
    # create_model("lr")

    return app
