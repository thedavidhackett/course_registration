import pytest
import json

from db import notifications
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


def test_get_student_courses(client):
    response = client.get("/api/student/courses")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 514101 == data['registered'][0]['id']

def test_get_student_notifications(client):
    response = client.get("/api/student/notifications")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["type"] == "info"

def test_delete_notification(client):
    n = notifications.find_one({"student_id": 5})
    id = str(n["_id"])
    response = client.delete(f"/api/notifications/{id}")

    assert response.status_code == 200

    assert not notifications.find_one({"_id": n["_id"]})

def test_course_view(client):
    response = client.get("/api/course-section/514101")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 514101 == data['id']


def test_departments(client):
    response = client.get("/api/departments")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 1 == data[0]['id']

def test_student_restrictions(client):
    response = client.get("/api/student/restrictions")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data == []
