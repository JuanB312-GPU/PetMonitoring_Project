from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from connection import Base
import bcrypt
from datetime import date

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
    
class Pet(Base):

    __tablename__ = "pet"

    pet_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Numeric(2, 1))
    height = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    date_of_birth = Column(Date) # Assuming Date is imported from datetime
    breed_id = Column(Integer)  # Foreign key to Breed table
    species_id = Column(Integer)  # Foreign key to species table
    user_id = Column(Integer)  # Foreign key to User table

    def calculate_age(birthdate: date) -> int:
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

class Breed(Base):
    __tablename__ = "breed"

    breed_id = Column(Integer, primary_key=True, index=True)
    species_id = Column(Integer)  # Foreign key to species table
    name = Column(String)

class Species(Base):
    __tablename__ = "species"

    species_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Medical_condition(Base):
    __tablename__ = "medical_condition"

    mc_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    recommendations = Column(String)

class Vaccine(Base):
    __tablename__ = "vaccine"

    vaccine_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    recommended_age = Column(Numeric(2, 1))  # Assuming age is in years

class Activity(Base):
    __tablename__ = "activity"

    activity_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Feeding(Base):
    __tablename__ = "feeding"

    feeding_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    calories = Column(Numeric(6, 2))

class Pet_medical_condition(Base):
    __tablename__ = "pet_mc"

    pet_id = Column(Integer, ForeignKey("pet.pet_id"), primary_key=True)  # Foreign key to Pet table
    mc_id = Column(Integer, ForeignKey("medical_condition.mc_id"), primary_key=True)  # Foreign key to Medical_condition table

class Pet_vaccine(Base):
    __tablename__ = "pet_vaccine"

    pet_id = Column(Integer, ForeignKey("pet.pet_id"), primary_key=True)
    vaccine_id = Column(Integer, ForeignKey("vaccine.vaccine_id"), primary_key=True)

class Pet_activity(Base):
    __tablename__ = "pet_activity"

    pet_id = Column(Integer, ForeignKey("pet.pet_id"), primary_key=True)
    activity_id = Column(Integer, ForeignKey("activity.activity_id"), primary_key=True)
    weekly_frequency_activity = Column(Integer)  # Assuming frequency is stored as an integer (e.g., number of times per week)

class Pet_feeding(Base):
    __tablename__ = "pet_feeding"

    pet_id = Column(Integer, ForeignKey("pet.pet_id"), primary_key=True)
    feeding_id = Column(Integer, ForeignKey("feeding.feeding_id"), primary_key=True)
    daily_meal_frequency = Column(Integer)  # Assuming frequency is stored as an integer (e.g., number of times per day)

class Pet_history(Base):
    __tablename__ = "history_register"

    hr_id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer)
    date = Column(Date)  # Date of the history record
    body_metric = Column(Numeric(2, 1))  # Body metric value (e.g., weight, BMI, etc.)

