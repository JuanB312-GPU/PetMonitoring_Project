from pydantic import BaseModel
from models import User, Pet, Pet_medical_condition, Pet_vaccine, Pet_activity, Pet_feeding, Pet_history

class BD_inserts(BaseModel):
    
    @staticmethod
    def create_user(db, name, email, phone, password):
        user = User(
            name=name,
            email=email,
            phone_number=phone
        )
        # Hash the password
        user.password_to_hash(password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def create_pet(db, name, height, weight, date_of_birth, breed, species, user_id):
        age = Pet.calculate_age(date_of_birth)
        pet = Pet(
            name=name,
            age= age,
            height=height,
            weight=weight,
            date_of_birth=date_of_birth,
            breed_id=breed,
            species_id=species,
            user_id=user_id
        )
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet
    
    @staticmethod
    def create_pet_medical_condition(db, pet_id, mc_id):
        pet_condition = Pet_medical_condition(
            pet_id=pet_id,
            mc_id=mc_id
        )
        db.add(pet_condition)
        db.commit()
        db.refresh(pet_condition)
        return True
    
    @staticmethod
    def create_pet_vaccine(db, pet_id, vaccine_id):
        pet_vaccine = Pet_vaccine(
            pet_id=pet_id,
            vaccine_id=vaccine_id
        )
        db.add(pet_vaccine)
        db.commit()
        db.refresh(pet_vaccine)
        return True
    
    @staticmethod
    def create_pet_activity(db, pet_id, activity_id, frequency):
        pet_activity = Pet_activity(
            pet_id=pet_id,
            activity_id=activity_id,
            weekly_frequency_activity=frequency
        )
        db.add(pet_activity)
        db.commit()
        db.refresh(pet_activity)
        return True
    
    @staticmethod
    def create_pet_feeding(db, pet_id, feeding_id, frequency):
        pet_feeding = Pet_feeding(
            pet_id=pet_id,
            feeding_id=feeding_id,
            daily_meal_frequency =frequency
        )
        db.add(pet_feeding)
        db.commit()
        db.refresh(pet_feeding)
        return True

    @staticmethod
    def create_pet_history(db, pet_id, date, body_metric):
        pet_history = Pet_history(
            pet_id=pet_id,
            date=date,
            body_metric=body_metric
        )
        db.add(pet_history)
        db.commit()
        db.refresh(pet_history)
        return pet_history
