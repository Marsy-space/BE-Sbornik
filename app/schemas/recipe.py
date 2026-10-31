from pydantic import BaseModel, Field
from typing import Optional


class RecipeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    short_description: Optional[str] = None
    cooking_time_minutes: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    is_private: bool = False

class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    short_description: Optional[str] = None
    cooking_time_minutes: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    is_private: Optional[bool] = None

class RecipeOut(BaseModel):
    id: int
    author_id: int
    title: str
    short_description: Optional[str]
    cooking_time_minutes: Optional[int]
    category_id: Optional[int]
    is_private: bool

    class Config:
        from_attributes = True

class RecipeAccessOut(BaseModel):
    recipe_id: int
    user_id: int

    class Config:
        from_attributes = True