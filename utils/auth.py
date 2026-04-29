import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def get_token():
    url = f"{BASE_URL}/auth/login"

    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data["data"]["access_token"]