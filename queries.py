from models import User, Medical_condition, Vaccine, Breed, Species, Pet_medical_condition, Pet_vaccine, Pet, Activity, Feeding, Pet_activity, Pet_feeding
from sqlalchemy.orm import Session

class BD_Queries:

    @staticmethod
    def get_by_name(db, name: str):
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def get_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_phone(db, phone: str):
        return db.query(User).filter(User.phone_number == phone).first()
    
    @staticmethod
    def get_medical_conditions(db):
        return db.query(Medical_condition).all()
    
    @staticmethod
    def get_vaccines(db):
        return db.query(Vaccine).all()
    
    @staticmethod
    def get_breeds_by_species(db, species_id: int):
        return db.query(Breed).filter(Breed.species_id == species_id).all()
    
    @staticmethod
    def get_species(db):
        return db.query(Species).all()
    
    @staticmethod
    def get_species_by_id(db, species_id: int):
        return db.query(Species).filter(Species.species_id == species_id).first()
    
    @staticmethod
    def get_breed_by_id(db, breed_id: int):
        return db.query(Breed).filter(Breed.breed_id == breed_id).first()
    
    @staticmethod
    def get_condition_by_id(db, condition_id: int):
        return db.query(Medical_condition).filter(Medical_condition.mc_id == condition_id).first()
    
    @staticmethod
    def get_vaccine_by_id(db, vaccine_id: int):
        return db.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    
    @staticmethod
    def get_conditions_by_pet(db, pet_id: int):
        return db.query(Medical_condition).join(Pet_medical_condition).filter(Pet_medical_condition.pet_id == pet_id).all()
    
    @staticmethod
    def get_vaccines_by_pet(db, pet_id: int):
        return db.query(Vaccine).join(Pet_vaccine).filter(Pet_vaccine.pet_id == pet_id).all()
    
    @staticmethod
    def get_user_pets(db, user_id: int):
        return db.query(Pet).filter(Pet.user_id == user_id).all()
    
    @staticmethod
    def get_activities(db):
        return db.query(Activity).all()
    
    @staticmethod
    def get_activity_by_id(db, activity_id: int):
        return db.query(Activity).filter(Activity.activity_id == activity_id).first()
    
    @staticmethod
    def get_feedings(db):
        return db.query(Feeding).all()
    
    @staticmethod
    def get_activities_by_pet(db, pet_id: int):
        return (
            db.query(Activity.name, Pet_activity.weekly_frequency_activity)
            .join(Pet_activity, Activity.activity_id == Pet_activity.activity_id)
            .filter(Pet_activity.pet_id == pet_id)
            .all()
        )
    
    @staticmethod
    def get_feedings_by_pet(db, pet_id: int):
        return (
            db.query(Feeding.name, Pet_feeding.daily_meal_frequency)
            .join(Pet_feeding, Feeding.feeding_id == Pet_feeding.feeding_id)
            .filter(Pet_feeding.pet_id == pet_id)
            .all()
        )