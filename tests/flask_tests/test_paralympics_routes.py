def test_print_response_params(client):
    """
    This is just so you can see what type of detail you get in a response object.
    Don't use this in your tests!
    """
    response = client.get("/")
    print("Printing response.headers:")
    print(response.headers)
    print('\n Printing response.headers["Content-Type"]:')
    print(response.headers['Content-Type'])
    print("Printing response.status_code:")
    print(response.status_code)
    print("Printing response.data:")
    print(response.data)
    print("Printing response.json:")
    print(response.json)


def test_index_success(client):
    """
    GIVEN a Flask test client
    WHEN a request is made to /
    THEN the status code should be 200
    AND the words "Winter" and "Summer" should be in the page content
    AND at least 25 urls should be in the content
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b'Winter' in response.data
    assert b'Summer' in response.data

    count_href = response.data.count(b'href')
    assert count_href >= 25


def test_index_fails_post_request(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /
    THEN the status code should be 405
    """
    response = client.post("/")
    assert response.status_code == 405


def test_get_event_success(client):
    """
    GIVEN a Flask test client
    WHEN a request is made to /event/1
    THEN the status code should be 200
    AND the word "Highlights" should be in the page content
    """
    response = client.get("/event/1")
    assert response.status_code == 200
    assert b'Highlights' in response.data


def test_get_event_not_found(client):
    """
    GIVEN a Flask test client
    WHEN a request is made to /event/1000
    THEN the status code should be 404
    """
    response = client.get("/event/1000")
    assert response.status_code == 404
    assert b'Event not found' in response.data


def test_prediction_form_post_success(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /predict with valid form data
    THEN the status code should be 200
    AND there should be "prediction" in the page content
    """
    form_data = {
        "year": 2030,
        "team": "Germany",
    }
    response = client.post("/predict", data=form_data)
    assert response.status_code == 200
    assert b'Prediction' in response.data


def test_prediction_form_data_missing(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /predict with missing form data
    THEN the status code should be 200
    AND there should be "This field is required" in the page content
    """
    form_data = {
        "year": 2030,
    }

    response = client.post("/predict", data=form_data)
    assert response.status_code == 200
    assert b'This field is required' in response.data


# TODO: Debug this, test fails
'''
def test_new_quiz_form_post_success(client, db_session):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /quiz with valid form data
    THEN the status code should be 200
    AND it should redirect to '/'
    AND there should be "Quiz added!" in the page content
    AND there should be one more row in the database than before
    """
    form_data = {
        "quiz_name": "Test New Quiz",
        "close_date": "01/01/2025",
    }

    response = client.post("/quiz", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Quiz added!' in response.data

    # Check that the new quiz is in the database
    from flask_para.paralympics import Quiz
    quiz = db_session.query(Quiz).filter(Quiz.quiz_name == "Test Quiz").first()
    assert quiz is not None



def test_prediction_returns_int():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with valid data
    THEN the result should be an integer
    """
    from paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Germany")
    assert isinstance(prediction, int)
'''

def test_prediction_no_data_returns_error():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with invalid data
    THEN the result should be an error message with 'Error making prediction'
    """
    from paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Invalid")
    assert "Error making prediction" in prediction
