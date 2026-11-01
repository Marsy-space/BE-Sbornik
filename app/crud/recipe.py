from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.models.recipe_access import RecipeAccess
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.core.logging import get_logger

logger = get_logger()


def create_recipe(db: Session, data: RecipeCreate, author_id: int) -> Recipe:
    recipe = Recipe(**data.dict(), author_id=author_id)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    logger.info(f"Создан рецепт id={recipe.id} автором id={author_id}")
    return recipe


def get_recipe(db: Session, recipe_id: int) -> Recipe | None:
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def list_recipes(db: Session, skip: int = 0, limit: int = 100) -> list[Recipe]:
    return (
        db.query(Recipe)
        .filter(Recipe.is_private == False)  # noqa: E712
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_recipe(db: Session, recipe_id: int, data: RecipeUpdate, author_id: int) -> Recipe | None:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(recipe, field, value)
    db.commit()
    db.refresh(recipe)
    logger.info(f"Обновлён рецепт id={recipe_id}")
    return recipe


def delete_recipe(db: Session, recipe_id: int, author_id: int) -> bool:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return False
    db.delete(recipe)
    db.commit()
    logger.info(f"Удалён рецепт id={recipe_id}")
    return True


def set_privacy(db: Session, recipe_id: int, author_id: int, is_private: bool) -> Recipe | None:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.author_id == author_id)
        .first()
    )
    if not recipe:
        return None
    recipe.is_private = is_private
    db.commit()
    db.refresh(recipe)
    logger.info(f"Рецепт id={recipe_id} теперь {'приватный' if is_private else 'публичный'}")
    return recipe


def can_view_recipe(db: Session, recipe: Recipe, user_id: int | None) -> bool:
    """Проверяет, может ли пользователь видеть рецепт."""
    if not recipe.is_private:
        return True
    if user_id is None:
        return False
    if recipe.author_id == user_id:
        return True
    access = (
        db.query(RecipeAccess)
        .filter(RecipeAccess.recipe_id == recipe.id, RecipeAccess.user_id == user_id)
        .first()
    )
    return access is not None