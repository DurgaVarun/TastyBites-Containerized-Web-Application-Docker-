import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_login_page(client):
    assert client.get("/").status_code == 200


def test_register_page(client):
    assert client.get("/register").status_code == 200


def test_contact_page(client):
    assert client.get("/Contact.html").status_code == 200
