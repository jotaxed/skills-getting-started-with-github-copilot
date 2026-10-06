from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregistering_participant_removes_their_email():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregistering_unknown_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "unknown@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
