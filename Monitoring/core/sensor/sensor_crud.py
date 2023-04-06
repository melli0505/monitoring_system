from sqlalchemy.orm import Session

from core.db import models, schemas
from core.utils import utils

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

def get_sensor_info(db: Session):
    return db.query(models.Sensor).all()