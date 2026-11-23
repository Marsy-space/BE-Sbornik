from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    username: str = Field(min_length=2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: int
    is_blocked: bool
    is_verified: bool
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EmailUpdate(BaseModel):
    new_email: EmailStr
