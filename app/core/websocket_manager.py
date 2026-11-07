from fastapi import WebSocket
from typing import Dict


class ConnectionManager:

    def __init__(self):
        
        self.active_connections: Dict[int, dict] = {}
        
        self.recipe_rooms: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, role: str):
        await websocket.accept()
        self.active_connections[user_id] = {"socket": websocket, "role": role}

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast_announcement(self, sender_id: int, message: str):
        """Рассылка сообщения всем онлайн пользователям от админа/модератора"""
        if self.active_connections.get(sender_id, {}).get("role") not in ["admin", "moderator"]:
            return

        for uid, conn in self.active_connections.items():
            await conn["socket"].send_text(f"[РАССЫЛКА ОТ АДМИНА]: {message}")

    async def connect_to_recipe(self, websocket: WebSocket, recipe_id: int, user_id: int):
        await websocket.accept()
        if recipe_id not in self.recipe_rooms:
            self.recipe_rooms[recipe_id] = {}
        self.recipe_rooms[recipe_id][user_id] = websocket

    def disconnect_from_recipe(self, recipe_id: int, user_id: int):
        if recipe_id in self.recipe_rooms:
            if user_id in self.recipe_rooms[recipe_id]:
                del self.recipe_rooms[recipe_id][user_id]
            if not self.recipe_rooms[recipe_id]:
                del self.recipe_rooms[recipe_id]

    async def broadcast_to_recipe(self, recipe_id: int, sender_id: int, message: str):
        """Рассылка сообщения всем, кто смотрит определенный рецепт"""
        if recipe_id in self.recipe_rooms:
            for uid, websocket in self.recipe_rooms[recipe_id].items():
                await websocket.send_text(f"Пользователь #{sender_id}: {message}")


manager = ConnectionManager()