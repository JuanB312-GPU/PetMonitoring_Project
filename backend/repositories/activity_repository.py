from sqlalchemy.orm.session import Session
from ..models.activity import Activity, Feeding
from ..models.relationships import Pet_activity, Pet_feeding

class ActivityRepository:

    @staticmethod
    def get_activities(db: Session):
        return db.query(Activity).all()
    
    @staticmethod
    def get_feedings(db: Session):
        return db.query(Feeding).all()
    
    @staticmethod
    def get_activity_by_id(db: Session, activity_id: int):
        return db.query(Activity).filter(Activity.activity_id == activity_id).first()
    
    @staticmethod
    def get_activities_by_pet(db: Session, pet_id: int):
        return (
            db.query(Activity.name, Pet_activity.weekly_frequency_activity)
            .join(Pet_activity, Activity.activity_id == Pet_activity.activity_id)
            .filter(Pet_activity.pet_id == pet_id)
            .all()
        )
    
    @staticmethod
    def get_feedings_by_pet(db: Session, pet_id: int):
        return (
            db.query(Feeding.name, Pet_feeding.daily_meal_frequency)
            .join(Pet_feeding, Feeding.feeding_id == Pet_feeding.feeding_id)
            .filter(Pet_feeding.pet_id == pet_id)
            .all()
        )
    
    @staticmethod
    def create_pet_activity(db: Session, pet_activity: Pet_activity):
        db.add(pet_activity)
        db.commit()
        db.refresh(pet_activity)
        return True
    
    @staticmethod
    def create_pet_feeding(db: Session, pet_feeding: Pet_feeding):
        db.add(pet_feeding)
        db.commit()
        db.refresh(pet_feeding)
        return True
