from fastapi import FastAPI
from app.db import Base, engine
from app.api import auth
from app.db import Base, engine, SessionLocal
from app.models.user import User, Role
from app.core.logging import get_logger

logger = get_logger()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сборник рецептов API")

app.include_router(auth.router)

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
