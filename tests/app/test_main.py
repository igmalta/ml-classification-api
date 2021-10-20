# Test app main components.
# python -m pytest tests/app/test_main.py

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import models


def test_index():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Successful operation"


def test_construct_response():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.request.method == "GET"
        assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def example_user():
    user = {
        "email": "adminnxns@gmxail.com",
        "first_name": "Juan",
        "last_name": "Perez",
        "password": "123456",
    }
    return user


def test_not_exists_user(example_user):
    assert models.User.objects(email=example_user["email"]).first() is None


def test_create_user(example_user):
    with TestClient(app) as client:
        response = client.post("/users/", data=example_user)
        assert response.request.method == "POST"
        assert response.status_code == status.HTTP_201_CREATED


def test_exits_user(example_user):
    assert models.User.objects(email=example_user["email"]).first() is not None


def test_login(example_user):
    data = {"username": example_user["email"], "password": example_user["password"]}
    with TestClient(app) as client:
        response = client.post("/login/", data=data)
        assert response.request.method == "POST"
        assert response.status_code == status.HTTP_200_OK
        global token
        token = response.json()["access_token"]
        assert len(token) > 0


def test_remove_user(example_user):
    models.User.objects(email=example_user["email"]).delete()
    assert models.User.objects(email=example_user["email"]).first() is None


def test_not_authorized_nlp():
    with TestClient(app) as client:
        response = client.post("/nlp/")
        assert response.request.method == "POST"
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_nlp():
    params = {
        "sequence": "One day I will see the world",
        "candidate_labels": ["travel", "cooking", "dancing"],
    }
    with TestClient(app) as client:
        response = client.post("/nlp/", json=params, headers={"Authorization": f"Bearer {token}"})
        assert response.request.method == "POST"
        assert response.status_code == status.HTTP_200_OK
