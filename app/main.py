from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import Base, engine, SessionLocal
from app.models import User, Role, Recipe, RecipeAccess  # noqa: F401  (нужно, чтобы создались все таблицы)
from app.core.logging import get_logger
from app.api import auth, recipes, favorites, admin, upload, interactive

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

app = FastAPI(
    title="Сборник рецептов API",
    description="Backend-сервис для платформы рецептов (аутентификация, рецепты, медиа, избранное, отзывы, список покупок)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Раздача загруженных картинок (папка static/uploads создаётся в app/api/upload.py)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(favorites.router)
app.include_router(admin.router)
app.include_router(upload.router)
app.include_router(interactive.router)


@app.get("/")
def root():
    return {"message": "Сборник рецептов API работает"}
