from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Optional, Regexp, ValidationError

from paralympics_sq3.db import get_db


class QuizForm(FlaskForm):
    quiz_name = StringField('Quiz Name', validators=[DataRequired()])
    close_date = StringField('Date', [Optional(),
                                      Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$',
                                             message="Date must be in the format DD/MM/YYYY")
                                      ])

    def validate_quiz_name(self, quiz_name):
        """Custom validator to ensure that the quiz_name is unique."""
        db = get_db()
        quiz = db.execute('SELECT * from quiz where quiz_name = ?', (quiz_name.data,)).fetchone()
        if quiz:
            raise ValidationError('Quiz name already exists. Please choose a different name.')


class PredictionForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    team = SelectField('Team', choices=[], validators=[DataRequired()])
