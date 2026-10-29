from fastapi import FastAPI
from app.db import Base, engine, SessionLocal
from app.models import User, Role, Recipe, RecipeAccess
from app.core.logging import get_logger
from app.api import auth, recipes
from app.api import favorites, admin
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(title="Сборник рецептов API")

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

app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(favorites.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Сборник рецептов API работает"}