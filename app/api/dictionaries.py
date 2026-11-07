from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.recipe import Category, Ingredient
from app.schemas.recipe import CategoryOut, IngredientOut, IngredientCreate, IngredientBase
from app.core.security import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(tags=["dictionaries"])

# Категории
@router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    name: str, 
    description: str = None,
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория уже существует")
    cat = Category(name=name, description=description)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

# Ингредиенты
@router.get("/ingredients", response_model=List[IngredientOut])
def get_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()

@router.post("/ingredients", response_model=IngredientOut, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    data: IngredientCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # Доступно авторизованным
):
    existing = db.query(Ingredient).filter(Ingredient.name == data.name).first()
    if existing:
        return existing # Если уже есть, просто возвращаем его
        
    ing = Ingredient(name=data.name, unit=data.unit)
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing