# 💍 Wedzo — Digital Wedding Invitation Platform

A full-stack platform for creating beautiful, personalized digital wedding invitations with RSVP tracking, WhatsApp blast, and 5 stunning animated templates.

---

## ✨ Features

- **5 Beautiful Templates** — Eternal Rose, Midnight Garden, Golden Hour, Celestial Love, Tropical Bloom
- **Two Invitation Modes**:
  - **Personalized** — Unique URL per guest, name pre-filled, WhatsApp blast, CSV import
  - **General** — Single URL, open RSVP for anyone
- **Background Music** — Auto-play with a glass-blur player
- **Animated RSVP Flow** — Confetti on "Yes", countdown timer, success screen
- **Photo Gallery** — Masonry grid with lightbox, up to 8 photos
- **AI Background Removal** — Cutout portrait via remove.bg API
- **Wishes Wall** — Guests can leave messages, auto-refreshes every 30 seconds
- **7-Step Wedding Wizard** — Full admin creation flow
- **QR Code Generation** — Per-wedding QR codes for easy sharing
- **Guest Management** — CSV upload, individual WhatsApp links, RSVP tracking

---

## 🏗️ Project Structure

```
Wedzo/
├── backend/          # FastAPI Python backend
│   ├── routers/      # API route handlers
│   ├── main.py       # App entry point
│   ├── models.py     # SQLAlchemy database models
│   ├── schemas.py    # Pydantic v2 schemas
│   ├── auth.py       # JWT authentication
│   ├── cloudinary_utils.py
│   ├── removebg.py
│   └── alembic/      # Database migrations
└── frontend/         # React + Vite frontend
    └── src/
        ├── pages/         # Route-level pages
        ├── components/    # Reusable components
        │   ├── ui/        # LoadingScreen, MusicPlayer, etc.
        │   ├── guest/     # Invitation sections (RSVP, Gallery, etc.)
        │   └── admin/     # Admin-specific components
        ├── templates/     # 5 wedding templates
        ├── hooks/         # useWedding, useCountdown, useParallax, useGyroscope
        ├── api/           # Axios client + API helpers
        └── store/         # Zustand auth store
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- [Cloudinary](https://cloudinary.com) account
- [remove.bg](https://remove.bg) API key

---

### 1. Database Setup

```sql
CREATE DATABASE wedzo;
```

---

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy and fill environment variables
copy .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/wedzo
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

REMOVEBG_API_KEY=your_removebg_key

BASE_URL=http://localhost:5173

ADMIN_EMAIL=admin@wedzo.com
ADMIN_PASSWORD=admin123
```

```bash
# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn main:app --reload --port 8000
```

Backend runs at: [http://localhost:8000](http://localhost:8000)  
API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy and fill environment variables
copy .env.example .env
```

Edit `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_BASE_URL=http://localhost:5173
VITE_GOOGLE_MAPS_KEY=your_google_maps_key_optional
```

```bash
# Start the dev server
npm run dev
```

Frontend runs at: [http://localhost:5173](http://localhost:5173)

---

## 📋 Usage

### 1. Admin Login

Navigate to `/admin` and login with your configured admin credentials.

### 2. Create a Wedding

Click **+ New Wedding** and follow the 7-step wizard:

| Step | Content |
|------|---------|
| 1 | Choose mode (Personalized or General) |
| 2 | Couple names, slug, love story |
| 3 | Ceremony date, time, venue |
| 4 | Reception details |
| 5 | Dress code, RSVP deadline, contact |
| 6 | Couple photo, gallery, background music |
| 7 | Template selection + publish |

### 3. Manage Guests (Personalized Mode)

From the dashboard, click **Guests** to:
- Add guests manually
- Import from CSV (`name`, `phone`, `email` columns)
- Copy individual invitation links
- Send WhatsApp messages
- Track RSVP status

### 4. Share the Invitation

- **General mode**: Share `/wedding/{slug}`
- **Personalized mode**: Share `/wedding/{slug}/{guest-slug}` (generated per guest)
- Use the **QR Code** button on the dashboard for printable QR codes

---

## 🎨 Templates

| Template | Colors | Vibe |
|----------|--------|------|
| Eternal Rose | Blush, Rose Gold, Burgundy | Timeless floral elegance |
| Midnight Garden | Navy, Forest Green, Gold | Dark botanical romance |
| Golden Hour | Sand, Terracotta, Ivory | Warm sunset glow |
| Celestial Love | Deep Navy, Purple, Gold | Cosmic mystical |
| Tropical Bloom | Jungle Green, Coral, Yellow | Vibrant paradise |

---

## 🔧 API Endpoints

### Auth
- `POST /api/auth/login` — Admin login
- `GET /api/auth/me` — Get current admin

### Weddings
- `GET /api/weddings` — List all (admin)
- `POST /api/weddings` — Create wedding (admin)
- `GET /api/weddings/{slug}` — Get by slug (public)
- `GET /api/weddings/by-id/{id}` — Get by ID (admin)
- `PUT /api/weddings/{id}` — Update (admin)
- `DELETE /api/weddings/{id}` — Delete (admin)
- `PATCH /api/weddings/{id}/toggle` — Toggle active (admin)

### Guests
- `GET /api/guests/{wedding_id}` — List guests (admin)
- `POST /api/guests/{wedding_id}` — Add guest (admin)
- `POST /api/guests/{wedding_id}/bulk` — Bulk add (admin)
- `DELETE /api/guests/{guest_id}` — Delete guest (admin)
- `GET /api/guests/{wedding_id}/{guest_slug}` — Get guest info (public)

### RSVP
- `POST /api/rsvp` — Submit RSVP (public)
- `GET /api/rsvp/{wedding_id}` — List RSVPs (admin)

### Wishes
- `POST /api/wishes` — Post wish (public)
- `GET /api/wishes/{wedding_id}` — List wishes (public)

### Media
- `POST /api/media/upload/photo` — Upload photo + remove bg
- `POST /api/media/upload/gallery` — Upload gallery photos
- `POST /api/media/upload/music` — Upload background music

---

## 🗄️ Database Schema

```
admins         — id, email, hashed_password, created_at
weddings       — id, slug, groom_name, bride_name, template, invitation_mode, ...
guests         — id, wedding_id, name, slug, phone, email, invitation_url, rsvp_submitted
rsvps          — id, wedding_id, guest_id?, guest_name, attending, guest_count, message
wishes         — id, wedding_id, guest_name, message, created_at
```

---

## 🛠️ Tech Stack

**Frontend**
- React 18 + Vite 5
- TailwindCSS 3
- Framer Motion 11 (animations)
- GSAP 3 (hero text stagger)
- Three.js (background effects)
- React Router 6
- Zustand (state management)
- React Hook Form + Zod (validation)
- Axios
- canvas-confetti
- qrcode.react
- html2canvas
- Papa Parse (CSV)

**Backend**
- FastAPI
- PostgreSQL + SQLAlchemy ORM
- Alembic (migrations)
- Pydantic v2
- Python-Jose (JWT)
- Passlib + bcrypt
- Cloudinary (media storage)
- remove.bg API (background removal)
- Uvicorn

---

## 📦 Build for Production

```bash
# Frontend
cd frontend
npm run build          # Outputs to frontend/dist/

# Backend — run with gunicorn/uvicorn behind nginx
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📝 License

MIT — feel free to use for personal and commercial projects.
"# wedzo_project" 
