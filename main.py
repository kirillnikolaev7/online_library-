from fastapi import FastAPI
from database.db import engine, Base
from models import books, users, subscriptions, ratings
from routes.books import router as book_router
from routes.users import user_router
from routes.subscriptions import router as subscription_router
from routes.ratings import router as rating_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(rating_router)

@app.get("/")
def root():
    return {"message": "Library API is running"}