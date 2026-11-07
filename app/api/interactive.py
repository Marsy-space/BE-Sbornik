from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.recipe import Recipe, Favorite, Review, ShoppingListItem, RecipeIngredient
from app.schemas.recipe import ReviewCreate, ReviewOut, RecipeOut, SearchByIngredientsRequest, ShoppingItemOut
from app.core.security import get_current_user
from app.models.user import User
from app.core.websocket_manager import manager


router = APIRouter(tags=["interactive"])


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


@router.post("/recipes/{recipe_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def add_review(recipe_id: int, data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = Review(recipe_id=recipe_id, user_id=current_user.id, rating=data.rating, comment=data.comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


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



@router.websocket("/ws/chat/{user_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    user_id: int,
    role: str = Query("user", description="Роль: user, moderator, admin")
):
    await manager.connect(websocket, user_id, role)
    try:
        while True:
            data = await websocket.receive_text()

            if data.startswith("!broadcast "):
                announcement_text = data.replace("!broadcast ", "")
                await manager.broadcast_announcement(user_id, announcement_text)

            elif data.startswith("!support "):
                support_text = data.replace("!support ", "")
                for uid, conn in manager.active_connections.items():
                    if conn["role"] in ["admin", "moderator"]:
                        await conn["socket"].send_text(f"[Техподдержка] Пользователь #{user_id}: {support_text}")
                
                await websocket.send_text("Ваше сообщение отправлено в техническую поддержку.")

            else:
                await websocket.send_text(f"Сервер получил: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id)



@router.websocket("/ws/recipe/{recipe_id}/chat/{user_id}")
async def recipe_chat_endpoint(
    websocket: WebSocket,
    recipe_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket-комната для обсуждения рецепта в реальном времени.
    Сообщения автоматически сохраняются как отзывы/комментарии в базу данных,
    чтобы они не пропадали при перезагрузке страницы.
    """
    await manager.connect_to_recipe(websocket, recipe_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()

            
            new_review = Review(
                recipe_id=recipe_id,
                user_id=user_id,
                rating=5,  
                comment=data
            )
            db.add(new_review)
            db.commit()

            
            await manager.broadcast_to_recipe(recipe_id, user_id, data)

    except WebSocketDisconnect:
        manager.disconnect_from_recipe(recipe_id, user_id)