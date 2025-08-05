from sqlalchemy import Column, Integer, String, Numeric
from ..config.database import Base

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
