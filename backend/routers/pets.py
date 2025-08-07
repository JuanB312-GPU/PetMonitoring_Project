from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..schemas.pet import PetCreate, PetOut, Species, Breed
from ..services.pet_service import PetService
from ..repositories.pet_repository import PetRepository
from ..services.user_service import UserService
from typing import List

router = APIRouter(prefix="/api/pets", tags=["pets"])

@router.get("", response_model=List[PetOut])
def get_pets(user_id: int, db: Session = Depends(get_db)):
    # Validar que el usuario existe
    user_service = UserService.get_user_by_id(db, user_id)  
    if not user_service:
        raise HTTPException(status_code=404, detail="User not found")
    pets = PetService.get_user_pets(db, user_id)
    return pets

@router.post("",status_code=status.HTTP_201_CREATED)
def create_pet(data: PetCreate, db: Session = Depends(get_db)):
    try:
        pet = PetService.create_pet(db, data)
        return {"message": "Pet created successfully", "pet_id": pet.pet_id}  # type: ignore
    except HTTPException as http_exc:
        raise http_exc  # Re-lanzar tal cual

@router.get("/species", response_model=List[Species])
def get_species(db: Session = Depends(get_db)):
    species = PetRepository.get_species(db)
    if not species:
        raise HTTPException(status_code=404, detail="No species found")
    return species

@router.get("/breeds/{species_id}", response_model=List[Breed])
def get_breeds_by_species(species_id: int, db: Session = Depends(get_db)):
    breeds = PetRepository.get_breeds_by_species(db, species_id)
    if not breeds:
        raise HTTPException(status_code=404, detail="No breeds found for this species")
    return breeds
