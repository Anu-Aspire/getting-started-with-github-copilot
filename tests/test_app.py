from copy import deepcopy
from fastapi.testclient import TestClient
import pytest

from src import app as app_module

client = TestClient(app_module.app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Restore activities dict before each test to avoid state bleed
    original = deepcopy({
        k: deepcopy(v) for k, v in {
            "Basketball Team": {
                "description": "Join our competitive basketball team and participate in inter-school matches",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 15,
                "participants": ["alex@mergington.edu"]
            },
            "Tennis Club": {
                "description": "Learn tennis skills and compete in friendly tournaments",
                "schedule": "Saturdays, 10:00 AM - 11:30 AM",
                "max_participants": 16,
                "participants": ["james@mergington.edu"]
            },
            "Drama Club": {
                "description": "Perform in school plays and develop acting skills",
                "schedule": "Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 25,
                "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
            },
            "Art Studio": {
                "description": "Explore painting, drawing, and sculpture techniques",
                "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 18,
                "participants": ["mia@mergington.edu"]
            },
            "Debate Club": {
                "description": "Engage in competitive debates and develop critical thinking skills",
                "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
            },
            "Science Club": {
                "description": "Conduct experiments and explore scientific concepts",
                "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 22,
                "participants": ["ryan@mergington.edu"]
            },
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"]
            }
        }.items()
    })
    app_module.activities.clear()
    app_module.activities.update(original)
    yield


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Basketball Team" in data
    assert isinstance(data["Basketball Team"]["participants"], list)


def test_signup_for_activity():
    email = "test.user@example.com"
    activity = "Chess Club"
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in app_module.activities[activity]["participants"]
    assert r.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_already_registered():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 400


def test_signup_unknown_activity():
    r = client.post("/activities/Nonexistent/signup?email=someone@example.com")
    assert r.status_code == 404


def test_unregister_participant():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    r = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
    assert r.json()["message"] == f"Unregistered {email} from {activity}"


def test_unregister_nonexistent_participant():
    email = "nobody@example.com"
    activity = "Chess Club"
    r = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 404


def test_unregister_unknown_activity():
    r = client.delete("/activities/Nope/unregister?email=someone@example.com")
    assert r.status_code == 404
