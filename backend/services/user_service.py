from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin
from ..models.user import User

class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        # Check if user with email already exists
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="A user with this email already exists")
        
        # Check if user with phone already exists
        existing_user_phone = UserRepository.get_by_phone(db, user_data.phone)
        if existing_user_phone:
            raise HTTPException(status_code=400, detail="A user with this phone number already exists")
        
        # Check if passwords match
        if user_data.password != user_data.confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        # Create new user
        user = User(
            name=user_data.name,
            email=user_data.email,
            phone_number=user_data.phone
        )
        # Hash the password
        user.password_to_hash(user_data.password)
        
        return UserRepository.create_user(db, user)

    @staticmethod
    def login_user(db: Session, user_data: UserLogin):
        # Get user by email
        user = UserRepository.get_by_email(db, user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not user.verify_password(user_data.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return UserRepository.get_by_email(db, email)
