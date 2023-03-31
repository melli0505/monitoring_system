from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from core import crud
from core.db import models, schemas
from core.base import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return FileResponse("frontend/main.html")

@app.get('/api/')
def root():
    return {"message": "This is backend side API section!"}

@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_user(db=db, user=user)

@app.get("/api/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/sensors/", response_model=List[schemas.Sensor])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datas = crud.get_data(db=db, skip=skip, limit=limit)
    return datas

@app.get("/api/sensors/{sensor_num}", response_model=List[schemas.Sensor])
def read_data_by_sensor_num(sensor_num: int = 0, db: Session = Depends(get_db)):
    datas = crud.get_data_by_sensor_num(db=db, sensor_num=sensor_num)
    return datas

@app.get("/api/sensors/{start}/{end}", response_model=List[schemas.Sensor])
def read_sensor_by_date(start: str, end: str, db: Session = Depends(get_db)):
    datas = crud.get_sensor_by_date(db=db, start=start, end=end)
    return datas
