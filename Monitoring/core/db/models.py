from sqlalchemy import Boolean, Column, ForeignKey,  Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    disable = Column(Boolean, index=True, default=True)

class Degree(Base):
    __tablename__ = "degrees"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    degree = Column(Float, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    sensor = relationship("Sensor", back_populates="degrees")

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    administer_id = Column(Integer, ForeignKey("users.id"))
    degrees = relationship("Degree", back_populates="sensor")

