from sqlalchemy.orm.session import Session
from ..repositories.medical_repository import MedicalRepository

class MedicalService:

    @staticmethod
    def get_medical_conditions(db: Session):
        return MedicalRepository.get_medical_conditions(db)

    @staticmethod
    def get_vaccines(db: Session):
        return MedicalRepository.get_vaccines(db)

    @staticmethod
    def get_conditions_by_pet(db: Session, pet_id: int):
        return MedicalRepository.get_conditions_by_pet(db, pet_id)

    @staticmethod
    def get_vaccines_by_pet(db: Session, pet_id: int):
        return MedicalRepository.get_vaccines_by_pet(db, pet_id)
    
    @staticmethod
    def get_species(db: Session):
        return MedicalRepository.get_species(db)
    
    @staticmethod
    def get_breeds_by_species(db: Session, species_id: int):
        return MedicalRepository.get_breeds_by_species(db, species_id)
