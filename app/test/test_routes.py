import pytest

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


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
