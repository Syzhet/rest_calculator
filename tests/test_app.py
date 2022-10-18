from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index() -> None:
    """Home Page Test."""

    response = client.get('/')
    assert response.status_code == 200
    assert response.text == 'Hello world!'


def test_query_get() -> None:
    """Test get request handler with string parameter."""

    response = client.get(
        '/eval',
        params={'phrase': '(2+2)*2'}
    )
    assert response.status_code == 200
    assert response.text == '(2+2)*2 = 8.0'


def test_fail_query_get() -> None:
    """Test fail get request handler with string parameter."""

    response = client.get(
        '/eval',
        params={'phrase': '(2+2)=2'}
    )
    assert response.status_code == 400
    assert response.text == ('Bad operands or operators')


def test_body_post() -> None:
    """Test post request handler with body parameter."""

    response = client.post(
        '/eval',
        json={'phrase': '(2+2)*2'}
    )
    assert response.status_code == 201
    assert response.json() == {'result': '(2+2)*2 = 8.0'}


def test_fail_body_post() -> None:
    """Test post request handler with body parameter."""

    response = client.post(
        '/eval',
        json={'phrase': '(2+2)=2'}
    )
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad operands or operators'}
