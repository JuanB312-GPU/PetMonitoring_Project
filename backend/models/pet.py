from sqlalchemy import Column, Integer, String, Date, Numeric
from ..config.database import Base
from datetime import date

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

    @staticmethod
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
