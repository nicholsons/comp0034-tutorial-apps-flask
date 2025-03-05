from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo

from ex_flasklogin import db
from ex_flasklogin.models import User, Profile


class SignupForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address required')])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password required')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
        if user is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
        if user is None:
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = db.session.execute(db.select(User).filter_by(email=self.email.data)).scalar_one_or_none()
        if user is None:
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')


class ProfileForm(FlaskForm):
    """ Class for the profile form"""
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')

    def validate_username(self, username):
        profile = db.session.execute(db.select(Profile).filter_by(username=username.data)).scalar_one_or_none()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')
