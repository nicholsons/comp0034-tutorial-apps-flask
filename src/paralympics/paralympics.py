import importlib.resources

import joblib
import pandas as pd
import requests
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from paralympics import db
from paralympics.figures import line_chart
from paralympics.forms import PredictionForm, QuizForm
from paralympics.models import Event, Host, HostEvent, Quiz

main = Blueprint('main', __name__)


@main.route('/flash')
def flash_message():
    """Renders a page with a flash message."""
    # Generate a Flash message
    flash('This is a flash message!')
    # Redirect to the homepage, the flash message should be displayed
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    """Renders the home page that is now a list of all paralympics with hyperlinks to the event page for each."""
    # Query the database to get all the events and arrange in date order
    query = db.select(Event.event_id, Event.type, Event.year, Host.host).join(Event.host_events).join(
        HostEvent.host).order_by(Event.type, Event.year)
    events = db.session.execute(query).all()
    return render_template('events.html', events=events)


@main.route('/event/<int:event_id>')
def get_event(event_id):
    """Get event by event_id
    If an event_id is not provided, the first event is returned by default.
    If an invalid event_id is provided, a 404 error is returned.
    """
    query = db.select(Event.type, Event.start, Event.end, Event.highlights, Event.url, Event.year, Host.host).join(
        Event.host_events).join(HostEvent.host).filter(Event.event_id == event_id)
    event = db.session.execute(query).fetchone()
    if event is None:
        abort(404, description="Event not found")
    return render_template('event.html', event=event)


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
    line_fig = line_chart(feature="participants", db=db)
    return render_template('chart.html', fig_html=line_fig)


# TODO: Move quiz to its own blueprint
@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # If the form has been submitted, use the values from it which are accessed using request.form
    form = QuizForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get the values from the form
        quiz_name = form.quiz_name.data
        close_date = form.close_date.data

        # Create a Quiz object
        quiz = Quiz(quiz_name=quiz_name, close_date=close_date)

        # Check it does not already exist.
        existing_quiz = db.session.query(Quiz).filter(Quiz.quiz_name == quiz_name).first()

        # If it does, display a message and do not add it.
        if existing_quiz:
            flash(f"Quiz with name {quiz_name} already exists.")
        # Otherwise, try to add it to the database
        else:
            try:
                db.session.add(quiz)
                db.session.commit()
                # Display a message to confirm it has been added
                flash('Quiz added!', 'success')
                return redirect(url_for('main.index'))
            except Exception as e:
                # If there is an error, display a message and return to the previous form
                flash(f'Error adding quiz: {e}', 'danger')

    return render_template('quiz.html', form=form)


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()

    if form.validate_on_submit():
        # Get all values from the form
        year = form.year.data
        team = form.team.data.name

        # Make the prediction
        prediction = make_prediction(year, team)

        # If the prediction returns an error message rather than a number, print a different message
        if type(prediction) != int:
            prediction_text = f"Sorry, insufficient data to predict a result, please select a different team"
        else:
            prediction_text = f"Prediction: {form.team.data.name} will win {prediction} medals in {form.year.data}!"

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
