from fastapi.testclient import TestClient
from src.app import app

# Initialize the activities dictionary
app.activities = {}

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    activity_name = "test_activity"
    email = "test@example.com"

    # Create a test activity
    app.state.activities[activity_name] = {
        "description": "A test activity",
        "schedule": "Monday 10am",
        "max_participants": 10,
        "participants": []
    }

    # Sign up for the activity
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Check that the participant was added
    assert email in app.state.activities[activity_name]["participants"]

def test_signup_duplicate():
    activity_name = "test_activity"
    email = "test@example.com"

    # Attempt to sign up the same participant again
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"