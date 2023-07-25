from sqlalchemy.orm import Session

from core.db import models, schemas
from core.utils import utils

def get_voltage(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Voltage).all()

def get_voltage_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Voltage).filter(models.Voltage.time > start, models.Voltage.time < end).all()


def get_current(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Current).all()

def get_current_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Current).filter(models.Current.time > start, models.Current.time < end).all()



def get_power(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Power).all()

def get_power_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Power).filter(models.Power.time > start, models.Power.time < end).all()




def get_energy(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Energy).all()

def get_energy_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Energy).filter(models.Energy.time > start, models.Energy.time < end).all()



def get_pf(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.PF).all()

def get_pf_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.PF).filter(models.PF.time > start, models.PF.time < end).all()


def get_frequency(db:Session):
    # index 단위로 sensor data 추출
    return db.query(models.Frequency).all()

def get_frequency_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Frequency).filter(models.Frequency.time > start, models.Frequency.time < end).all()


