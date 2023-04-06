from typing import List
from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends, Form
from sqlalchemy.orm import Session

from core.user import user_crud as crud
from .user_crud import *

from core.db import schemas
from core.db.base import SessionLocal
from db.base import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/api/users',
    tags=['users']
)

@router.post("/signup") #, response_model=schemas.User)
def create_user(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = schemas.UserCreate(username=username, email=email, password=password)
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
