from fastapi.testclient import TestClient
from main import app  # Asegúrate de importar correctamente tu FastAPI app

client = TestClient(app)

def test_login_success():
    # Primero registramos un usuario válido
    client.post("/api/auth/register", json={
        "name": "Ana312",
        "email": "ana@example.com",
        "phone": "3103012052",
        "password": "123456",
        "confirmPassword": "123456"
    })

    # Luego hacemos login con ese usuario
    response = client.post("/api/auth/login", json={
        "email": "ana@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()
    print("/n",20)
    print(data)  # Para depuración
    print("/n",20)
    assert data['user']['email'] == "ana@example.com"
    assert data['user']['name']== "Ana312"
    assert "user_id" in data['user']

def test_login_invalid_email():
    response = client.post("/api/auth/login", json={
        "email": "noexiste@example.com",
        "password": "123456"
    })

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}

def test_login_wrong_password():
    # Crear el usuario primero
    client.post("/api/auth/register", json={
        "name": "Jose",
        "email": "jose@example.com",
        "phone": "3103000000",
        "password": "correctpass",
        "confirmPassword": "correctpass"
    })

    # Intentar login con contraseña incorrecta
    response = client.post("/api/auth/login", json={
        "email": "jose@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}