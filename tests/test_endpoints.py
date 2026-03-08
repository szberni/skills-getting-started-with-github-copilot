def test_signup_success(client):
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up test@example.com for Chess Club"
    # Verify added to participants
    activities_response = client.get("/activities")
    assert "test@example.com" in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate(client):
    # First signup
    client.post("/activities/Chess%20Club/signup?email=test@example.com")
    # Attempt duplicate
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Signup first
    client.post("/activities/Chess%20Club/signup?email=test@example.com")
    response = client.delete("/activities/Chess%20Club/participants?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Removed test@example.com from Chess Club"
    # Verify removed
    activities_response = client.get("/activities")
    assert "test@example.com" not in activities_response.json()["Chess Club"]["participants"]


def test_remove_participant_not_found(client):
    response = client.delete("/activities/Chess%20Club/participants?email=nonexistent@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_activity_not_found(client):
    response = client.delete("/activities/NonExistent/participants?email=test@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"