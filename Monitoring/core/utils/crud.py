from sqlalchemy.orm import Session
from fastapi import Query
from typing import Annotated, Union
import hashlib as hash
from datetime import timedelta, datetime

from core.db import models, schemas
from core.utils import utils

def get_degree(db:Session, skip: int = 0, limit: int = 100):
    # index 단위로 sensor data 추출
    return db.query(models.Degree).offset(skip).limit(limit).all()

def get_degree_by_sensor_num(db: Session, sensor_id: int):
    # sensor number에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.sensor_id == sensor_id).all()

def get_degree_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.time > start, models.Degree.time < end).all()

def create_sensor(db: Session, sensor: schemas.SensorCreate, user: schemas.User):
    db_sensor = models.Sensor(id=sensor.id, administer_id=user.id)
    # database session에 db_sensor 정보 추가
    db.add(db_sensor)
    # db에 반영
    db.commit()
    # 최신 db 정보 
    db.refresh(db_sensor)
    return db_sensor

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_sensor(db: Session, id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == id).first()