"""Tests for POST /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_successful_removes_participant(client):
    """Test that a valid unregister removes participant from activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify participant was actually removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregister from non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_enrolled_participant_returns_400(client):
    """Test that unregistering non-enrolled participant returns 400"""
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"  # Not signed up for this
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_then_signup_same_participant(client):
    """Test that a participant can unregister and sign up again"""
    # Arrange
    activity_name = "Drama Club"
    email = "jessica@mergington.edu"
    
    # Act - Unregister
    unregister_response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert unregister succeeded
    assert unregister_response.status_code == 200
    
    # Act - Sign up again
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert signup succeeded
    assert signup_response.status_code == 200
    
    # Verify participant was re-added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_unregister_updates_participant_count(client):
    """Test that participant count decreases after unregister"""
    # Arrange
    activity_name = "Art Studio"
    email = "lucas@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count - 1


def test_unregister_response_message_format(client):
    """Test that unregister response message has correct format"""
    # Arrange
    activity_name = "Math Olympiad"
    email = "ryan@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    data = response.json()
    
    # Assert
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_multiple_participants_from_activity(client):
    """Test that unregistering one participant doesn't affect others"""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email_to_remove}")
    
    # Assert
    assert response.status_code == 200
    
    # Verify specific participant removed but other remains
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants
