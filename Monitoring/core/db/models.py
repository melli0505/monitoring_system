from sqlalchemy import Boolean, Column, ForeignKey,  Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, index=True)
    sensor_number = Column(Integer, index=True)
    value = Column(Float, index= True)
    administer_id = Column(Integer, ForeignKey("users.id"))
    
    # administer = relationship("User", back_populates="sensors")