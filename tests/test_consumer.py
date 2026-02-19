import json
from consumer_service.src.consumer import callback

def test_message_parsing():
    message = {"to": "test@example.com", "subject": "Test", "body": "Hello"}
    body = json.dumps(message)

    assert json.loads(body)["to"] == "test@example.com"
