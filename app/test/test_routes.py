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

    response = client.get("/get-user")
    assert response.status_code == 200
    assert json.loads(response.data) == expected


# def test_student_courses_page(client):
#     response = client.get("/student/courses")
#     assert response.status_code == 200

# def test_search_course_page(client):
#     response = client.get("/course")
#     assert response.status_code == 200

# def test_course_page(client):
#     response = client.get("/course/514101")
#     assert response.status_code == 200
