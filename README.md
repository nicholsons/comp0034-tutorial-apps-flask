# COMP0034 2025 Computer practicals (Flask app)

These are worked examples of the activities. 

They are not coursework exemplars!

The sub-packages are:

| Package            | Description                                                                 | Command line to run                                        |
|:-------------------|:----------------------------------------------------------------------------|:-----------------------------------------------------------| 
| `data`             | the database and data files for paralympics app                             | N/A                                                        |
| `paralympics`      | Flask activities in weeks 6-9 (SQLAlchemy from week 7 on).                  | `flask --app paralympics run --debug`                      |
| `paralympics_sq3`  | Flask activities weeks 7-9 (sqlite3 instead of SQLAlchemy)                  | See below. Initialise the database before running the app. |
| `ex_flasklogin`    | Simple example using Flask-Login                                            | `flask --app ex_flasklogin run --debug`                    |
| `ex_jwtextended`   | Simple example using Flask-JWT-Extended                                     | `flask --app ex_jwtextended run --debug`                   |
| `ex-mlmodel`       | Simple example of an app with a machine learning prediction (Iris data set) | `flask --app ex_mlmodel run --debug`                       |
| `ex_dash_in_flask` | Simple example hosting a Dash app inside a Flask app                        | `flask --app ex_dash_in_flask run --debug`                 |


For the SQLite3 version you need
to [initialise the database](https://flask.palletsprojects.com/en/stable/tutorial/database/#initialize-the-database-file)
before running the app for the first time. Once the database is created in `instance/paralympics.sqlite` you don't need
to create it again.

1. Initialise the database: `flask --app paralympics_sq3 init-db`
2. Run the app: `flask --app paralympics_sq3 run --debug`
