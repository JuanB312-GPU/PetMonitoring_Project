from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session
from backend.config.database import Base, engine, get_db
from backend.config.settings import settings
from backend.routers import auth, pets, medical, activities, reports
from backend.services.medical_service import MedicalService

# Crear tablas solo si no estamos en modo de importación
import os
if not os.environ.get('SKIP_DB_INIT'):
    try:
        Base.metadata.create_all(bind=engine)  # type: ignore
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"⚠️  Advertencia: No se pudo conectar a la base de datos: {e}")
        print("🔧 La aplicación se ejecutará en modo sin base de datos")
        # Establecer variable de entorno para evitar reconexiones
        os.environ['SKIP_DB_INIT'] = 'true'

app = FastAPI(title="PetCare Monitor API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/components", StaticFiles(directory="components"), name="components")

# Include routers
app.include_router(auth.router)
app.include_router(pets.router)
app.include_router(medical.router)
app.include_router(activities.router)
app.include_router(reports.router)

@app.get("/", response_class=HTMLResponse)
def serve_index():
    try:
        with open("index.html", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback para manejar problemas de codificación
        with open("index.html", encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found</h1>"

# Para mantener compatibilidad con las rutas del frontend sin prefijo /api
@app.get("/species")
def get_species_legacy(db: Session = Depends(get_db)):

    if not MedicalService.get_species(db):
        raise HTTPException(status_code=404, detail="No species found")
    return MedicalService.get_species(db)

@app.get("/breeds/{species_id}")
def get_breeds_legacy(species_id: int, db: Session = Depends(get_db)):

    if not MedicalService.get_breeds_by_species(db, species_id):
        raise HTTPException(status_code=404, detail="No breeds found for this species")
    return MedicalService.get_breeds_by_species(db, species_id)

@app.get("/conditions")
def get_conditions_legacy(db: Session = Depends(get_db)):

    if not MedicalService.get_medical_conditions(db):
        raise HTTPException(status_code=404, detail="No medical conditions found")
    return MedicalService.get_medical_conditions(db)

@app.get("/vaccines")
def get_vaccines_legacy(db: Session = Depends(get_db)):

    if not MedicalService.get_vaccines(db):
        raise HTTPException(status_code=404, detail="No vaccines found")
    return MedicalService.get_vaccines(db)

@app.get("/activities")
def get_activities_legacy(db: Session = Depends(get_db)):
    from backend.services.activity_service import ActivityService
    return ActivityService.get_all_activities(db)

@app.get("/feedings")
def get_feedings_legacy(db: Session = Depends(get_db)):
    from backend.services.activity_service import ActivityService
    return ActivityService.get_all_feedings(db)
