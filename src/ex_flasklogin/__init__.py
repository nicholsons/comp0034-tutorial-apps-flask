import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# See https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
# See https://flask-reuploaded.readthedocs.io/en/latest/getting_started/
photos = UploadSet(name="photos", extensions=IMAGES)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='create-your-own-key',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'simple_login.sqlite'),
        UPLOADED_PHOTOS_DEST="static/images",
        # SQLALCHEMY_ECHO=True
    )
    if test_config:
        app.config.from_mapping(test_config)

    # Create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise the extensions
    db.init_app(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    configure_uploads(app, photos)

    # Create and initialise the database
    from flask_login_example.models import User
    with app.app_context():
        db.create_all()

        from flask_login_example import views

    return app
