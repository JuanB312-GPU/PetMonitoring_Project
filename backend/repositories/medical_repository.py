from sqlalchemy.orm.session import Session
from ..models.medical import Medical_condition, Vaccine
from ..models.relationships import Pet_medical_condition, Pet_vaccine

class MedicalRepository:

    @staticmethod
    def get_medical_conditions(db: Session):
        return db.query(Medical_condition).all()
    
    @staticmethod
    def get_vaccines(db: Session):
        return db.query(Vaccine).all()
    
    @staticmethod
    def get_condition_by_id(db: Session, condition_id: int):
        return db.query(Medical_condition).filter(Medical_condition.mc_id == condition_id).first()
    
    @staticmethod
    def get_vaccine_by_id(db: Session, vaccine_id: int):
        return db.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    
    @staticmethod
    def get_conditions_by_pet(db: Session, pet_id: int):
        return db.query(Medical_condition).join(Pet_medical_condition).filter(Pet_medical_condition.pet_id == pet_id).all()
    
    @staticmethod
    def get_vaccines_by_pet(db: Session, pet_id: int):
        return db.query(Vaccine).join(Pet_vaccine).filter(Pet_vaccine.pet_id == pet_id).all()
    
    @staticmethod
    def get_species(db: Session):
        from ..models.pet import Species
        return db.query(Species).all()
    
    @staticmethod
    def get_breeds_by_species(db: Session, species_id: int):
        from ..models.pet import Breed
        return db.query(Breed).filter(Breed.species_id == species_id).all()
    
    @staticmethod
    def get_species_by_id(db: Session, species_id: int):
        from ..models.pet import Species
        return db.query(Species).filter(Species.species_id == species_id).first()
    
    @staticmethod
    def get_breed_by_id(db: Session, breed_id: int):
        from ..models.pet import Breed
        return db.query(Breed).filter(Breed.breed_id == breed_id).first()
    
    @staticmethod
    def create_pet_medical_condition(db: Session, pet_condition: Pet_medical_condition):
        db.add(pet_condition)
        db.commit()
        db.refresh(pet_condition)
        return True
    
    @staticmethod
    def create_pet_vaccine(db: Session, pet_vaccine: Pet_vaccine):
        db.add(pet_vaccine)
        db.commit()
        db.refresh(pet_vaccine)
        return True
