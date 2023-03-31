from typing import List, Union
from pandas import Timestamp
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class SensorBase(BaseModel):
    timestamp: Timestamp
    sensor_number: int
    value: float

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    administer_id : int

    class Config:
        orm_mode = True