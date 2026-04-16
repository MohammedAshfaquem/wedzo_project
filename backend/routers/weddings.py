import re
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_admin

router = APIRouter(prefix="/api/weddings", tags=["weddings"])


def generate_slug(bride: str, groom: str) -> str:
    """Generate URL-safe slug from couple names."""
    combined = f"{groom} {bride}".lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", combined)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug


def ensure_unique_slug(db: Session, slug: str, exclude_id: str = None) -> str:
    """Append numeric suffix if slug already exists."""
    base_slug = slug
    counter = 2
    while True:
        query = db.query(models.Wedding).filter(models.Wedding.slug == slug)
        if exclude_id:
            query = query.filter(models.Wedding.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@router.get("", response_model=List[schemas.WeddingResponse])
def list_weddings(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    return db.query(models.Wedding).order_by(models.Wedding.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.WeddingResponse, status_code=status.HTTP_201_CREATED)
def create_wedding(
    payload: schemas.WeddingCreate,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    slug = payload.slug or generate_slug(payload.bride_name, payload.groom_name)
    slug = ensure_unique_slug(db, slug)

    wedding = models.Wedding(
        slug=slug,
        **{k: v for k, v in payload.model_dump().items() if k != "slug"},
    )
    wedding.slug = slug
    db.add(wedding)
    db.commit()
    db.refresh(wedding)
    return wedding


@router.get("/by-id/{wedding_id}", response_model=schemas.WeddingResponse)
def get_wedding_by_id(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")
    return wedding


@router.get("/{slug}", response_model=schemas.WeddingResponse)
def get_wedding(slug: str, db: Session = Depends(get_db)):
    wedding = db.query(models.Wedding).filter(models.Wedding.slug == slug).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")
    return wedding


@router.put("/{wedding_id}", response_model=schemas.WeddingResponse)
def update_wedding(
    wedding_id: str,
    payload: schemas.WeddingUpdate,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(wedding, field, value)

    db.commit()
    db.refresh(wedding)
    return wedding


@router.delete("/{wedding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wedding(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")
    db.delete(wedding)
    db.commit()


@router.patch("/{wedding_id}/toggle", response_model=schemas.WeddingResponse)
def toggle_wedding(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")
    wedding.is_active = not wedding.is_active
    db.commit()
    db.refresh(wedding)
    return wedding
