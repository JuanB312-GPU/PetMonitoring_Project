import pytest
from fastapi.testclient import TestClient
from main import app  # Asegúrate de ajustar este import a tu proyecto real

client = TestClient(app)


def test_create_pet_success():
    pet_data = {
        "name": "Tita2",
        "user_id": 34,
        "species": "1",
        "breed": "1",
        "birthdate": "2024-10-09",
        "height": 20,
        "weight": 20,
        "conditions": [3, 4, 5],
        "vaccines": [4, 5, 6]
    }

    response = client.post("/api/pets", json=pet_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tita1"
    assert "species" in data
    assert "breed" in data
    assert isinstance(data["conditions"], list)
    assert isinstance(data["vaccines"], list)


def test_create_pet_repeated_name():
    # Se asume que ya existe una mascota con nombre "Bob" y user_id=1
    pet_data = {
        "name": "Tita2",
        "user_id": 34,
        "species": "1",
        "breed": "1",
        "birthdate": "2019-02-11",
        "height": 21,
        "weight": 22,
        "conditions": [3],
        "vaccines": [5]
    }

    response = client.post("/api/pets", json=pet_data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Pet with this name already exists"}


def test_create_pet_user_not_found():
    pet_data = {
        "name": "Ghosty",
        "user_id": 9999,  # ID inexistente
        "species": "1",
        "breed": "1",
        "birthdate": "2023-10-09",
        "height": 25,
        "weight": 10,
        "conditions": [],
        "vaccines": []
    }

    response = client.post("/api/pets", json=pet_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_pets_success():
    response = client.get("/api/pets/?user_id=34")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for pet in data:
        assert "id" in pet
        assert "name" in pet
        assert "species" in pet
        assert "breed" in pet
        assert "birthdate" in pet
        assert "height" in pet
        assert "weight" in pet
        assert isinstance(pet["conditions"], list)
        assert isinstance(pet["vaccines"], list)


def test_get_pets_user_not_found():
    # Simula que el usuario activo no existe

    response = client.get("/api/pets/?user_id=9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}