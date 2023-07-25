from typing import List, Union
from pandas import Timestamp
from pydantic import BaseModel

# Voltage
class VoltageBase(BaseModel):
    time: Timestamp
    voltage: float

class VoltageCreate(VoltageBase):
    pass

class Voltage(VoltageBase):
    id: int
    class Config:
        orm_mode = True

# Current
class CurrentBase(BaseModel):
    time: Timestamp
    current: float

class CurrentCreate(CurrentBase):
    pass

class Current(CurrentBase):
    id: int
    class Config:
        orm_mode = True

# Power
class PowerBase(BaseModel):
    time: Timestamp
    power: float

class PowerCreate(PowerBase):
    pass

class Power(PowerBase):
    id: int
    class Config:
        orm_mode = True

# Energy
class EnergyBase(BaseModel):
    time: Timestamp
    energy: float

class EnergyCreate(EnergyBase):
    pass

class Energy(EnergyBase):
    id: int
    class Config:
        orm_mode = True

# PF
class PFBase(BaseModel):
    time: Timestamp
    pf: float

class PFCreate(PFBase):
    pass

class PF(PFBase):
    id: int
    class Config:
        orm_mode = True

# Frequency
class FrequencyBase(BaseModel):
    time: Timestamp
    frequency: float

class FrequencyCreate(FrequencyBase):
    pass

class Frequency(FrequencyBase):
    id: int
    class Config:
        orm_mode = True

# user
class UserBase(BaseModel):
    username: str
    email: str = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str
    disable: bool = False

    class Config:
        orm_mode = True

