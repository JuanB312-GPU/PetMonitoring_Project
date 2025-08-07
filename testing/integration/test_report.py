import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_pet_report_success():
    payload = {
        "petId": 5,
        "reportType": "health_summary",
        "bmiStatus": 1597.2222222222222,
        "date": "2025-08-05"
    }
    response = client.post("/api/reports", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert data["message"] == "Report created successfully"
    assert "report_id" in data

def test_create_pet_report_pet_not_found():
    payload = {
        "petId": 3500,
        "reportType": "health_summary",
        "bmiStatus": 1597.2222222222222,
        "date": "2025-08-05"
    }
    response = client.post("/api/reports", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}

def test_get_user_reports_success():
    response = client.get("/api/reports/34")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for report in data:
        assert "id" in report
        assert "report_type" in report
        assert "created_at" in report
        assert "pet_name" in report
        assert "pet_species" in report
        assert "pet_breed" in report
        assert "pet_weight" in report
        assert "pet_height" in report
        assert "health_metric" in report
        assert isinstance(report["conditions"], list)

def test_get_user_reports_user_not_found():
    response = client.get("/api/reports/200")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
