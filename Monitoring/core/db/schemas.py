from typing import List, Union
from pandas import Timestamp
from pydantic import BaseModel

# data
class DegreeBase(BaseModel):
    time: Timestamp
    degree: float
    sensor_id: int

class DegreeCreate(DegreeBase):
    pass

class Degree(DegreeBase):
    id: int
    class Config:
        orm_mode = True

# sensor
class SensorBase(BaseModel):
    id: int

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    administer_id : int = 1
    degrees : List[Degree] = []
    class Config:
        orm_mode = True

# user
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    email: str = None
    hashed_password: str
    sensors: List[Sensor] = []

    class Config:
        orm_mode = True