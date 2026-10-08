from fastapi import FastAPI
from app.db import Base, engine
from app.api import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сборник рецептов API")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Сборник рецептов API работает"}
