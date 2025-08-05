from sqlalchemy.orm.session import Session
from ..models.user import User

class UserRepository:

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_phone(db: Session, phone: str):
        return db.query(User).filter(User.phone_number == phone).first()
    
    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def create(db: Session, user: User):
        """Alias para create_user - usado por UserService"""
        return UserRepository.create_user(db, user)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()
