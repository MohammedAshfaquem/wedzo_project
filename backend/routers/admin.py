from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas
from backend.auth import verify_password, create_access_token, get_current_admin, get_password_hash
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == payload.email).first()
    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token({"sub": admin.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.AdminResponse)
def register(payload: schemas.AdminLogin, db: Session = Depends(get_db)):
    """Create a new admin user. Only works if no admins exist yet."""
    existing_admins = db.query(models.Admin).first()
    if existing_admins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins already exist. Contact your administrator.",
        )
    
    hashed_password = get_password_hash(payload.password)
    admin = models.Admin(email=payload.email, hashed_password=hashed_password)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@router.get("/me", response_model=schemas.AdminResponse)
def get_me(current_admin: models.Admin = Depends(get_current_admin)):
    return current_admin
