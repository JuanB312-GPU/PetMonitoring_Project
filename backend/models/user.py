from sqlalchemy import Column, Integer, String
from ..config.database import Base
import bcrypt

class User(Base):
    __tablename__ = "USER"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password_hash = Column(String)

    def password_to_hash(self, password: str):
        # Hashea la contraseña y la guarda en password_hash
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = hashed.decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        # Verifica si la contraseña coincide con el hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
