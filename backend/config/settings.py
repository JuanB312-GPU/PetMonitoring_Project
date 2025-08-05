import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/PetMonitoring")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:8000,http://localhost:8000").split(",")

settings = Settings()
