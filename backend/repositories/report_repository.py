from sqlalchemy.orm.session import Session
from typing import List, Dict, Any
from ..models.relationships import Pet_history
from ..models.pet import Pet, Breed, Species
from ..models.medical import Medical_condition
from ..models.relationships import Pet_medical_condition

class ReportRepository:

    @staticmethod
    def create_pet_history(db: Session, pet_history: Pet_history) -> Pet_history:
        try:
            db.add(pet_history)
            db.commit()
            db.refresh(pet_history)
            return pet_history
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_pet_reports_for_user(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """FUNCIÓN COMPLETA COPIADA DEL ORIGINAL - CRÍTICA PARA REPORTES"""
        if not db or user_id is None:
            return []
            
        try:
            pets = db.query(Pet).filter(Pet.user_id == user_id).all()  # type: ignore

            reports = []
            for pet in pets:
                # Get species and breed info
                species = db.query(Species).filter(Species.species_id == pet.species_id).first()  # type: ignore
                breed = db.query(Breed).filter(Breed.breed_id == pet.breed_id).first()  # type: ignore

                # Get last history record
                last_history = (
                    db.query(Pet_history)  # type: ignore
                    .filter(Pet_history.pet_id == pet.pet_id)
                    .order_by(Pet_history.date.desc())
                    .first()
                )

                # Get medical conditions
                condition_ids = (
                    db.query(Pet_medical_condition.mc_id)  # type: ignore
                    .filter(Pet_medical_condition.pet_id == pet.pet_id)
                    .all()
                )
                condition_ids = [cid[0] for cid in condition_ids] if condition_ids else []
                
                if condition_ids:
                    conditions = (
                        db.query(Medical_condition.name)  # type: ignore
                        .filter(Medical_condition.mc_id.in_(condition_ids))
                        .all()
                    )
                else:
                    conditions = []
                condition_names = [c[0] for c in conditions]

                if last_history:
                    reports.append({
                        "id": last_history.hr_id,
                        "report_type": "health_summary",
                        "created_at": last_history.date.isoformat(),
                        "pet_name": pet.name,
                        "pet_species": species.name if species else "Unknown",
                        "pet_breed": breed.name if breed else "Unknown",
                        "pet_weight": pet.weight,
                        "pet_height": pet.height,
                        "health_metric": last_history.body_metric,
                        "conditions": condition_names
                    })

            return reports
        except Exception as e:
            print(f"Error getting pet reports: {e}")
            return []
