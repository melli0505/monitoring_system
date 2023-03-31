from sqlalchemy.orm import Session
from fastapi import Query
from typing import Annotated
import hashlib as hash

from .db import models, schemas

def create_hashpassword(password: str):
    return hash.sha256(password.encode()).hexdigest()

# read single user by id
def get_user(db: Session, user_id: int):
    # db의 User table의 id와 입력받은 id가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.id == user_id).first()

# read single user by username
def get_user_by_username(db: Session, username: str):
    # db의 User table의 usernamer과 입력받은 username가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.username == username).first()

# read muiltiple user with list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # db의 User table에서 [skip : limit] 까지의 리스트
    return db.query(models.User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
    password = create_hashpassword(user.password)
    db_user = models.User(username=user.username, hashed_password=password)
    # database session에 db_user 정보 추가
    db.add(db_user)
    # db에 반영
    db.commit()
    # 최신 db 정보 
    db.refresh(db_user)
    return db_user

def get_degree(db:Session, skip: int = 0, limit: int = 100):
    # index 단위로 sensor data 추출
    return db.query(models.Degree).offset(skip).limit(limit).all()

def get_degree_by_sensor_num(db: Session, sensor_id: int):
    # sensor number에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.sensor_id == sensor_id).all()

def get_degree_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Degree).filter(models.Degree.time > start, models.Degree.time < end).all()

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(id=sensor.id, administer_id=1)
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