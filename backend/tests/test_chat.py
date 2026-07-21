from unittest.mock import patch


@patch("app.api.chat.service.generate_response")
def test_chat_endpoint(mock_generate_response, client):

    mock_generate_response.return_value = "Hello! How can I help you?"

    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "message": "hello",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["response"] == "Hello! How can I help you?"