import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.database import engine, SessionLocal
from backend import models
from backend.auth import get_password_hash
from backend.routers import admin, weddings, guests, rsvp, wishes, media

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (Alembic handles migrations in prod)
    models.Base.metadata.create_all(bind=engine)

    # Seed default admin if not exists
    db = SessionLocal()
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "changeme")
        existing = db.query(models.Admin).filter(models.Admin.email == admin_email).first()
        if not existing:
            try:
                hashed = get_password_hash(admin_password)
                default_admin = models.Admin(email=admin_email, hashed_password=hashed)
                db.add(default_admin)
                db.commit()
            except Exception as e:
                print(f"Warning: Could not create default admin user: {e}")
                db.rollback()
    finally:
        db.close()

    yield


app = FastAPI(
    title="Wedding Platform API",
    description="Digital Wedding Invitation Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(admin.router)
app.include_router(weddings.router)
app.include_router(guests.router)
app.include_router(rsvp.router)
app.include_router(wishes.router)
app.include_router(media.router)


@app.get("/")
def root():
    return {"status": "Wedding Platform API is running", "docs": "/docs"}
