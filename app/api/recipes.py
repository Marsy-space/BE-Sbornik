from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeOut, RecipeAccessOut
from app.crud import recipe as crud_recipe
from app.crud import recipe_access as crud_access

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud_recipe.create_recipe(db, data, author_id=user.id)


@router.get("/", response_model=list[RecipeOut])
def list_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_recipe.list_recipes(db, skip, limit)


@router.get("/{recipe_id}", response_model=RecipeOut)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    recipe = crud_recipe.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    if not crud_recipe.can_view_recipe(db, recipe, user.id if user else None):
        raise HTTPException(status_code=403, detail="Нет доступа к рецепту")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeOut)
def update_recipe(
    recipe_id: int,
    data: RecipeUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    recipe = crud_recipe.update_recipe(db, recipe_id, data, author_id=user.id)
    if not recipe:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование")
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not crud_recipe.delete_recipe(db, recipe_id, author_id=user.id):
        raise HTTPException(status_code=403, detail="Нет прав на удаление")


@router.patch("/{recipe_id}/privacy", response_model=RecipeOut)
def set_privacy(
    recipe_id: int,
    is_private: bool,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    recipe = crud_recipe.set_privacy(db, recipe_id, author_id=user.id, is_private=is_private)
    if not recipe:
        raise HTTPException(status_code=403, detail="Нет прав на изменение приватности")
    return recipe


@router.post("/{recipe_id}/access/{target_user_id}", response_model=RecipeAccessOut)
def grant_access(
    recipe_id: int,
    target_user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    access = crud_access.grant_access(db, recipe_id, author_id=user.id, target_user_id=target_user_id)
    if not access:
        raise HTTPException(status_code=404, detail="Рецепт или пользователь не найден")
    return access


@router.delete("/{recipe_id}/access/{target_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_access(
    recipe_id: int,
    target_user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not crud_access.revoke_access(db, recipe_id, author_id=user.id, target_user_id=target_user_id):
        raise HTTPException(status_code=404, detail="Доступ не найден")


@router.get("/{recipe_id}/access", response_model=list[RecipeAccessOut])
def list_access(
    recipe_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud_access.list_access(db, recipe_id, author_id=user.id)