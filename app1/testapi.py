from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_mail():
    response = client.post("/gmail?email=dipusharma868%40gmail.com")
    assert response.status_code == 200
    assert response.json() == {
        "message": "email has been sent",
    }
