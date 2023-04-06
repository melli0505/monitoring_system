from fastapi import FastAPI, Depends, APIRouter

from sqlalchemy.orm import Session
from typing import List

from core.db import schemas
from core.db.base import SessionLocal

from .data_crud import *

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

@router.get("/", response_model=List[schemas.Degree])
def read_degrees(db: Session = Depends(get_db)):
    degrees = get_degree(db=db)
    return degrees

@router.get("/{sensor_num}", response_model=List[schemas.Degree])
def read_degrees_by_sensor_num(sensor_num: int, db: Session = Depends(get_db)):
    degrees = get_degree_by_sensor_num(db=db, sensor_id=sensor_num)
    return degrees

@router.get("/{start}/{end}", response_model=List[schemas.Degree])
def read_degrees_by_date(start: str, end: str, db: Session = Depends(get_db)):
    degrees = get_degree_by_date(db=db, start=start, end=end)
    return degrees