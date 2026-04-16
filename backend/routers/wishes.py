from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas

router = APIRouter(prefix="/api/wishes", tags=["wishes"])


@router.post("", response_model=schemas.WishResponse, status_code=status.HTTP_201_CREATED)
def post_wish(payload: schemas.WishCreate, db: Session = Depends(get_db)):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == payload.wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    wish = models.Wish(
        wedding_id=payload.wedding_id,
        guest_name=payload.guest_name,
        wish_message=payload.wish_message,
    )
    db.add(wish)
    db.commit()
    db.refresh(wish)
    return wish


@router.get("/{wedding_id}", response_model=List[schemas.WishResponse])
def list_wishes(wedding_id: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Wish)
        .filter(models.Wish.wedding_id == wedding_id)
        .order_by(models.Wish.created_at.desc())
        .all()
    )
