from sqlalchemy import Column, Integer, String, Numeric
from ..config.database import Base

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
