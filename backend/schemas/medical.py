from pydantic import BaseModel

class ConditionOut(BaseModel):
    mc_id: int
    name: str
    description: str
    recommendations: str

class VaccineOut(BaseModel):
    vaccine_id: int
    name: str
    recommended_age: float
