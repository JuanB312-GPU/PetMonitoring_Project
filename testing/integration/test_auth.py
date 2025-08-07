from fastapi.testclient import TestClient
from main import app  # Asegúrate de importar correctamente tu FastAPI app

client = TestClient(app)
def test_register_user_success():
    # Datos válidos para el registro
    payload = {
        "name": "Ana312",
        "email": "ana@example.com",
        "phone": "3103012052",
        "password": "123456",
        "confirmPassword": "123456"
    }

    # Enviar la solicitud POST al endpoint
    response = client.post("/api/auth/register", json=payload)

    # Validar el código de estado esperado
    assert response.status_code == 201

    # Validar contenido de la respuesta
    data = response.json()

    assert data['user']['email'] == "ana@example.com"
    assert data['user']['name'] == "Ana312"
    assert data['user']['phone_number'] == "3103012052"
    assert "password_hash" in data.user
    assert "user_id" in data.user

def test_register_user_email_conflict():
    # Primer registro exitoso
    client.post("/api/auth/register", json={
        "name": "Carlos23",
        "email": "sharkm12@example.com",
        "phone": "3103012052",
        "password": "joseph.",
        "confirmPassword": "joseph."
    })

    # Segundo intento con el mismo email
    response = client.post("/api/auth/register", json={
        "name": "Ana312",
        "email": "sharkm12@example.com",  # Mismo email
        "phone": "3103015010",
        "password": "123456",
        "confirmPassword": "123456"
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "A user with this email already exists"}

def test_register_user_phone_conflict():
    # Registro original
    client.post("/api/auth/register", json={
        "name": "Carlos23",
        "email": "carlosx@example.com",
        "phone": "3103012052",
        "password": "joseph.",
        "confirmPassword": "joseph."
    })

    # Nuevo registro con mismo teléfono
    response = client.post("/api/auth/register", json={
        "name": "Ana312",
        "email": "ana612@example.com",
        "phone": "3103012052",  # Teléfono repetido
        "password": "123456",
        "confirmPassword": "123456"
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "A user with this phone number already exists"}

def test_register_user_name_conflict():
    # Registro original
    client.post("/api/auth/register", json={
        "name": "PetLover43",
        "email": "canyd12312@example.com",
        "phone": "3142986790",
        "password": "joseph.",
        "confirmPassword": "joseph."
    })

    # Segundo intento con mismo nombre
    response = client.post("/api/auth/register", json={
        "name": "PetLover43",  # Nombre repetido
        "email": "tiger34@example.com",
        "phone": "3103012052",
        "password": "123456",
        "confirmPassword": "123456"
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "A user with this name already exists"}