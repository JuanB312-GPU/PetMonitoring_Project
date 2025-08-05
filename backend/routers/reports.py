from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..schemas.reports import PetHistory, ReportResponse
from ..services.report_service import ReportService
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
        
        # Validar que el pet_id existe
        if not data.petId or data.petId <= 0:
            raise HTTPException(status_code=400, detail="Invalid pet ID")
        
        # Validar BMI
        if data.bmiStatus is None or data.bmiStatus < 0:
            raise HTTPException(status_code=400, detail="Invalid BMI status")
            
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
        
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user ID")
            
        reports = ReportService.get_pet_reports_for_user(db, user_id)
        logger.info(f"Found {len(reports)} reports for user {user_id}")
        
        return reports  # Devolver lista vacía si no hay reportes
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting reports for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
