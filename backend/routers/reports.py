from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..schemas.reports import PetHistory, ReportResponse
from ..services.report_service import ReportService
from ..services.user_service import UserService
from ..services.pet_service import PetService
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.options("/{user_id}")
def options_reports(user_id: int):
    """Handle preflight requests for CORS"""
    return {}

@router.post("")
def create_report(data: PetHistory, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating report for pet {data.petId} with BMI {data.bmiStatus}")
        
        # Validar que la mascota existe
        if not PetService.pet_exists(db, data.petId):
            raise HTTPException(status_code=404, detail="Pet not found")
            
        report = ReportService.create_report(db, data)
        logger.info(f"Report created successfully with ID {report.hr_id}")
        
        return {"message": "Report created successfully", "report_id": report.hr_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{user_id}", response_model=List[ReportResponse])
def get_reports_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Getting reports for user {user_id}")

        # Validar que el usuario existe
        user_service = UserService.get_user_by_id(db, user_id)
        if not user_service:
            raise HTTPException(status_code=404, detail="User not found")
            
        reports = ReportService.get_pet_reports_for_user(db, user_id)
        logger.info(f"Found {len(reports)} reports for user {user_id}")
        
        return reports  # Devolver lista vacía si no hay reportes
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting reports for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
