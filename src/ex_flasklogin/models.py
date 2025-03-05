from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flask_login_example import db


class User(db.Model, UserMixin):
    """
    User model class

    Inherits the FlaskSQLAlchemy model
    Inherits UserMixin which is required for Flask-Login
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    profile = db.relationship('Profile', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.email, self.first_name, self.last_name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password_text):
        return check_password_hash(self.password, password_text)


class Profile(db.Model):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(db.String, nullable=True)
    photo: Mapped[str] = mapped_column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='profile')
