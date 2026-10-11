from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class RecipeAccess(Base):
    __tablename__ = "recipe_access"

    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    granted_at = Column(DateTime, default=datetime.utcnow)

    recipe = relationship("Recipe", back_populates="access_list")
    user = relationship("User")