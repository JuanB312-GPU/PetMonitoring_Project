from pydantic import BaseModel
from datetime import date
from typing import List

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
