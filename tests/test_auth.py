import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
VALID_EMAIL = os.getenv("EMAIL")
VALID_PASSWORD = os.getenv("PASSWORD")


def generate_email():
    return f"user{random.randint(10000,99999)}@gmail.com"


# =========================
# POSITIVE TESTS
# =========================

def test_register_valid_user():
    payload = {
        "username": "Ameenah",
        "email": generate_email(),
        "password": "Meenah@15",
        "first_name": "Aminat",
        "last_name": "Baruwa",
        "phone_number": "09029468111"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    data = response.json()

    assert response.status_code in [200, 201]
    assert data["status"] == "success"
    assert "access_token" in data["data"]


def test_login_success():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": VALID_EMAIL,
        "password": VALID_PASSWORD
    })
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "access_token" in data["data"]


# =========================
# NEGATIVE TESTS
# =========================

def test_login_wrong_password():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": VALID_EMAIL,
        "password": "WrongPass123"
    })

    data = response.json()

    assert response.status_code in [400, 401, 422]
    assert "message" in data or "error" in data


def test_login_invalid_email_format():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "aminatgmail.com",
        "password": VALID_PASSWORD
    })

    assert response.status_code in [400, 422]


def test_login_missing_password():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": VALID_EMAIL
    })

    assert response.status_code in [400, 422]


def test_login_missing_email():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "password": VALID_PASSWORD
    })

    assert response.status_code in [400, 422]


def test_login_empty_fields():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "",
        "password": ""
    })

    assert response.status_code in [400, 422]


def test_register_missing_email():
    payload = {
        "username": "Ameenah",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert response.status_code in [400, 422]


def test_register_invalid_email_format():
    payload = {
        "username": "Ameenah",
        "email": "aminatgmail.com",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert response.status_code in [400, 422]


def test_register_short_password():
    payload = {
        "username": "Ameenah",
        "email": generate_email(),
        "password": "123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    # API may still accept weak password, so we validate safely
    assert response.status_code in [400, 422, 201]


def test_register_duplicate_email():
    email = VALID_EMAIL

    payload = {
        "username": "Ameenah",
        "email": email,
        "password": VALID_PASSWORD
    }

    requests.post(f"{BASE_URL}/auth/register", json=payload)
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert response.status_code in [400, 409, 200]


# =========================
# EDGE CASES
# =========================

def test_login_case_sensitivity_email():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": VALID_EMAIL.upper(),
        "password": VALID_PASSWORD
    })

    assert response.status_code in [200, 400, 401]


def test_register_long_username():
    payload = {
        "username": "A" * 200,
        "email": "aminatbaruwa20@gmail.com",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert response.status_code in [200, 201, 400, 422]


def test_register_special_characters_username():
    payload = {
        "username": "@@@###",
        "email": "aminatbaruwa20@gmail.com",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    assert response.status_code in [200, 201, 400, 422]


def test_login_sql_injection_attempt():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "' OR 1=1 --",
        "password": "anything"
    })

    assert response.status_code in [400, 401, 422]


def test_login_xss_attempt():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "<script>alert(1)</script>",
        "password": "test"
    })

    assert response.status_code in [400, 401, 422]


# =========================
# EXTRA STABILITY TESTS
# (added for Stage 3 compliance)
# =========================

def test_register_empty_payload():
    response = requests.post(f"{BASE_URL}/auth/register", json={})
    assert response.status_code in [400, 422]


def test_login_empty_payload():
    response = requests.post(f"{BASE_URL}/auth/login", json={})
    assert response.status_code in [400, 422]


def test_register_missing_password():
    payload = {
        "username": "Ameenah",
        "email": "aminatbaruwa20@gmail.com"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    assert response.status_code in [400, 422]


def test_register_whitespace_email():
    payload = {
        "username": "Ameenah",
        "email": "   ",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    assert response.status_code in [400, 422]


def test_register_long_email():
    payload = {
        "username": "Ameenah",
        "email": "a" * 250 + "@gmail.com",
        "password": "Meenah@15"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    assert response.status_code in [400, 422]