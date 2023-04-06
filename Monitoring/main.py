from typing import List, Union
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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
templates = Jinja2Templates(directory="templates")

app.include_router(user_router.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')#, response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/signup')
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get('/mypage')
def my_page(request: Request):
    return templates.TemplateResponse("me.html", {"request": request})

@app.get('/dashboard')
def show_dashboard(request:Request):
    return templates.TemplateResponse("chart.html", {"request": request})

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
    
# api section
@app.get('/api/')
def root():
    return {"message": "This is backend side API section."}

# data
@app.get("/api/data/", response_model=List[schemas.Degree])
def read_degrees(db: Session = Depends(get_db)):
    degrees = crud.get_degree(db=db)
    return degrees

@app.get("/api/data/{sensor_num}", response_model=List[schemas.Degree])
def read_degrees_by_sensor_num(sensor_num: int, db: Session = Depends(get_db)):
    degrees = crud.get_degree_by_sensor_num(db=db, sensor_id=sensor_num)
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

@app.get("/api/sensor/sensor_info")
def read_sensor_info(db: Session = Depends(get_db)):
    sensor = crud.get_sensor_info(db=db)
    return sensor

@app.get("/api/sensor/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = crud.get_sensor(db=db, id=sensor_id)
    return sensor
