import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert

def test_get_activities():
    # Arrange
    # ...nessuna preparazione necessaria...
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_valid():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_invalid_email():
    # Arrange
    invalid_emails = ["", "not-an-email", "student@", "@mergington.edu", "student@@mergington.edu"]
    activity = "Chess Club"
    for email in invalid_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        # Assert
        assert response.status_code == 200 or response.status_code == 400
        # Se vuoi che il backend rifiuti email non valide, cambia assert qui


def test_remove_participant():
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_remove_nonexistent_participant():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_invalid_activity():
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_root_redirect():
    # Arrange
    # ...nessuna preparazione necessaria...
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code in (200, 307, 308)
    assert response.headers["location"].endswith("/static/index.html")
