from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.models.recipe import Recipe, RecipeIngredient, Step, Category, Favorite
from app.schemas.recipe import RecipeCreate, RecipeOut
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/", response_model=List[RecipeOut])
def get_recipes(
    limit: int = 10,
    offset: int = 0,
    category_id: Optional[int] = None,
    max_cooking_time: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)
    if category_id:
        query = query.filter(Recipe.category_id == category_id)
    if max_cooking_time:
        query = query.filter(Recipe.cooking_time <= max_cooking_time)
    if search:
        query = query.filter(Recipe.title.ilike(f"%{search}%"))
    
    return query.offset(offset).limit(limit).all()

@router.get("/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe

@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = Recipe(
        title=data.title,
        description=data.description,
        cooking_time=data.cooking_time,
        servings=data.servings,
        calories=data.calories,
        category_id=data.category_id,
        author_id=current_user.id
    )
    db.add(recipe)
    db.flush()

    for ing in data.ingredients:
        db.add(RecipeIngredient(recipe_id=recipe.id, ingredient_id=ing.ingredient_id, amount=ing.amount))

    for st in data.steps:
        db.add(Step(recipe_id=recipe.id, step_number=st.step_number, description=st.description, image_url=st.image_url))

    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    if recipe.author_id != current_user.id and current_user.role_id != 3:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления этого рецепта")
    
    db.delete(recipe)
    db.commit()