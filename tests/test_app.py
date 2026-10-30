
import pytest

from server.app import create_app
from server.models import db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Workout API is running!"
    }
def test_get_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_exercises(client):
    response = client.get("/exercises")

    assert response.status_code == 200
    assert response.get_json() == []
def test_get_workout_not_found(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404
def test_get_exercise_not_found(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404

def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 45,
            "notes": "Morning workout"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["duration_minutes"] == 45
def test_create_workout_invalid_duration(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": -5,
            "notes": "Invalid workout"
        }
    )

    assert response.status_code == 400
def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Push Up",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "Push Up"

def test_create_exercise_invalid_name(client):
    response = client.post(
        "/exercises",
        json={
            "name": "",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    assert response.status_code == 400
def test_delete_workout(client):
    create_response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 40,
            "notes": "Workout to delete"
        }
    )

    workout_id = create_response.get_json()["id"]

    response = client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout deleted successfully"
    get_response = client.get(f"/workouts/{workout_id}")
    assert get_response.status_code == 404
def test_delete_exercise(client):
    create_response = client.post(
        "/exercises",
        json={
            "name": "Squat",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    exercise_id = create_response.get_json()["id"]

    response = client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Exercise deleted successfully"
    get_response = client.get(f"/exercises/{exercise_id}")
    assert get_response.status_code == 404
def test_add_exercise_to_workout(client):
    workout_response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 45,
            "notes": "Upper body workout"
        }
    )

    exercise_response = client.post(
        "/exercises",
        json={
            "name": "Push Up",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    workout_id = workout_response.get_json()["id"]
    exercise_id = exercise_response.get_json()["id"]

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={
            "sets": 3,
            "reps": 12,
            "duration_seconds": 30
        }
    )

    assert response.status_code == 201
    assert response.get_json()["sets"] == 3
    assert response.get_json()["reps"] == 12
def test_add_exercise_with_negative_reps(client):
    workout_response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 45,
            "notes": "Test workout"
        }
    )

    exercise_response = client.post(
        "/exercises",
        json={
            "name": "Plank",
            "category": "Core",
            "equipment_needed": False
        }
    )

    workout_id = workout_response.get_json()["id"]
    exercise_id = exercise_response.get_json()["id"]

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={
            "sets": 3,
            "reps": -5,
            "duration_seconds": 30
        }
    )

    assert response.status_code == 400
def test_add_exercise_with_negative_sets(client):
    workout_response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 45,
            "notes": "Test workout"
        }
    )

    exercise_response = client.post(
        "/exercises",
        json={
            "name": "Burpees",
            "category": "Cardio",
            "equipment_needed": False
        }
    )

    workout_id = workout_response.get_json()["id"]
    exercise_id = exercise_response.get_json()["id"]

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={
            "sets": -2,
            "reps": 10,
            "duration_seconds": 30
        }
    )

    assert response.status_code == 400
def test_workout_contains_added_exercise(client):
    workout_response = client.post(
        "/workouts",
        json={
            "date": "2026-10-31",
            "duration_minutes": 40,
            "notes": "Upper body training"
        }
    )

    exercise_response = client.post(
        "/exercises",
        json={
            "name": "Push Up",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    workout_id = workout_response.get_json()["id"]
    exercise_id = exercise_response.get_json()["id"]

    client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={
            "sets": 3,
            "reps": 12,
            "duration_seconds": 30
        }
    )

    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["name"] == "Push Up"

