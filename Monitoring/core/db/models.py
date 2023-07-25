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

class Voltage(Base):
    __tablename__ = "voltages"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    voltage = Column(Float, index=True)

class Current(Base):
    __tablename__ = "currents"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    current = Column(Float, index=True)

class Power(Base):
    __tablename__ = "powers"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    power = Column(Float, index=True)

class Energy(Base):
    __tablename__ = "energies"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    energy = Column(Float, index=True)

class PF(Base):
    __tablename__ = "pfs"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    pf = Column(Float, index=True)

class Frequency(Base):
    __tablename__ = "frequencies"
    
    id = Column(Integer, primary_key=True, index = True)
    time = Column(TIMESTAMP, index=True)
    frequency = Column(Float, index=True)

# class Sensor(Base):
#     __tablename__ = "sensors"

#     id = Column(Integer, primary_key=True, index=True)
#     administer_id = Column(Integer, ForeignKey("users.id"))
#     degrees = relationship("Degree", back_populates="sensor")

