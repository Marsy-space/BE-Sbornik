from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.recipe import Favorite
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeOut

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/{recipe_id}", status_code=status.HTTP_201_CREATED)
def add_to_favorites(recipe_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.recipe_id == recipe_id).first()
    if existing:
        return {"message": "Уже в избранном"}
        
    fav = Favorite(user_id=user.id, recipe_id=recipe_id)
    db.add(fav)
    db.commit()
    return {"message": "Добавлено в избранное"}

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(recipe_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.recipe_id == recipe_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Не найдено в избранном")
    db.delete(fav)
    db.commit()

@router.get("/", response_model=list[RecipeOut])
def get_my_favorites(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    favorites = db.query(Favorite).filter(Favorite.user_id == user.id).all()
    if not favorites:
        return []  # Защита от ошибки с пустым списком
    recipe_ids = [f.recipe_id for f in favorites]
    return db.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()