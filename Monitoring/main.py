from typing import List, Union
from typing_extensions import Annotated

from jose import JWTError, jwt

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from core.db import models, schemas
from core.db.base import SessionLocal, engine

from core.user import user_router, user_crud
from core.utils import utils, crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)



@app.get('/')
def index():
    return FileResponse("frontend/main.html")

@app.get('/api/')
def root():
    return {"message": "This is backend side API section."}

# login
@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db, username=form_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    hashed_pass = user.hashed_password
    if not utils.verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    return {
        "access_token": utils.create_access_token(user.username),
        "refresh_token": utils.create_refresh_token(user.username)
    }

# user info
@app.get('/me')
async def get_me(user: models.User = Depends(utils.get_current_user)):
    return user

# data
@app.get("/api/data/", response_model=List[schemas.Degree])
def read_degrees(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    degrees = crud.get_degree(db=db, skip=skip, limit=limit)
    return degrees

@app.get("/api/data/{sensor_num}", response_model=List[schemas.Degree])
def read_degrees_by_sensor_num(id: int = 0, db: Session = Depends(get_db)):
    degrees = crud.get_degree_by_sensor_num(db=db, sensor_id=id)
    return degrees

@app.get("/api/data/{start}/{end}", response_model=List[schemas.Degree])
def read_degrees_by_date(start: str, end: str, db: Session = Depends(get_db)):
    degrees = crud.get_degree_by_date(db=db, start=start, end=end)
    return degrees

# sensor
@app.post("/api/sensor/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, username: str, db: Session = Depends(get_db)):
    exist_sensor = crud.get_sensor(db=db, id=sensor.id)
    if exist_sensor:
        raise HTTPException(status_code=400, detail="Sensor id already exist")
    user = user_crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="Could not found user")
    return crud.create_sensor(db=db, sensor=sensor, user=user)

@app.get("/api/sensor/", response_model=List[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db=db, skip=skip, limit=limit)
    return sensors

@app.get("/api/sensor/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = crud.get_sensor(db=db, id=sensor_id)
    return sensor