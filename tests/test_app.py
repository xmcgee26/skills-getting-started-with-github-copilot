import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert activities_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
