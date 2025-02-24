# COMP0034 2025 Computer practicals (Flask app)

These are worked examples of the activities. They are not coursework exemplars!

The sub-packages are:

- `data`: the database and data files
- `flask_para`: Flask activities in weeks 6-9 (SQLAlchemy from week 7 on)
- `flask_para_sq3`: Flask activities weeks 7-9 (sqlite3 instead of SQLAlchemy)

Run commands:

- `flask --app flask_para run --debug`

For the SQLite3 version you need
to [initialise the database](https://flask.palletsprojects.com/en/stable/tutorial/database/#initialize-the-database-file)
before running the app for the first time. Once the database is created in `instance/paralympics.sqlite` you don't need
to create it again.

1. Initialise the database: `flask --app flask_para_sq3 init-db`
2. Run the app: `flask --app flask_para_sq3 run --debug`
