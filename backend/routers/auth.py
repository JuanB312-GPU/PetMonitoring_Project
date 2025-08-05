from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from ..config.database import get_db
from ..schemas.user import UserCreate, UserLogin, UserOut
from ..services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_user(db, data)
    # Retornar un diccionario directamente para evitar problemas de tipo
    return {
        "user_id": user.user_id,  # type: ignore
        "name": user.name,  # type: ignore
        "email": user.email,  # type: ignore
        "phone_number": user.phone_number  # type: ignore
    }

@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.login_user(db, data)
    return {
        "message": "Login successful", 
        "user": {
            "user_id": user.user_id,  # type: ignore
            "name": user.name,  # type: ignore
            "email": user.email  # type: ignore
        }
    }
