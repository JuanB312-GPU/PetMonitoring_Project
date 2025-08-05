from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class PetHistory(BaseModel):
    petId: int
    bmiStatus: float
    date: date

class ReportResponse(BaseModel):
    id: int
    report_type: str
    created_at: date
    pet_name: str
    pet_species: str
    pet_breed: str
    pet_weight: float
    pet_height: float
    health_metric: float
    conditions: List[str]
