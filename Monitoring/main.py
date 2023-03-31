from typing import List, Union
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from core import crud
from core.db import models, schemas
from core.base import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def decode_token(token:str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")

@app.get('/')
def index():
    return FileResponse("frontend/main.html")

@app.get('/api/')
def root():
    return {"message": "This is backend side API section."}

# login
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = crud.create_hashpassword(form_data.password)
    if not user.hashed_password == hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

# users
@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
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

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user
# data
@app.get("/api/data/", response_model=List[schemas.Degree])
def read_degrees(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    degrees = crud.get_degree(db=db, skip=skip, limit=limit)
    return degrees

@app.get("/api/data/{sensor_num}", response_model=List[schemas.Degree])
def read_degrees_by_sensor_num(sensor_num: int = 0, db: Session = Depends(get_db)):
    degrees = crud.get_degree_by_sensor_num(db=db, sensor_num=sensor_num)
    return degrees

@app.get("/api/data/{start}/{end}", response_model=List[schemas.Degree])
def read_degrees_by_date(start: str, end: str, db: Session = Depends(get_db)):
    degrees = crud.get_degree_by_date(db=db, start=start, end=end)
    return degrees

# sensor
@app.post("/api/sensor/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    exist_sensor = crud.get_sensor(db=db, id=sensor.id)
    if exist_sensor:
        raise HTTPException(status_code=400, detail="Sensor id already exist")
    return crud.create_sensor(db=db, sensor=sensor)

@app.get("/api/sensor/", response_model=List[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db=db, skip=skip, limit=limit)
    return sensors

@app.get("/api/sensor/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = crud.get_sensor(db=db, sensor_id=sensor_id)
    return sensor