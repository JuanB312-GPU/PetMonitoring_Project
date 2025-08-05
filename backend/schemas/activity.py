from pydantic import BaseModel

class Activity(BaseModel):
    activity_id: int
    name: str
    description: str

class ActivityCreate(BaseModel):
    pet_id: int
    activity_id: int
    frequency: int  # Assuming frequency is an integer representing weeks

class Feeding(BaseModel):
    feeding_id: int
    name: str
    description: str
    calories: float

class FeedingCreate(BaseModel):
    pet_id: int
    feeding_id: int
    frequency: int  # Assuming frequency is an integer representing days
