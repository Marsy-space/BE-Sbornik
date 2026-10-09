from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.recipe import Recipe, Favorite, Review, ShoppingListItem, RecipeIngredient
from app.schemas.recipe import ReviewCreate, ReviewOut, RecipeOut, SearchByIngredientsRequest, ShoppingItemOut
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(tags=["interactive"])

# --- Избранное ---
@router.post("/recipes/{recipe_id}/favorite", status_code=status.HTTP_201_CREATED)
def add_favorite(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.recipe_id == recipe_id).first()
    if fav:
        return {"message": "Рецепт уже в избранном"}
    db.add(Favorite(user_id=current_user.id, recipe_id=recipe_id))
    db.commit()
    return {"message": "Рецепт добавлен в избранное"}

@router.delete("/recipes/{recipe_id}/favorite")
def remove_favorite(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.recipe_id == recipe_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Рецепт не найден в избранном")
    db.delete(fav)
    db.commit()
    return {"message": "Удалено из избранного"}

# --- Отзывы ---
@router.post("/recipes/{recipe_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def add_review(recipe_id: int, data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = Review(recipe_id=recipe_id, user_id=current_user.id, rating=data.rating, comment=data.comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

# --- Поиск по ингредиентам ("Что приготовить") ---
@router.post("/recipes/search-by-ingredients", response_model=List[RecipeOut])
def search_by_ingredients(payload: SearchByIngredientsRequest, db: Session = Depends(get_db)):
    if not payload.ingredient_ids:
        return []
    
    matching_recipes = (
        db.query(Recipe)
        .join(RecipeIngredient)
        .filter(RecipeIngredient.ingredient_id.in_(payload.ingredient_ids))
        .group_by(Recipe.id)
        .all()
    )
    return matching_recipes

# --- Список покупок ---
@router.post("/shopping-list/add-recipe/{recipe_id}")
def add_recipe_to_shopping_list(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    for ring in recipe.ingredients:
        db.add(ShoppingListItem(
            user_id=current_user.id,
            ingredient_name=ring.ingredient.name,
            amount=ring.amount,
            unit=ring.ingredient.unit
        ))
    db.commit()
    return {"message": "Ингредиенты добавлены в список покупок"}

@router.get("/shopping-list", response_model=List[ShoppingItemOut])
def get_shopping_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ShoppingListItem).filter(ShoppingListItem.user_id == current_user.id).all()