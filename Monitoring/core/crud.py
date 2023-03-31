from sqlalchemy.orm import Session
from fastapi import Query
from typing import Annotated

from .db import models, schemas

# read single user by id
def get_user(db: Session, user_id: int):
    # db의 User table의 id와 입력받은 id가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.id == user_id).first()

# read single user by email
def get_user_by_email(db: Session, email: str):
    # db의 User table의 email와 입력받은 email가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.email == email).first()

# read muiltiple user with list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # db의 User table에서 [skip : limit] 까지의 리스트
    return db.query(models.User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    # database session에 db_user 정보 추가
    db.add(db_user)
    # db에 반영
    db.commit()
    # 최신 db 정보 
    db.refresh(db_user)
    return db_user

def get_data(db:Session, skip: int = 0, limit: int = 100):
    # index 단위로 sensor data 추출
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_data_by_sensor_num(db: Session, sensor_num: int):
    # sensor number에 따라 data 추출
    return db.query(models.Sensor).filter(models.Sensor.sensor_number == sensor_num).all()

def get_sensor_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Sensor).filter(models.Sensor.timestamp > start, models.Sensor.timestamp < end).all()
