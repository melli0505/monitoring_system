from fastapi import FastAPI, Depends, APIRouter

from sqlalchemy.orm import Session
from typing import List

from core.db import schemas
from core.db.base import SessionLocal

from .data_crud import *

from mqtt.pzem_pub import publish_control

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/api/data',
    tags=['data']
)

@router.get("/voltage", response_model=List[schemas.Voltage])
def read_voltage(db: Session = Depends(get_db)):
    return get_voltage(db=db)

@router.get("/energy", response_model=List[schemas.Energy])
def read_energy(db: Session = Depends(get_db)):\
    return get_energy(db=db)

@router.get("/current", response_model=List[schemas.Current])
def read_current(db: Session = Depends(get_db)):
    return get_current(db=db)

@router.get("/power", response_model=List[schemas.Power])
def read_power(db: Session = Depends(get_db)):
    return get_power(db=db)

@router.get("/pf", response_model=List[schemas.PF])
def read_pf(db: Session = Depends(get_db)):
    return get_pf(db=db)

@router.get("/frequency", response_model=List[schemas.Frequency])
def read_frequency(db: Session = Depends(get_db)):
    return get_frequency(db=db)


@router.get("/voltage/{start}/{end}", response_model=List[schemas.Voltage])
def read_degrees_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_voltage_by_date(db=db, start=start, end=end)

@router.get("/energy/{start}/{end}", response_model=List[schemas.Energy])
def read_energy_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_energy_by_date(db=db, start=start, end=end)

@router.get("/current/{start}/{end}", response_model=List[schemas.Current])
def read_current_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_current_by_date(db=db, start=start, end=end)

@router.get("/power/{start}/{end}", response_model=List[schemas.Power])
def read_power_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_power_by_date(db=db, start=start, end=end)

@router.get("/pf/{start}/{end}", response_model=List[schemas.PF])
def read_pf_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_pf_by_date(db=db, start=start, end=end)

@router.get("/frequency/{start}/{end}", response_model=List[schemas.Frequency])
def read_frequency_by_date(start: str, end: str, db: Session = Depends(get_db)):
    return get_frequency_by_date(db=db, start=start, end=end)


@router.get("/reset_energy_counter")
def reset_energy_counter():
    publish_control("reset")
    return True