import requests

def test_api_running():
    response = requests.post(
        "http://localhost:8000/api/notifications/email",
        json={
            "to": "integration@example.com",
            "subject": "Integration",
            "body": "Integration Test"
        }
    )
    assert response.status_code == 202
