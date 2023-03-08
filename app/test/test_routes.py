import pytest
import json

from app import create_app

@pytest.fixture()
def app():
    app = create_app(testing=True)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_user(client):
    expected = {
        "id" : 5,
        "name" : "Foo Bar",
        "level" : "graduate"
    }

    response = client.get("/api/get-user")
    assert response.status_code == 200
    assert json.loads(response.data) == expected


def test_student_courses_page(client):
    response = client.get("/api/student/courses")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 514101 == data['registered'][0]['id']
