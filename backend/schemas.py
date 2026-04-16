from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, date


# ─── AUTH ───────────────────────────────────────────────────────────────────

class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── WEDDING ─────────────────────────────────────────────────────────────────

class WeddingCreate(BaseModel):
    slug: Optional[str] = None
    invitation_mode: str = "general"
    template: str = "EternalRose"

    bride_name: str
    groom_name: str
    bride2_name: Optional[str] = None
    groom2_name: Optional[str] = None
    wedding_date: datetime
    our_story: Optional[str] = None

    ceremony_time: Optional[str] = None
    ceremony_venue: Optional[str] = None
    ceremony_address: Optional[str] = None
    ceremony_maps_url: Optional[str] = None

    reception_time: Optional[str] = None
    reception_venue: Optional[str] = None
    reception_address: Optional[str] = None
    reception_maps_url: Optional[str] = None

    dress_code: Optional[str] = None
    dress_code_colors: Optional[List[str]] = None
    rsvp_deadline: Optional[date] = None
    rsvp_contact: Optional[str] = None

    cover_photo_url: Optional[str] = None
    cover_photo_cutout_url: Optional[str] = None
    gallery_urls: Optional[List[str]] = None
    background_music_url: Optional[str] = None

    primary_color: Optional[str] = "#B76E79"
    secondary_color: Optional[str] = "#6B2D3E"

    @field_validator("rsvp_deadline", mode="before")
    @classmethod
    def empty_deadline_to_none(cls, value):
        if value == "":
            return None
        return value


class WeddingUpdate(BaseModel):
    invitation_mode: Optional[str] = None
    template: Optional[str] = None
    bride_name: Optional[str] = None
    groom_name: Optional[str] = None
    bride2_name: Optional[str] = None
    groom2_name: Optional[str] = None
    wedding_date: Optional[datetime] = None
    our_story: Optional[str] = None

    ceremony_time: Optional[str] = None
    ceremony_venue: Optional[str] = None
    ceremony_address: Optional[str] = None
    ceremony_maps_url: Optional[str] = None

    reception_time: Optional[str] = None
    reception_venue: Optional[str] = None
    reception_address: Optional[str] = None
    reception_maps_url: Optional[str] = None

    dress_code: Optional[str] = None
    dress_code_colors: Optional[List[str]] = None
    rsvp_deadline: Optional[date] = None
    rsvp_contact: Optional[str] = None

    cover_photo_url: Optional[str] = None
    cover_photo_cutout_url: Optional[str] = None
    gallery_urls: Optional[List[str]] = None
    background_music_url: Optional[str] = None

    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("rsvp_deadline", mode="before")
    @classmethod
    def empty_deadline_to_none(cls, value):
        if value == "":
            return None
        return value


class WeddingResponse(BaseModel):
    id: str
    slug: str
    invitation_mode: str
    template: str
    bride_name: str
    groom_name: str
    bride2_name: Optional[str] = None
    groom2_name: Optional[str] = None
    wedding_date: datetime
    our_story: Optional[str] = None
    ceremony_time: Optional[str] = None
    ceremony_venue: Optional[str] = None
    ceremony_address: Optional[str] = None
    ceremony_maps_url: Optional[str] = None
    reception_time: Optional[str] = None
    reception_venue: Optional[str] = None
    reception_address: Optional[str] = None
    reception_maps_url: Optional[str] = None
    dress_code: Optional[str] = None
    dress_code_colors: Optional[List[str]] = None
    rsvp_deadline: Optional[date] = None
    rsvp_contact: Optional[str] = None
    cover_photo_url: Optional[str] = None
    cover_photo_cutout_url: Optional[str] = None
    gallery_urls: Optional[List[str]] = None
    background_music_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── GUEST ───────────────────────────────────────────────────────────────────

class GuestCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class GuestBulkCreate(BaseModel):
    guests: List[GuestCreate]


class GuestResponse(BaseModel):
    id: str
    wedding_id: str
    name: str
    slug: str
    phone: Optional[str] = None
    email: Optional[str] = None
    invitation_url: Optional[str] = None
    rsvp_submitted: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── RSVP ────────────────────────────────────────────────────────────────────

class RSVPCreate(BaseModel):
    wedding_id: str
    guest_id: Optional[str] = None
    guest_name: str
    attending: bool
    guest_count: int = 1
    message: Optional[str] = None


class RSVPResponse(BaseModel):
    id: str
    wedding_id: str
    guest_id: Optional[str] = None
    guest_name: str
    attending: bool
    guest_count: int
    message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── WISH ────────────────────────────────────────────────────────────────────

class WishCreate(BaseModel):
    wedding_id: str
    guest_name: str
    wish_message: str


class WishResponse(BaseModel):
    id: str
    wedding_id: str
    guest_name: str
    wish_message: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── MEDIA ───────────────────────────────────────────────────────────────────

class PhotoUploadResponse(BaseModel):
    original_url: str
    cutout_url: Optional[str] = None


class MediaUploadResponse(BaseModel):
    url: str


# ─── WHATSAPP ────────────────────────────────────────────────────────────────

class WhatsAppLink(BaseModel):
    guest_id: str
    guest_name: str
    whatsapp_url: str
    invitation_url: str
