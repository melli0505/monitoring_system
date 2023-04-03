from db.base import SessionLocal
from db import models
from db import schemas
import utils.utils

from sqlalchemy.orm import Session

# read single user by id
def get_user(db: Session, user_id: int):
    # db의 User table의 id와 입력받은 id가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.id == user_id).first()

# read single user by username
def get_user_by_username(db: Session, username: str):
    print(db)
    # db의 User table의 usernamer과 입력받은 username가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.username == username).first()

# read muiltiple user with list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # db의 User table에서 [skip : limit] 까지의 리스트
    return db.query(models.User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
    password = utils.get_hashed_password(user.password)
    db_user = models.User(username=user.username, hashed_password=password, email=user.email)
    # database session에 db_user 정보 추가
    db.add(db_user)
    # db에 반영
    db.commit()
    # 최신 db 정보 
    db.refresh(db_user)
    return db_user