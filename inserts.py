from pydantic import BaseModel
from models import User, Pet, History_register, Pet_medical_condition, Pet_vaccine

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
    def create_history_register(db, pet_id, date, body_metric):
        history = History_register(
            pet_id=pet_id,
            date=date,
            body_metric=body_metric
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
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