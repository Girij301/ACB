from fastapi.testclient import TestClient

from app.main import app



def test_list_executions(client):
    response = client.get("/executions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_execution_not_found(client):
    response = client.get("/executions/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution not found."


def test_get_execution_steps_not_found(client):
    response = client.get("/executions/999999/steps")

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution not found."


def test_get_validation_records_not_found(client):
    response = client.get("/executions/999999/validations")

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution not found."


def test_get_retry_records_not_found(client):
    response = client.get("/executions/999999/retries")

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution not found."


def test_get_debug_records_not_found(client):
    response = client.get("/executions/999999/debug")

    assert response.status_code == 404
    assert response.json()["detail"] == "Execution not found."
