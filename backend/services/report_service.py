from sqlalchemy.orm.session import Session
from ..repositories.report_repository import ReportRepository
from ..schemas.reports import PetHistory
from ..models.relationships import Pet_history

class ReportService:

    @staticmethod
    def create_report(db: Session, report_data: PetHistory):
        pet_history = Pet_history(
            pet_id=report_data.petId,
            date=report_data.date,
            body_metric=report_data.bmiStatus
        )
        return ReportRepository.create_pet_history(db, pet_history)

    @staticmethod
    def get_pet_reports_for_user(db: Session, user_id: int):
        return ReportRepository.get_pet_reports_for_user(db, user_id)
