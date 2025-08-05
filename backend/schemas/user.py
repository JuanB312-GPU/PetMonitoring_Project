from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    confirmPassword: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    phone_number: str
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str
