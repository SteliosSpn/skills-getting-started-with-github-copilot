import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "pytest@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup_resp.status_code in (200, 400)  # 400 if already signed up

    # Try duplicate signup
    dup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json().get("detail", "")

    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister_resp.status_code == 200
    assert "unregistered" in unregister_resp.json().get("message", "")

    # Unregister again (should fail)
    unregister_again = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister_again.status_code == 400
    assert "not registered" in unregister_again.json().get("detail", "")
