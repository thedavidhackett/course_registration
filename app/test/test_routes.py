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

def test_register_with_lab_no_lab(client):
    response = client.post("/api/register", data=json.dumps({"course_section_id": 513001}),\
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert len(data['options']) == 2


def test_register_with_lab(client):
    response = client.post("/api/register", data=json.dumps({"course_section_id": 513001, "lab_id": 5130001}),\
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['msg'] == "You successfully registered for 513001 - Compliers"


def test_register_full(client):
    response = client.post("/api/register", data=json.dumps({"course_section_id": 514102}),\
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert len(data['options']) == 1

def test_register_tentative(client):
    response = client.post("/api/register/tentative", data=json.dumps({"course_section_id": 512301}),\
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['msg'] == "Your registration for 512301 - User Interface and User Experience Design is tentative"
    assert notifications.find_one({"instructor_id": 2})


def test_register_pending(client):
    response = client.post("/api/register/pending", data=json.dumps({"course_section_id": 410001}),\
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['msg'] == "Your registration for 410001 - Ulysses is pending"
    assert notifications.find_one({"instructor_id": 3})
