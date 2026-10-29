from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.schemas.user import UserOut
from app.models.recipe import Recipe
from app.models.favorite import Favorite

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(User).all()

@router.patch("/users/{user_id}/block", response_model=UserOut)
def toggle_block_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Нельзя заблокировать самого себя")
    
    user.is_blocked = not user.is_blocked # переключаем статус
    db.commit()
    db.refresh(user)
    return user

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    total_users = db.query(func.count(User.id)).scalar()
    total_recipes = db.query(func.count(Recipe.id)).scalar()
    total_favorites = db.query(func.count(Favorite.user_id)).scalar()
    
    return {
        "total_users": total_users,
        "total_recipes": total_recipes,
        "total_favorites": total_favorites
    }