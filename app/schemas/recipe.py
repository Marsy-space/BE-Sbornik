from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Ingredient Schemas ---
class IngredientBase(BaseModel):
    name: str
    unit: str = "гр"

class IngredientCreate(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: int
    class Config:
        from_attributes = True

class RecipeIngredientInput(BaseModel):
    ingredient_id: int
    amount: float

class RecipeIngredientOut(BaseModel):
    ingredient: IngredientOut
    amount: float
    class Config:
        from_attributes = True

# --- Step Schemas ---
class StepInput(BaseModel):
    step_number: int
    description: str
    image_url: Optional[str] = None

class StepOut(StepInput):
    id: int
    class Config:
        from_attributes = True

# --- Category Schemas ---
class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

# --- Recipe Schemas ---
class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cooking_time: int = Field(gt=0, description="Время приготовления в минутах")
    servings: int = Field(default=1, gt=0)
    calories: Optional[int] = None
    category_id: Optional[int] = None
    ingredients: List[RecipeIngredientInput] = []
    steps: List[StepInput] = []

class RecipeOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    cooking_time: int
    servings: int
    calories: Optional[int]
    image_url: Optional[str]
    author_id: int
    category: Optional[CategoryOut]
    ingredients: List[RecipeIngredientOut]
    steps: List[StepOut]
    created_at: datetime
    class Config:
        from_attributes = True

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    recipe_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# --- Search Schemas ---
class SearchByIngredientsRequest(BaseModel):
    ingredient_ids: List[int]

# --- Shopping List Schemas ---
class ShoppingItemOut(BaseModel):
    id: int
    ingredient_name: str
    amount: float
    unit: str
    is_bought: bool
    class Config:
        from_attributes = True