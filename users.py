from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.users import User, UserCreate, UserResponse

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Пользователь уже существует")
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.post("/signin")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if db_user.password != user.password:
        raise HTTPException(status_code=403, detail="Неверный пароль")
    return {"message": "Вход выполнен успешно"}