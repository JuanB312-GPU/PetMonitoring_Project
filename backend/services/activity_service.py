from sqlalchemy.orm.session import Session
from ..repositories.activity_repository import ActivityRepository
from ..schemas.activity import ActivityCreate, FeedingCreate
from ..models.relationships import Pet_activity, Pet_feeding

class ActivityService:

    @staticmethod
    def create_pet_activity(db: Session, activity_data: ActivityCreate):
        pet_activity = Pet_activity(
            pet_id=activity_data.pet_id,
            activity_id=activity_data.activity_id,
            weekly_frequency_activity=activity_data.frequency
        )
        return ActivityRepository.create_pet_activity(db, pet_activity)

    @staticmethod
    def create_pet_feeding(db: Session, feeding_data: FeedingCreate):
        pet_feeding = Pet_feeding(
            pet_id=feeding_data.pet_id,
            feeding_id=feeding_data.feeding_id,
            daily_meal_frequency=feeding_data.frequency
        )
        return ActivityRepository.create_pet_feeding(db, pet_feeding)

    @staticmethod
    def get_activities_by_pet(db: Session, pet_id: int):
        return ActivityRepository.get_activities_by_pet(db, pet_id)

    @staticmethod
    def get_feedings_by_pet(db: Session, pet_id: int):
        return ActivityRepository.get_feedings_by_pet(db, pet_id)

    @staticmethod
    def get_all_activities(db: Session):
        return ActivityRepository.get_activities(db)

    @staticmethod
    def get_all_feedings(db: Session):
        return ActivityRepository.get_feedings(db)
    
    @staticmethod
    def get_activities(db: Session):
        return ActivityRepository.get_activities(db)

    @staticmethod
    def get_feedings(db: Session):
        return ActivityRepository.get_feedings(db)
