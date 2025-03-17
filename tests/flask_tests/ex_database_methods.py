# Approaches to handling the database changes in Flask app testing
# Partially complete code to illustrate the concepts. The code will not run as is.

# 1. Create a test database
import pytest
from my_flask_app import create_app, db

@pytest.fixture
def app():
    # Database can be in memory or saved tofile
    # app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_example(client):
    response = client.get('/')
    assert response.status_code == 200


# 2. Use a transaction to handle database changes
# This code still creates the database but uses a transaction to handle database changes.
import pytest
from my_flask_app import create_app, db

@pytest.fixture(scope='session')
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session({'bind': connection})
    yield session
    transaction.rollback()
    connection.close()

def test_example(session):
    # Perform database operations using the session
    pass

# 3. Approach that ensures any database interaction is inside a request context
# App and db are in 2 separate fixtures but could be combined
# https://agallagher.net/coding/flask_sqlalchemy_pytest/
@pytest.fixture(scope='session')
def app_ctx(app):
	with app.app_context():
		yield


@pytest.fixture(scope='session')
def db(app, app_ctx):
	_db.app = app
	_db.create_all()

	yield _db

	_db.drop_all()


@pytest.fixture(scope='function')
def session(app, db, app_ctx):
	connection = db.engine.connect()
	transaction = connection.begin()

	session = db._make_scoped_session(options={'bind': connection})
	db.session = session

	yield session

	transaction.rollback()
	connection.close()
	session.remove()


def test0_write_to_database(example_row0, session):
	session.add(example_row0)
	session.commit()

	out = select(ExampleTable).where(ExampleTable.row_name == 'row_value')
	result = session.execute(out).all()

	assert len(result) == 1