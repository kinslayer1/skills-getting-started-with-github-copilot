"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_successful_adds_participant(client):
    """Test that a valid signup adds participant to activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify participant was actually added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup to non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    """Test that duplicate signup returns 400 error"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_multiple_participants_same_activity(client):
    """Test that multiple different participants can sign up"""
    # Arrange
    activity_name = "Programming Class"
    emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
    
    # Act
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    final_participants = activities_response.json()[activity_name]["participants"]
    for email in emails:
        assert email in final_participants


def test_signup_same_email_different_activities(client):
    """Test that same student can sign up for multiple different activities"""
    # Arrange
    email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Programming Class", "Art Studio"]
    
    # Act
    for activity_name in activities_to_join:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    for activity_name in activities_to_join:
        assert email in activities_data[activity_name]["participants"]


def test_signup_response_message_format(client):
    """Test that signup response message has correct format"""
    # Arrange
    activity_name = "Drama Club"
    email = "actor@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()
    
    # Assert
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
