from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import Base, engine, SessionLocal
from app.models.user import Role
from app.api import auth, recipes, upload, interactive
from app.core.logging import get_logger

logger = get_logger()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Сборник рецептов API",
    description="Backend-сервис для платформы рецептов (аутентификация, рецепты, медиа, интерактив)",
    version="1.0.0"
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # На продакшене указать конкретный адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Раздача загруженных статических файлов (картинок)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение роутеров
app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(upload.router)
app.include_router(interactive.router)

@app.get("/")
def root():
    return {"message": "Сборник рецептов API работает"}

def seed_roles():
    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            db.add_all([
                Role(id=1, name="Guest", description="Неавторизованный пользователь"),
                Role(id=2, name="User", description="Авторизованный пользователь"),
                Role(id=3, name="Admin", description="Администратор"),
            ])
            db.commit()
            logger.info("Роли добавлены в базу")
    finally:
        db.close()

seed_roles()