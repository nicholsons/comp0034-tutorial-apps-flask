import pytest

from ex_formwithselect.formwithselect import app


@pytest.fixture
def client():
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_submit(client):
    response = client.post('/', data={
        'select_field': 'blue',
        'radio_field': 'one'
    })
    assert b'You chose select: blue, radio: one' in response.data
