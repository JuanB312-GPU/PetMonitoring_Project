from fastapi import HTTPException
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from connection import SessionLocal, engine
from models import Base
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inserts import BD_inserts
from queries import BD_Queries
from typing import List
from datetime import date


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/components", StaticFiles(directory="components"), name="components")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # O "*" para todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def form():
    with open("index.html") as f:
        return f.read()

# Json Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    confirmPassword: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    phone_number: str

class UserLogin(BaseModel):
    email: str
    password: str

class ConditionOut(BaseModel):
    mc_id: int
    name: str
    description: str
    recommendations: str

class VaccineOut(BaseModel):
    vaccine_id: int
    name: str
    recommended_age: float

class Species(BaseModel):
    species_id: int
    name: str

class Breed(BaseModel):
    breed_id: int
    species_id: int
    name: str

class PetCreate(BaseModel):
    name: str
    user_id: int
    species: int
    breed: int
    birthdate: date
    height: float
    weight: float
    conditions: List[int]
    vaccines: List[int]

class PetOut(BaseModel):   
    id: int
    name: str
    species: str
    breed: str
    birthdate: date
    height: float
    weight: float
    conditions: List[str]
    vaccines: List[str]

@app.post("/api/auth/register")
def create_user(data: UserCreate, db: Session = Depends(get_db)):

    # Validate name, email and phone number.
    verfication_name = BD_Queries.get_by_name(db, data.name)
    verification_email = BD_Queries.get_by_email(db, data.email)
    verification_phone = BD_Queries.get_by_phone(db, data.phone)
    if verfication_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    if verification_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if verification_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    # Create user
    user = BD_inserts.create_user( 
        db, data.name, data.email, data.phone, data.password
    )
    return {"message": "Created", "user": user}

@app.post("/api/auth/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):

    # Validate email and password
    user = BD_Queries.get_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    if not user.verify_password(data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    # If everything is ok, return user data
    return {"message": "Logged", "user": user}

@app.get("/conditions", response_model=list[ConditionOut])
def get_conditions(db: Session = Depends(get_db)):
    return BD_Queries.get_medical_conditions(db)

@app.get("/vaccines", response_model=list[VaccineOut])
def get_vaccines(db: Session = Depends(get_db)):
    return BD_Queries.get_vaccines(db)

@app.get("/species", response_model=list[Species])
def get_species(db: Session = Depends(get_db)):
    return BD_Queries.get_species(db)

@app.get("/breeds/{species_id}", response_model=list[Breed])
def get_breeds_by_species(species_id: int, db: Session = Depends(get_db)):
    return BD_Queries.get_breeds_by_species(db, species_id)

@app.get("/api/pets", response_model=list[PetOut])
def get_pets(user_id: int, db: Session = Depends(get_db)):
    pets = BD_Queries.get_user_pets(db, user_id)

    result = []

    for pet in pets:

        # Get species and breed names
        species = BD_Queries.get_species_by_id(db, pet.species_id)
        breed = BD_Queries.get_breed_by_id(db, pet.breed_id)
        # Get conditions and vaccines
        conditions = BD_Queries.get_conditions_by_pet(db, pet.pet_id)
        vaccines = BD_Queries.get_vaccines_by_pet(db, pet.pet_id)
        conditions_names = [condition.name for condition in conditions]
        vaccines_names = [vaccine.name for vaccine in vaccines]

        result.append(PetOut(
            id=pet.pet_id,
            name=pet.name,
            species=species.name,  
            breed=breed.name,
            birthdate=pet.date_of_birth,
            height=pet.height,
            weight=pet.weight,
            conditions=conditions_names,  
            vaccines=vaccines_names        
        ))

    return result

@app.post("/api/pets")
def create_pet(data: PetCreate, db: Session = Depends(get_db)):
    print(data)

    # Create pet
    pet = BD_inserts.create_pet(
        db, data.name, data.height, data.weight,
        data.birthdate, data.breed, data.species, data.user_id
    )

    # Create pet conditions
    for condition_id in data.conditions:
        BD_inserts.create_pet_medical_condition(
            db, pet.pet_id, condition_id
        )
    
    # Create pet vaccines
    for vaccine_id in data.vaccines:
        BD_inserts.create_pet_vaccine(
            db, pet.pet_id, vaccine_id
        )
    
    # Get species and breed names
    species = BD_Queries.get_species_by_id(db, data.species)
    breed = BD_Queries.get_breed_by_id(db, data.breed)
    # Get conditions and vaccines
    conditions = BD_Queries.get_conditions_by_pet(db, pet.pet_id)
    vaccines = BD_Queries.get_vaccines_by_pet(db, pet.pet_id)
    conditions_names = [condition.name for condition in conditions]
    vaccines_names = [vaccine.name for vaccine in vaccines]

    return {
        "message": "Pet created",
        "pet": {
            "id": pet.pet_id,
            "name": pet.name,
            "species": species.name,
            "breed": breed.name,
            "birthdate": str(pet.date_of_birth),
            "height": float(pet.height),
            "weight": float(pet.weight),
            "conditions": conditions_names,
            "vaccines": vaccines_names
        }}
