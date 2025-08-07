import pytest
from fastapi.testclient import TestClient
from main import app  # Ajusta la ruta a tu archivo main.py si es necesario

client = TestClient(app)


def test_get_conditions_success():
    response = client.get("/conditions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("mc_id" in item and "name" in item and "description" in item and "recommendations" in item for item in data)


def test_get_conditions_not_found():

    response = client.get("/conditions")
    assert response.status_code == 404
    assert response.json() == {"detail": "No medical conditions found"}


def test_get_vaccines_success():
    response = client.get("/vaccines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("vaccine_id" in item and "name" in item and "recommended_age" in item for item in data)


def test_get_vaccines_not_found():
   

    response = client.get("/vaccines")
    assert response.status_code == 404
    assert response.json() == {"detail": "No vaccines found"}


def test_get_species_success():
    response = client.get("/species")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("species_id" in item and "name" in item for item in data)


def test_get_species_not_found():
   
    response = client.get("/species")
    assert response.status_code == 404
    assert response.json() == {"detail": "No species found"}


@pytest.mark.parametrize("species_id", [1, 2])
def test_get_breeds_success(species_id):
    response = client.get(f"/breeds/{species_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("breed_id" in item and "species_id" in item and "name" in item for item in data)
    assert all(item["species_id"] == species_id for item in data)


def test_get_breeds_not_found():
   
    response = client.get("/breeds/9999")  # Suponiendo que no existe esa especie
    assert response.status_code == 404
    assert response.json() == {"detail": "No breeds found for this species"}