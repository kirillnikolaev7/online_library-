from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.subscriptions import Subscription, SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/", response_model=SubscriptionResponse)
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    sub = Subscription(**data.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@router.get("/", response_model=list[SubscriptionResponse])
def get_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()


@router.get("/user/{user_id}", response_model=list[SubscriptionResponse])
def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()


@router.get("/{sub_id}", response_model=SubscriptionResponse)
def get_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return sub


@router.patch("/{sub_id}", response_model=SubscriptionResponse)
def update_subscription(sub_id: int, data: SubscriptionUpdate, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    for field, value in data.dict(exclude_none=True).items():
        setattr(sub, field, value)
    db.commit()
    db.refresh(sub)
    return sub


@router.delete("/{sub_id}")
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    db.delete(sub)
    db.commit()
    return {"detail": "Удалено"}