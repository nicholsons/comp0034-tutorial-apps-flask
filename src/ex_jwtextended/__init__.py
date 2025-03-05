from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["FLASK_SECRET_KEY"] = "your-secret-key"  # Change this!
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # In memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        from jwtexample.models import User
        db.create_all()
        batman = User(username="batman", password="robin")
        panther = User(username="panther", password="claw")
        db.session.add(batman)
        db.session.add(panther)
        db.session.commit()

    from jwtexample.routes import bp
    app.register_blueprint(bp)

    return app
