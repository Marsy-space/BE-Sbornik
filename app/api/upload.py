import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.security import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.post("/image")
def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Разрешены только форматы JPG, PNG и WebP")

    file_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {"url": f"/static/uploads/{file_name}"}