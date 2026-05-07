from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.db import get_db
from models.ratings import Rating, RatingCreate, RatingUpdate, RatingResponse

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=RatingResponse)
def create_rating(data: RatingCreate, db: Session = Depends(get_db)):
    existing = db.query(Rating).filter(
        Rating.book_id == data.book_id,
        Rating.user_id == data.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Оценка уже существует")
    r = Rating(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.get("/book/{book_id}")
def get_book_ratings(book_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.book_id == book_id).all()
    avg = db.query(func.avg(Rating.rating)).filter(Rating.book_id == book_id).scalar()
    return {
        "ratings": ratings,
        "average": round(avg, 2) if avg else None
    }


@router.get("/user/{user_id}", response_model=list[RatingResponse])
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    return db.query(Rating).filter(Rating.user_id == user_id).all()


@router.patch("/{rating_id}", response_model=RatingResponse)
def update_rating(rating_id: int, data: RatingUpdate, db: Session = Depends(get_db)):
    r = db.query(Rating).filter(Rating.id == rating_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Оценка не найдена")
    for field, value in data.dict(exclude_none=True).items():
        setattr(r, field, value)
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    r = db.query(Rating).filter(Rating.id == rating_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Оценка не найдена")
    db.delete(r)
    db.commit()
    return {"detail": "Удалено"}