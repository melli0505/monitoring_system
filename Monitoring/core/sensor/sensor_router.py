from typing import List
from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from core.user import user_crud
from core.sensor import sensor_crud

from core.db import schemas
from core.db.base import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/api/sensor',
    tags=['sensor']
)

# sensor
@router.post("/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, username: str, db: Session = Depends(get_db)):
    exist_sensor = user_crud.get_sensor(db=db, id=sensor.id)
    if exist_sensor:
        raise HTTPException(status_code=400, detail="Sensor id already exist")
    user = user_crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="Could not found user")
    return sensor_crud.create_sensor(db=db, sensor=sensor, user=user)

@router.get("/", response_model=List[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = sensor_crud.get_sensors(db=db, skip=skip, limit=limit)
    return sensors

@router.get("/sensor_info")
def read_sensor_info(db: Session = Depends(get_db)):
    sensor = sensor_crud.get_sensor_info(db=db)
    return sensor

@router.get("/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = sensor_crud.get_sensor(db=db, id=sensor_id)
    return sensor
