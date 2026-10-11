from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.models.recipe_access import RecipeAccess
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger()


def grant_access(db: Session, recipe_id: int, author_id: int, target_user_id: int) -> RecipeAccess | None:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return None
    target = db.query(User).filter(User.id == target_user_id).first()
    if not target:
        return None

    existing = (
        db.query(RecipeAccess)
        .filter(RecipeAccess.recipe_id == recipe_id, RecipeAccess.user_id == target_user_id)
        .first()
    )
    if existing:
        return existing

    access = RecipeAccess(recipe_id=recipe_id, user_id=target_user_id)
    db.add(access)
    db.commit()
    db.refresh(access)
    logger.info(f"Доступ к рецепту id={recipe_id} выдан пользователю id={target_user_id}")
    return access


def revoke_access(db: Session, recipe_id: int, author_id: int, target_user_id: int) -> bool:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return False
    access = (
        db.query(RecipeAccess)
        .filter(RecipeAccess.recipe_id == recipe_id, RecipeAccess.user_id == target_user_id)
        .first()
    )
    if not access:
        return False
    db.delete(access)
    db.commit()
    logger.info(f"Доступ к рецепту id={recipe_id} отозван у пользователя id={target_user_id}")
    return True


def list_access(db: Session, recipe_id: int, author_id: int) -> list[RecipeAccess]:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return []
    return db.query(RecipeAccess).filter(RecipeAccess.recipe_id == recipe_id).all()