from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_admin

router = APIRouter(prefix="/api/rsvp", tags=["rsvp"])


@router.post("", response_model=schemas.RSVPResponse, status_code=status.HTTP_201_CREATED)
def submit_rsvp(payload: schemas.RSVPCreate, db: Session = Depends(get_db)):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == payload.wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    rsvp = models.RSVP(
        wedding_id=payload.wedding_id,
        guest_id=payload.guest_id,
        guest_name=payload.guest_name,
        attending=payload.attending,
        guest_count=payload.guest_count,
        message=payload.message,
    )
    db.add(rsvp)

    # Mark guest as RSVP submitted if guest_id provided
    if payload.guest_id:
        guest = db.query(models.Guest).filter(models.Guest.id == payload.guest_id).first()
        if guest:
            guest.rsvp_submitted = True

    db.commit()
    db.refresh(rsvp)
    return rsvp


@router.get("/{wedding_id}", response_model=List[schemas.RSVPResponse])
def list_rsvps(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    return (
        db.query(models.RSVP)
        .filter(models.RSVP.wedding_id == wedding_id)
        .order_by(models.RSVP.created_at.desc())
        .all()
    )
