""" This version of the app only has the routes that have database interaction. """
import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from paralympics_sq3.db import get_db
from paralympics_sq3.forms import QuizForm

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
            'WHERE event.event_id = ?', (event_id,)).fetchone()
        return render_template('event.html', event=event)
    except sqlite3.Error as e:
        abort(404, "No event found with that id")


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
