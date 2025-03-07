from flask import Blueprint, render_template

from ex_reflection import db
from ex_reflection.models import Area

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Query the database to get all the areas
    query = db.select(Area.name).order_by(Area.name)
    areas = db.session.execute(query).fetchall()
    return render_template("index.html", areas=areas)
