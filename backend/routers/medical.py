from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..services.medical_service import MedicalService
from pydantic import BaseModel
from typing import List

# Schemas específicos para medical
class ConditionOut(BaseModel):
    mc_id: int
    name: str
    description: str
    recommendations: str

class VaccineOut(BaseModel):
    vaccine_id: int
    name: str
    recommended_age: float

router = APIRouter(tags=["medical"])

@router.get("/conditions", response_model=List[ConditionOut])
def get_conditions(db: Session = Depends(get_db)):
    conditions = MedicalService.get_medical_conditions(db)
    if not conditions:
        raise HTTPException(status_code=404, detail="No conditions found")
    return conditions

@router.get("/vaccines", response_model=List[VaccineOut])
def get_vaccines(db: Session = Depends(get_db)):
    vaccines = MedicalService.get_vaccines(db)
    if not vaccines:
        raise HTTPException(status_code=404, detail="No vaccines found")
    return vaccines
