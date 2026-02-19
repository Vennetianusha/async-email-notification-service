from fastapi.testclient import TestClient
from producer_api.src.main import app

client = TestClient(app)

def test_valid_email():
    response = client.post("/api/notifications/email", json={
        "to": "test@example.com",
        "subject": "Test",
        "body": "Test Body"
    })
    assert response.status_code == 202

def test_invalid_email():
    response = client.post("/api/notifications/email", json={
        "to": "wrong-email",
        "subject": "",
        "body": ""
    })
    assert response.status_code == 422
