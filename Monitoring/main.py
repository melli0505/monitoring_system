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
from core.data import data_router
from core.utils import utils

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
app.include_router(data_router.router)

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


@app.get('/')
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
