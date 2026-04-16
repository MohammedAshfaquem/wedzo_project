import re
import csv
import io
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from urllib.parse import quote
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_admin
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(ENV_PATH)

BASE_URL = os.getenv("BASE_URL", "http://localhost:5173")

router = APIRouter(prefix="/api/guests", tags=["guests"])


def generate_guest_slug(name: str) -> str:
    """Convert 'Atheef Abdul Rahman' → 'atheef-abdul-rahman'"""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def ensure_unique_guest_slug(db: Session, wedding_id: str, slug: str) -> str:
    base_slug = slug
    counter = 2
    while True:
        existing = db.query(models.Guest).filter(
            models.Guest.wedding_id == wedding_id,
            models.Guest.slug == slug,
        ).first()
        if not existing:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def generate_invitation_url(wedding_slug: str, guest_slug: str) -> str:
    return f"{BASE_URL}/wedding/{wedding_slug}/{guest_slug}"


def build_whatsapp_message(guest: models.Guest, wedding: models.Wedding) -> str:
    couple = f"{wedding.groom_name} & {wedding.bride_name}"
    if wedding.groom2_name and wedding.bride2_name:
        couple += f" | {wedding.groom2_name} & {wedding.bride2_name}"
    msg = (
        f"Dear *{guest.name}*, you are cordially invited to the wedding of *{couple}*.\n\n"
        f"View your exclusive invitation here:\n{guest.invitation_url}"
    )
    return msg


@router.get("/{wedding_id}", response_model=List[schemas.GuestResponse])
def list_guests(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    return (
        db.query(models.Guest)
        .filter(models.Guest.wedding_id == wedding_id)
        .order_by(models.Guest.created_at.desc())
        .all()
    )


@router.post("/{wedding_id}", response_model=schemas.GuestResponse, status_code=status.HTTP_201_CREATED)
def add_guest(
    wedding_id: str,
    payload: schemas.GuestCreate,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    slug = ensure_unique_guest_slug(db, wedding_id, generate_guest_slug(payload.name))
    invitation_url = generate_invitation_url(wedding.slug, slug)

    guest = models.Guest(
        wedding_id=wedding_id,
        name=payload.name,
        slug=slug,
        phone=payload.phone,
        email=payload.email,
        invitation_url=invitation_url,
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


@router.post("/{wedding_id}/bulk", response_model=List[schemas.GuestResponse], status_code=status.HTTP_201_CREATED)
async def bulk_add_guests(
    wedding_id: str,
    payload: schemas.GuestBulkCreate,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    created_guests = []
    for item in payload.guests:
        name = item.name.strip()
        if not name:
            continue
        phone = item.phone or None
        email = item.email or None

        slug = ensure_unique_guest_slug(db, wedding_id, generate_guest_slug(name))
        invitation_url = generate_invitation_url(wedding.slug, slug)

        guest = models.Guest(
            wedding_id=wedding_id,
            name=name,
            slug=slug,
            phone=phone,
            email=email,
            invitation_url=invitation_url,
        )
        db.add(guest)
        created_guests.append(guest)

    db.commit()
    for g in created_guests:
        db.refresh(g)
    return created_guests


@router.delete("/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(
    guest_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    db.delete(guest)
    db.commit()


@router.get("/{wedding_id}/{guest_slug}", response_model=schemas.GuestResponse)
def get_guest_by_slug(
    wedding_id: str,
    guest_slug: str,
    db: Session = Depends(get_db),
):
    # Find wedding by slug (wedding_id can be slug or UUID)
    wedding = (
        db.query(models.Wedding)
        .filter(
            (models.Wedding.id == wedding_id) | (models.Wedding.slug == wedding_id)
        )
        .first()
    )
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    guest = (
        db.query(models.Guest)
        .filter(
            models.Guest.wedding_id == wedding.id,
            models.Guest.slug == guest_slug,
        )
        .first()
    )
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


@router.post("/{wedding_id}/whatsapp-blast")
def generate_whatsapp_links(
    wedding_id: str,
    db: Session = Depends(get_db),
    _: models.Admin = Depends(get_current_admin),
):
    wedding = db.query(models.Wedding).filter(models.Wedding.id == wedding_id).first()
    if not wedding:
        raise HTTPException(status_code=404, detail="Wedding not found")

    guests = db.query(models.Guest).filter(models.Guest.wedding_id == wedding_id).all()
    links = []
    for guest in guests:
        msg = build_whatsapp_message(guest, wedding)
        wa_url = f"https://wa.me/{guest.phone.lstrip('+').replace(' ', '') if guest.phone else ''}?text={quote(msg)}"
        links.append(
            schemas.WhatsAppLink(
                guest_id=guest.id,
                guest_name=guest.name,
                whatsapp_url=wa_url,
                invitation_url=guest.invitation_url or "",
            )
        )
    return links
