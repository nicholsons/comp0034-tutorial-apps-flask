from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Optional, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField

from flask_para import db
from flask_para.models import Country


class QuizForm(FlaskForm):
    quiz_name = StringField('Quiz Name', validators=[DataRequired()])
    close_date = StringField('Date', [Optional(),
                                      Regexp(r'^\d{1,2}/\d{1,2}/\d{4}$',
                                             message="Date must be in the format DD/MM/YYYY")
                                      ])


# TODO: Add a custom validator to ensure that the quiz_name is unique.

def teams():
    """Return a query to get the list of teams for the QuerySelectField.
    https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/#wtforms_sqlalchemy.fields.QuerySelectField
    """
    return db.session.execute(db.select(Country).where(Country.member_type != 'dissolved')).scalars()


class PredictionForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    team = QuerySelectField('Team', query_factory=teams, get_label='name', allow_blank=True, validators=[DataRequired()])
