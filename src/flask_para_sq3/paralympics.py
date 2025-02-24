import importlib.resources
import sqlite3

import joblib
import pandas as pd
import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_para_sq3.db import get_db
from flask_para_sq3.figures import line_chart
from flask_para_sq3.forms import PredictionForm, QuizForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Renders the home page that is now a list of all paralympics with hyperlinks to the event page for each."""
    # Query the database to get all the events and arrange in date order
    db = get_db()
    query = ("SELECT event.event_id, event.type, event.year, host.host FROM event "
             "JOIN host_event ON event.event_id = host_event.event_id "
             "JOIN host on host_event.host_id = host.host_id "
             "ORDER BY event.type, event.year;")
    event_list = db.execute(query).fetchall()
    return render_template('events.html', events=event_list)


@main.route('/event/<int:event_id>')
def get_event(event_id):
    db = get_db()
    try:
        event = db.execute(
            'SELECT event.year, event.start, event.end, event.highlights, event.url, host.host '
            'FROM event '
            'JOIN host_event ON event.event_id = host_event.event_id '
            'JOIN host ON host_event.host_id = host.host_id '
            'WHERE event_id = ?', (event_id,)).fetchone()
        return render_template('event.html', event=event)
    except sqlite3.Error as e:
        return {'message': "No event found with that id"}, 404


@main.route('/news')
def get_news():
    """Get the top stories from Hacker News.
    The page will be slow to load due to the number of requests made to the Hacker News API.
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    item_ids = response.json()
    stories = []
    # Get 3 articles
    for i in range(3):
        url = f"https://hacker-news.firebaseio.com/v0/item/{item_ids[i]}.json"
        response = requests.get(url)
        stories.append(response.json())
    return render_template('news.html', stories=stories)


@main.get('/chart')
def display_chart():
    """ Returns a page with a line chart. """
    db = get_db()
    line_fig = line_chart(feature="participants", db=db)
    return render_template('chart.html', fig_html=line_fig)


# TODO: Move quiz to its own blueprint
@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # If the form has been submitted, use the values from it which are accessed using request.form
    form = QuizForm(request.form)

    if form.validate_on_submit():
        print("submitted")
        # Get the values from the form
        quiz_name = form.quiz_name.data
        close_date = form.close_date.data

        # check if a quiz with the same name already exists
        db = get_db()
        existing_quiz = db.execute("SELECT * FROM quiz WHERE quiz_name = ?", (quiz_name,)).fetchone()

        # If it does, display a message and do not add it.
        if existing_quiz:
            flash(f"Quiz with name {quiz_name} already exists.")
        # Otherwise, try to add it to the database
        else:
            try:
                quiz_sql = "INSERT INTO quiz (quiz_name, close_date) VALUES (?, ?)"
                db.execute(quiz_sql, (quiz_name, close_date))
                db.commit()
                # Display a message to confirm it has been added
                flash('Quiz added!', 'success')
                return redirect(url_for('main.index'))
            except sqlite3.Error as e:
                # If there is an error, display a message and return to the previous form
                flash(f'Error adding quiz: {e}', 'danger')
    return render_template('quiz.html', form=form)


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    # Set the choices for the SelectField
    form.team.choices = get_teams()

    if form.validate_on_submit():
        # Get all values from the form
        year = form.year.data
        team = form.team.data

        # Make the prediction
        prediction = make_prediction(year, team)

        # If the prediction returns an error message rather than a number, print a different message
        if type(prediction) != int:
            prediction_text = f"Sorry, insufficient data to predict a result, please select a different team"
        else:
            prediction_text = f"Prediction: {form.team.data} will win {prediction} medals in {form.year.data}!"

        return render_template(
            "prediction.html", form=form, prediction_text=prediction_text
        )
    return render_template("prediction.html", form=form)


def make_prediction(year, team):
    """Takes the year and team name and predicts how many total medals will be won

    Parameters:
    year (int): The year of the prediction
    team (str): The name of the team

    Returns:
    prediction (str or int): int of the prediction result, or string if error
    """
    # The predict() method fails if not in DataFrame format
    input_data = pd.DataFrame({'Year': [year], 'Team': [team]})

    # Get a prediction from the model
    with importlib.resources.open_binary('data', 'model.pkl') as file:
        model = joblib.load(file)
    try:
        prediction = model.predict(input_data)
        # Returns a float so convert to int and handle negative predictions
        return max(0, int(prediction[0]))
    except Exception as e:
        return f"Error making prediction: {e}"


def get_teams():
    """Get the list of teams for the SelectField in the PredictionForm.

    Returns:
        choices in the format [(value, label), ...]
        """
    db = get_db()
    sql = 'SELECT name FROM Country WHERE member_type != "dissolved"'
    countries = db.execute(sql).fetchall()
    return [(name, name) for name, in countries]
