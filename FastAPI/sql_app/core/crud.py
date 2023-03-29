from sqlalchemy.orm import Session

from .db import models, schemas

# read single user by id
def get_user(db: Session, user_id: int):
    # db의 User table의 id와 입력받은 id가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.id == user_id).first()

# read single user by email
def get_user_by_email(db: Session, email: str):
    # db의 User table의 email와 입력받은 email가 같은 부분 중 첫번째
    return db.query(models.User).filter(models.User.email == email).first()

# read muiltiple user with list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # db의 User table에서 [skip : limit] 까지의 리스트
    return db.query(models.User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # database session에 db_user 정보 추가
    db.add(db_user)
    # db에 반영
    db.commit()
    # 최신 db 정보 받아오기
    db.refresh(db_user)
    return db_user

# read multiple items
def get_items(db: Session, skip: int, limit: int):
    return db.query(models.Item).offset(skip).limit(limit).all()

# create item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # item에 있는 key-value받아오고 owner)id 추가
    db_item = models.Item(**item.dict(), owner_id = user_id)
    # database session에 db_item 정보 추가
    db.add(db_item)
    # db에 반영
    db.commit()
    # 최신 db 정보 받아오기
    db.refresh(db_item)
    return db_item