import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Date, Text, Integer,
    ForeignKey, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Wedding(Base):
    __tablename__ = "weddings"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    slug = Column(String, unique=True, nullable=False, index=True)
    invitation_mode = Column(String, nullable=False, default="general")  # "general" or "personalized"
    template = Column(String, nullable=False, default="EternalRose")

    # Couple info
    bride_name = Column(String, nullable=False)
    groom_name = Column(String, nullable=False)
    bride2_name = Column(String, nullable=True)
    groom2_name = Column(String, nullable=True)
    wedding_date = Column(DateTime, nullable=False)
    our_story = Column(Text, nullable=True)

    # Ceremony
    ceremony_time = Column(String, nullable=True)
    ceremony_venue = Column(String, nullable=True)
    ceremony_address = Column(String, nullable=True)
    ceremony_maps_url = Column(String, nullable=True)

    # Reception
    reception_time = Column(String, nullable=True)
    reception_venue = Column(String, nullable=True)
    reception_address = Column(String, nullable=True)
    reception_maps_url = Column(String, nullable=True)

    # Guest details
    dress_code = Column(String, nullable=True)
    dress_code_colors = Column(ARRAY(String), nullable=True)
    rsvp_deadline = Column(Date, nullable=True)
    rsvp_contact = Column(String, nullable=True)

    # Media
    cover_photo_url = Column(String, nullable=True)
    cover_photo_cutout_url = Column(String, nullable=True)
    gallery_urls = Column(ARRAY(String), nullable=True)
    background_music_url = Column(String, nullable=True)

    # Design
    primary_color = Column(String, nullable=True, default="#B76E79")
    secondary_color = Column(String, nullable=True, default="#6B2D3E")

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guests = relationship("Guest", back_populates="wedding", cascade="all, delete-orphan")
    rsvps = relationship("RSVP", back_populates="wedding", cascade="all, delete-orphan")
    wishes = relationship("Wish", back_populates="wedding", cascade="all, delete-orphan")


class Guest(Base):
    __tablename__ = "guests"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    wedding_id = Column(UUID(as_uuid=False), ForeignKey("weddings.id"), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    invitation_url = Column(String, nullable=True)
    rsvp_submitted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wedding = relationship("Wedding", back_populates="guests")
    rsvps = relationship("RSVP", back_populates="guest")


class RSVP(Base):
    __tablename__ = "rsvps"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    wedding_id = Column(UUID(as_uuid=False), ForeignKey("weddings.id"), nullable=False)
    guest_id = Column(UUID(as_uuid=False), ForeignKey("guests.id"), nullable=True)
    guest_name = Column(String, nullable=False)
    attending = Column(Boolean, nullable=False)
    guest_count = Column(Integer, default=1)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wedding = relationship("Wedding", back_populates="rsvps")
    guest = relationship("Guest", back_populates="rsvps")


class Wish(Base):
    __tablename__ = "wishes"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    wedding_id = Column(UUID(as_uuid=False), ForeignKey("weddings.id"), nullable=False)
    guest_name = Column(String, nullable=False)
    wish_message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wedding = relationship("Wedding", back_populates="wishes")
