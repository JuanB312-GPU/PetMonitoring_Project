from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..schemas.activity import Activity, Feeding, ActivityCreate, FeedingCreate
from ..services.activity_service import ActivityService
from ..services.pet_service import PetService
from typing import List

router = APIRouter(tags=["activities"])

@router.get("/activities", response_model=List[Activity])
def get_activities(db: Session = Depends(get_db)):
    activities = ActivityService.get_all_activities(db)
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")
    return activities

@router.get("/feedings", response_model=List[Feeding])
def get_feedings(db: Session = Depends(get_db)):
    feedings = ActivityService.get_all_feedings(db)
    if not feedings:
        raise HTTPException(status_code=404, detail="No feedings found")
    return feedings

@router.post("/api/activities", status_code=201)
def create_pet_activity(data: ActivityCreate, db: Session = Depends(get_db)):
    if not PetService.pet_exists(db, data.pet_id):
        raise HTTPException(status_code=404, detail="Pet not found")
    if not ActivityService.activity_exists(db, data.activity_id):
        raise HTTPException(status_code=404, detail="Activity not found")
    try:
        ActivityService.create_pet_activity(db, data)
        return {"message": "Pet activity created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/foods", status_code=201)
def create_pet_feeding(data: FeedingCreate, db: Session = Depends(get_db)):
    if not PetService.pet_exists(db, data.pet_id):
        raise HTTPException(status_code=404, detail="Pet not found")
    if not ActivityService.feeding_exists(db, data.feeding_id):
        raise HTTPException(status_code=404, detail="Feeding not found")
    try:
        ActivityService.create_pet_feeding(db, data)
        return {"message": "Pet feeding created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/activities/pet/{pet_id}")
def get_activities_by_pet(pet_id: int, db: Session = Depends(get_db)):
    if not PetService.pet_exists(db, pet_id):
        raise HTTPException(status_code=404, detail="Pet not found")
        
    activities = ActivityService.get_activities_by_pet(db, pet_id)
    return [{"name": activity[0], "frequency": activity[1]} for activity in activities]

@router.get("/api/foods/pet/{pet_id}")
def get_feedings_by_pet(pet_id: int, db: Session = Depends(get_db)):

    if not PetService.pet_exists(db, pet_id):
        raise HTTPException(status_code=404, detail="Pet not found")

    feedings = ActivityService.get_feedings_by_pet(db, pet_id)
    return [{"name": feeding[0], "frequency": feeding[1]} for feeding in feedings]
