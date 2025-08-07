import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_activities_success():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for activity in data:
        assert "activity_id" in activity
        assert "name" in activity
        assert "description" in activity

def test_get_activities_not_found():
    # Simulate no activities found
    
    response = client.get("/activities")
    assert response.status_code == 404
    assert response.json() == {"detail": "No activities found"}

def test_get_feedings_success():
    response = client.get("/feedings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for feeding in data:
        assert "feeding_id" in feeding
        assert "name" in feeding
        assert "description" in feeding
        assert "calories" in feeding

def test_get_feedings_not_found():
    
    response = client.get("/feedings")
    assert response.status_code == 404
    assert response.json() == {"detail": "No feedings found"}

def test_create_pet_activity_success():
    payload = {
        "activity_id": "7",
        "frequency": "10",
        "pet_id": "5"
    }
    response = client.post("/api/activities", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Pet activity created successfully"}

def test_create_pet_activity_activity_not_found():
    payload = {
        "activity_id": "12",
        "frequency": "10",
        "pet_id": "5"
    }
    response = client.post("/api/activities", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_create_pet_activity_pet_not_found():
    payload = {
        "activity_id": "10",
        "frequency": "10",
        "pet_id": "9999"
    }
    response = client.post("/api/activities", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}

def test_create_pet_feeding_success():
    payload = {
        "feeding_id": "7",
        "frequency": "10",
        "pet_id": "5"
    }
    response = client.post("/api/foods", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Pet feeding created successfully"}

def test_create_pet_feeding_feeding_not_found():
    payload = {
        "feeding_id": "20",
        "frequency": "10",
        "pet_id": "5"
    }
    response = client.post("/api/foods", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Feeding not found"}

def test_create_pet_feeding_pet_not_found():
    payload = {
        "feeding_id": "10",
        "frequency": "10",
        "pet_id": "9999"
    }
    response = client.post("/api/foods", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}

def test_get_pet_activities_success():
    response = client.get("/api/activities/pet/5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for activity in data:
        assert "name" in activity
        assert "frequency" in activity

def test_get_pet_activities_pet_not_found():
    response = client.get("/api/activities/pet/2500")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}

def test_get_pet_feedings_success():
    response = client.get("/api/foods/pet/5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for feeding in data:
        assert "name" in feeding
        assert "frequency" in feeding

def test_get_pet_feedings_pet_not_found():
    response = client.get("/api/foods/pet/2300")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}