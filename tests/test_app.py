"""
Unit tests for the Mergington High School Management System API
"""

from fastapi.testclient import TestClient
from src.app import app

# Create a test client using the FastAPI application
client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_redirect(self):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestActivitiesEndpoint:
    """Tests for activities listing endpoint"""

    def test_get_activities(self):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_structure(self):
        """Test that activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data


class TestSignupEndpoint:
    """Tests for activity signup endpoint"""

    def test_signup_for_activity(self):
        """Test signing up for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]

    def test_signup_duplicate_error(self):
        """Test that duplicate signup returns error"""
        email = "duplicate@mergington.edu"
        # First signup
        client.post("/activities/Chess Club/signup", params={"email": email})
        # Second signup should fail
        response = client.post("/activities/Chess Club/signup", params={"email": email})
        assert response.status_code == 400

    def test_signup_nonexistent_activity(self):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404


class TestDeleteSignupEndpoint:
    """Tests for removing signup endpoint"""

    def test_delete_signup(self):
        """Test removing a student from an activity"""
        email = "remove@mergington.edu"
        # Sign up first
        client.post("/activities/Tennis Club/signup", params={"email": email})
        # Then remove
        response = client.delete(
            "/activities/Tennis Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_delete_nonexistent_signup(self):
        """Test deleting signup for student not in activity"""
        response = client.delete(
            "/activities/Art Studio/signup",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400