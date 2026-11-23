import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, EmailUpdate
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token, get_current_user
from app.core.email import send_verification_email
from app.models.user import User
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    return crud_user.create_user(db, data)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_user.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    if user.is_blocked:
        raise HTTPException(status_code=403, detail="Пользователь заблокирован")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verify_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Неверный или устаревший токен")
    
    user.is_verified = True
    user.verify_token = None # Удаляем токен после использования
    db.commit()
    return {"message": "Email успешно подтвержден!"}

@router.patch("/me/email")
def update_email(data: EmailUpdate, db: Session = Depends(get_db), current_user: Annotated[User, Depends(get_current_user)] = None):
    if crud_user.get_user_by_email(db, data.new_email):
        raise HTTPException(status_code=400, detail="Email уже занят")
    
    current_user.email = data.new_email
    current_user.is_verified = False
    current_user.verify_token = uuid.uuid4().hex
    db.commit()
    
    send_verification_email(data.new_email, current_user.verify_token)
    # Для теста выводим ссылку в консоль
    print(f"ССЫЛКА ДЛЯ ПОДТВЕРЖДЕНИЯ (Смена Email): http://localhost:5173/verify-email?token={current_user.verify_token}")
    return {"message": "Email обновлен. Подтвердите новый адрес."}

@router.post("/me/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None
):
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Разрешены только форматы JPG, PNG и WebP"
        )

    file_name = f"avatar_{current_user.id}_{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join("static/uploads", file_name)
    
    os.makedirs("static/uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    current_user.avatar_url = f"/static/uploads/{file_name}"
    db.commit()
    
    return {"avatar_url": current_user.avatar_url}