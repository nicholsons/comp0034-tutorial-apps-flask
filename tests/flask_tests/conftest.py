import importlib.resources
import os

import pytest
from paralympics import create_app, db
from sqlalchemy.orm import Session


@pytest.fixture(scope='session')
def app():
    """Fixture that creates a test app.

    The app is created with test config parameters that include a test database.
    The app is created once for each test session.

    Returns:
        app A Flask app with a test config
    """
    # Location for the temporary testing database
    db_path = importlib.resources.files('data') / 'paralympics_testdb.sqlite'
    db_path_str = str(db_path)
    # a test config, this will overide the default config in the create_app function
    test_cfg = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path_str,
        "WTF_CSRF_ENABLED": False
    }
    app = create_app(test_config=test_cfg)

    yield app

    # clean up / reset resources
    with app.app_context():
        # Close the database session before deleting
        db.session.remove()
        db.engine.dispose()
    os.unlink(db_path_str)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Creates a new database session for a test.

    Creates a new database session for each test function.
    Begins a transaction before each test and rolls it back afterward to ensure no changes persist between tests.
    """

    with app.app_context():
        connection = db.engine.connect()

        # begin a non-ORM transaction
        transaction = connection.begin()

        # bind an individual Session to the connection
        db_session = Session(bind=connection)
        yield db_session

        db_session.close()
        transaction.rollback()
        connection.close()
