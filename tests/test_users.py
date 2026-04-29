import requests
import os
from dotenv import load_dotenv
from utils.auth import get_token

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def test_get_profile_success():
    token = get_token()

    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "user" in data["data"]


def test_get_profile_no_token():
    response = requests.get(f"{BASE_URL}/users/me")

    assert response.status_code in [401, 403]


def test_get_profile_invalid_token():
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )

    assert response.status_code in [401, 403]


def test_get_profile_malformed_token():
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={"Authorization": "Bearer "}
    )

    assert response.status_code in [401, 403]


def test_get_profile_wrong_method():
    token = get_token()

    response = requests.post(
        f"{BASE_URL}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [400, 404, 405]

   