from .models import User, Sensor, Degree
from .schemas import Degree, DegreeBase, DegreeCreate, Sensor, SensorBase, SensorCreate, User, UserBase, UserCreate
from .base import Base, SessionLocal, engine