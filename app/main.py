from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import Base, engine, SessionLocal
from app.models import User, Role, Recipe, RecipeAccess, Category, Ingredient, Favorite, Review
from app.core.logging import get_logger
from app.api import auth, recipes, favorites, admin, upload, interactive, dictionaries

logger = get_logger()

Base.metadata.create_all(bind=engine)

def seed_roles():
    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            db.add_all([
                Role(id=1, name="Guest", description="Неавторизованный пользователь"),
                Role(id=2, name="User", description="Авторизованный пользователь"),
                Role(id=3, name="Admin", description="Администратор системы"),
            ])
            db.commit()
            logger.info("Роли добавлены в базу")
    finally:
        db.close()

seed_roles()

def seed_dictionaries():
    db = SessionLocal()
    try:
        if db.query(Category).count() == 0:
            db.add_all([
                Category(name="Супы", description="Первые блюда"),
                Category(name="Салаты", description="Холодные закуски"),
                Category(name="Десерты", description="Сладкое")
            ])
        if db.query(Ingredient).count() == 0:
            db.add_all([
                Ingredient(name="Картофель", unit="гр"),
                Ingredient(name="Морковь", unit="гр"),
                Ingredient(name="Соль", unit="гр"),
                Ingredient(name="Свекла", unit="гр"),
                Ingredient(name="Мясо", unit="гр")
            ])
        db.commit()
    finally:
        db.close()

seed_dictionaries()

app = FastAPI(
    title="Сборник рецептов API",
    description="Backend-сервис для платформы рецептов",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(favorites.router)
app.include_router(admin.router)
app.include_router(upload.router)
app.include_router(interactive.router)
app.include_router(dictionaries.router)

@app.get("/")
def root():
    return {"message": "Сборник рецептов API работает"}