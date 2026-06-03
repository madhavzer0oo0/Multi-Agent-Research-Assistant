import requests

BASE_URL = "http://localhost:8000"


def register(email, password):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": email,
            "password": password
        }
    )


def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

def create_report(token, topic):
    return requests.post(
        f"{BASE_URL}/reports",
        json={"topic": topic},
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_reports(token):
    return requests.get(
        f"{BASE_URL}/reports",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )