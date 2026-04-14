"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_returns_all_activities(client):
    """Test that /activities returns all activities with correct structure"""
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_returns_correct_structure(client):
    """Test that activity objects have required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_details in data.items():
        assert isinstance(activity_name, str)
        assert set(activity_details.keys()) == required_fields
        assert isinstance(activity_details["participants"], list)
        assert isinstance(activity_details["max_participants"], int)


def test_get_activities_shows_initial_participants(client):
    """Test that activities show initially enrolled participants"""
    # Arrange
    expected_chess_club_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert data["Chess Club"]["participants"] == expected_chess_club_participants


def test_get_activities_has_all_activity_names(client):
    """Test that all expected activities are present"""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
        "Basketball Club", "Drama Club", "Art Studio", "Debate Team", "Math Olympiad"
    ]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity in expected_activities:
        assert activity in data


def test_get_activities_schedule_is_string(client):
    """Test that schedule field is a string for all activities"""
    # Arrange
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["schedule"], str)
        assert len(activity_details["schedule"]) > 0
