from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from ..repositories.pet_repository import PetRepository
from ..repositories.medical_repository import MedicalRepository
from ..schemas.pet import PetCreate
from ..models.pet import Pet
from ..models.relationships import Pet_medical_condition, Pet_vaccine

class PetService:

    @staticmethod
    def create_pet(db: Session, pet_data: PetCreate):
        # VALIDACIÓN CRÍTICA: Verificar si la mascota ya existe
        existing_pet = PetRepository.get_pet_by_name_user(db, pet_data.name, pet_data.user_id)
        if existing_pet:
            raise HTTPException(status_code=409, detail="Pet with this name already exists")

        # Calcular edad usando la función estática del modelo original
        age = Pet.calculate_age(pet_data.birthdate)
        
        # Crear pet exactamente como en el original
        pet = Pet(
            name=pet_data.name,
            age=age,  # type: ignore
            height=pet_data.height,  # type: ignore
            weight=pet_data.weight,  # type: ignore
            date_of_birth=pet_data.birthdate,
            breed_id=pet_data.breed,  # type: ignore
            species_id=pet_data.species,  # type: ignore
            user_id=pet_data.user_id  # type: ignore
        )
        
        # Guardar pet
        pet = PetRepository.create(db, pet)
        
        # Crear condiciones médicas (EXACTO al original)
        for condition_id in pet_data.conditions:
            pet_condition = Pet_medical_condition(
                pet_id=pet.pet_id,  # type: ignore
                mc_id=condition_id
            )
            db.add(pet_condition)
        
        # Crear vacunas (EXACTO al original)
        for vaccine_id in pet_data.vaccines:
            pet_vaccine = Pet_vaccine(
                pet_id=pet.pet_id,  # type: ignore
                vaccine_id=vaccine_id
            )
            db.add(pet_vaccine)
        
        db.commit()
        
        return pet

    @staticmethod
    def get_user_pets(db: Session, user_id: int):
        pets = PetRepository.get_user_pets(db, user_id)
        
        if not pets:
            # Devolver lista vacía en lugar de lanzar excepción
            return []

        result = []
        for pet in pets:
            # Obtener información exactamente como en el original
            species = PetRepository.get_species_by_id(db, pet.species_id)  # type: ignore
            breed = PetRepository.get_breed_by_id(db, pet.breed_id)  # type: ignore
            conditions = MedicalRepository.get_conditions_by_pet(db, pet.pet_id)  # type: ignore
            vaccines = MedicalRepository.get_vaccines_by_pet(db, pet.pet_id)  # type: ignore
            
            conditions_names = [condition.name for condition in conditions]
            vaccines_names = [vaccine.name for vaccine in vaccines]

            result.append({
                "id": pet.pet_id,  # type: ignore
                "name": pet.name,  # type: ignore
                "species": species.name if species else "Unknown",  
                "breed": breed.name if breed else "Unknown",
                "birthdate": pet.date_of_birth,  # type: ignore
                "height": pet.height,  # type: ignore
                "weight": pet.weight,  # type: ignore
                "conditions": conditions_names,  
                "vaccines": vaccines_names        
            })

        return result
