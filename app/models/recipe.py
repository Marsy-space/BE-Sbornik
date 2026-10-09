from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    recipes = relationship("Recipe", back_populates="category")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    unit = Column(String(20), nullable=False, default="гр")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    amount = Column(Float, nullable=False)

    ingredient = relationship("Ingredient")


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)

    recipe = relationship("Recipe", back_populates="steps")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    cooking_time = Column(Integer, nullable=False)  # в минутах
    servings = Column(Integer, default=1)
    calories = Column(Integer, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User")
    category = relationship("Category", back_populates="recipes")
    steps = relationship("Step", back_populates="recipe", cascade="all, delete-orphan", order_by="Step.step_number")
    ingredients = relationship("RecipeIngredient", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="recipe", cascade="all, delete-orphan")


class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    recipe = relationship("Recipe", back_populates="reviews")
    user = relationship("User")


class ShoppingListItem(Base):
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ingredient_name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    is_bought = Column(Boolean, default=False)