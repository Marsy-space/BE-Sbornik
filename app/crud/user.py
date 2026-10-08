from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.logging import get_logger

logger = get_logger()

def create_user(db: Session, data: UserCreate) -> User:
    logger.info(f"Регистрация нового пользователя: {data.email}")
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        username=data.username,
        role_id=2,  # User
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.debug(f"Пользователь создан: id={user.id}")
    return user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, username: str | None = None, email: str | None = None) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None
    if username:
        user.username = username
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    logger.info(f"Обновлён пользователь id={user_id}")
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    logger.info(f"Удалён пользователь id={user_id}")
    return True

def block_user(db: Session, user_id: int) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None
    user.is_blocked = True
    db.commit()
    db.refresh(user)
    logger.warning(f"Заблокирован пользователь id={user_id}")
    return user
