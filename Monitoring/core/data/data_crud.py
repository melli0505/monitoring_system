from sqlalchemy.orm import Session

from core.db import models, schemas
from core.utils import utils

def get_degree(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Degree).all()

def get_degree_by_sensor_num(db: Session, sensor_id: int):
    # sensor number에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.sensor_id == sensor_id).all()

def get_degree_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.time > start, models.Degree.time < end).all()
