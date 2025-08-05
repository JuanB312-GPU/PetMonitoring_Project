from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Date, Numeric
from ..config.database import Base

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
    pet_id = Column(Integer, ForeignKey("pet.pet_id"))
    date = Column(Date)  # Date of the history record
    body_metric = Column(Numeric(2, 1))  # Body metric value (e.g., weight, BMI, etc.)
