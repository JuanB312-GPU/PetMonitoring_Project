from sqlalchemy.orm.session import Session
from ..models.pet import Pet, Breed, Species

class PetRepository:

    @staticmethod
    def create(db: Session, pet: Pet):
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet
    
    @staticmethod
    def get_user_pets(db: Session, user_id: int):
        return db.query(Pet).filter(Pet.user_id == user_id).all()
    
    @staticmethod
    def get_pet_by_name_user(db: Session, name: str, user_id: int):
        """FUNCIÓN CRÍTICA FALTANTE - Usada en main.py línea 255"""
        return db.query(Pet).filter(Pet.name == name, Pet.user_id == user_id).first()

    @staticmethod
    def get_species(db: Session):
        return db.query(Species).all()
    
    @staticmethod
    def get_species_by_id(db: Session, species_id: int):
        return db.query(Species).filter(Species.species_id == species_id).first()
    
    @staticmethod
    def get_breeds_by_species(db: Session, species_id: int):
        return db.query(Breed).filter(Breed.species_id == species_id).all()
    
    @staticmethod
    def get_breed_by_id(db: Session, breed_id: int):
        return db.query(Breed).filter(Breed.breed_id == breed_id).first()
    
    @staticmethod
    def create_pet(db: Session, pet: Pet):
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet
