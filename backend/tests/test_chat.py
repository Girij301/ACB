from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "hello"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "success" in data
    assert "data" in data
    assert "response" in data["data"]