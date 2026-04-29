# SQLModel Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the backend from SQLAlchemy to SQLModel, replace the `forum` router with `role_models` and `news` stub routers, and update all imports throughout.

**Architecture:** SQLModel replaces `declarative_base()` and `SessionLocal` with its own engine/session setup. The `User` model is rewritten as a SQLModel table model. All routers that imported `sqlalchemy.orm.Session` are updated to import from `sqlmodel`. No feature logic is added — stubs only.

**Tech Stack:** Python, FastAPI, SQLModel, SQLite, passlib, python-jose, pydantic v2

---

## File Map

| Action | File |
|---|---|
| Modify | `backend/requirements.txt` |
| Rewrite | `backend/app/database.py` |
| Rewrite | `backend/app/models/user.py` |
| Modify | `backend/app/core/security.py` |
| Modify | `backend/app/routers/auth.py` |
| Modify | `backend/app/routers/workshops.py` |
| Modify | `backend/app/routers/mentoring.py` |
| Modify | `backend/app/routers/profiles.py` |
| Delete | `backend/app/routers/forum.py` |
| Create | `backend/app/routers/role_models.py` |
| Create | `backend/app/routers/news.py` |
| Rewrite | `backend/app/main.py` |

---

## Task 1: Update requirements.txt

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Replace SQLAlchemy, Alembic with SQLModel**

Open `backend/requirements.txt` and make these changes:
- Remove the line `SQLAlchemy==2.0.49`
- Remove the line `alembic==1.18.4`
- Remove the line `Mako==1.3.10` (Alembic dependency, no longer needed)
- Add `sqlmodel==0.0.21`

The file should contain `sqlmodel==0.0.21` and no longer contain `SQLAlchemy`, `alembic`, or `Mako`.

- [ ] **Step 2: Install updated dependencies**

```bash
cd backend
pip install -r requirements.txt
```

Expected: sqlmodel installs successfully (it will pull in SQLAlchemy internally).

- [ ] **Step 3: Commit**

```bash
git add backend/requirements.txt
git commit -m "chore: swap SQLAlchemy+Alembic for SQLModel in requirements"
```

---

## Task 2: Rewrite database.py

**Files:**
- Rewrite: `backend/app/database.py`

- [ ] **Step 1: Replace the file contents**

Replace the entire contents of `backend/app/database.py` with:

```python
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
```

- [ ] **Step 2: Verify import works**

```bash
cd backend
python -c "from app.database import get_db, create_db, engine; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/database.py
git commit -m "refactor: rewrite database.py using SQLModel engine and Session"
```

---

## Task 3: Rewrite User model

**Files:**
- Rewrite: `backend/app/models/user.py`

- [ ] **Step 1: Replace the file contents**

Replace the entire contents of `backend/app/models/user.py` with:

```python
import enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class UserRole(str, enum.Enum):
    member = "member"
    mentor = "mentor"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(
        default=UserRole.member,
        sa_column=Column(SAEnum(UserRole), default=UserRole.member)
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```

Note: `UserRole` now extends `str` — this is required for SQLModel enum fields to serialize correctly with Pydantic v2.

- [ ] **Step 2: Verify the model imports cleanly**

```bash
cd backend
python -c "from app.models.user import User, UserRole; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/models/user.py
git commit -m "refactor: rewrite User model as SQLModel table model"
```

---

## Task 4: Update security.py imports

**Files:**
- Modify: `backend/app/core/security.py`

- [ ] **Step 1: Replace the SQLAlchemy Session import**

In `backend/app/core/security.py`, change line 6:

```python
# Before
from sqlalchemy.orm import Session

# After
from sqlmodel import Session
```

The rest of the file stays exactly the same. The `db.query(User).filter(...).first()` call works with SQLModel's Session because SQLModel's Session inherits from SQLAlchemy's Session.

- [ ] **Step 2: Verify import works**

```bash
cd backend
python -c "from app.core.security import get_current_user, hash_password; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/security.py
git commit -m "refactor: update security.py to import Session from sqlmodel"
```

---

## Task 5: Update auth.py imports

**Files:**
- Modify: `backend/app/routers/auth.py`

- [ ] **Step 1: Replace the SQLAlchemy Session import**

In `backend/app/routers/auth.py`, change line 3:

```python
# Before
from sqlalchemy.orm import Session

# After
from sqlmodel import Session
```

The rest of the file stays exactly the same.

- [ ] **Step 2: Verify import works**

```bash
cd backend
python -c "from app.routers.auth import router; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/routers/auth.py
git commit -m "refactor: update auth.py to import Session from sqlmodel"
```

---

## Task 6: Update stub router imports (workshops, mentoring, profiles)

**Files:**
- Modify: `backend/app/routers/workshops.py`
- Modify: `backend/app/routers/mentoring.py`
- Modify: `backend/app/routers/profiles.py`

- [ ] **Step 1: Update workshops.py**

In `backend/app/routers/workshops.py`, change:

```python
# Before
from sqlalchemy.orm import Session

# After
from sqlmodel import Session
```

- [ ] **Step 2: Update mentoring.py**

In `backend/app/routers/mentoring.py`, change:

```python
# Before
from sqlalchemy.orm import Session

# After
from sqlmodel import Session
```

- [ ] **Step 3: Update profiles.py**

In `backend/app/routers/profiles.py`, change:

```python
# Before
from sqlalchemy.orm import Session

# After
from sqlmodel import Session
```

- [ ] **Step 4: Verify all three import cleanly**

```bash
cd backend
python -c "
from app.routers.workshops import router as w
from app.routers.mentoring import router as m
from app.routers.profiles import router as p
print('OK')
"
```

Expected output: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/workshops.py backend/app/routers/mentoring.py backend/app/routers/profiles.py
git commit -m "refactor: update stub routers to import Session from sqlmodel"
```

---

## Task 7: Create role_models.py stub router

**Files:**
- Create: `backend/app/routers/role_models.py`

- [ ] **Step 1: Create the file**

Create `backend/app/routers/role_models.py` with:

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/role-models", tags=["role_models"])

# -------------------------------------------------------
# Team 3 — Role Models
# This is your router. All your endpoints go here.
#
# Role models are inspiring women in STEM. Build a directory
# that lets users browse and search them.
#
# Your team will define the RoleModel model in app/models/role_model.py
# Coordinate with the News team — a NewsPost can reference a RoleModel.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_role_models(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def role_models_placeholder():
    return {"message": "Role Models router is working — Team 3 builds here"}
```

- [ ] **Step 2: Verify import works**

```bash
cd backend
python -c "from app.routers.role_models import router; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/routers/role_models.py
git commit -m "feat: add role_models stub router"
```

---

## Task 8: Create news.py stub router

**Files:**
- Create: `backend/app/routers/news.py`

- [ ] **Step 1: Create the file**

Create `backend/app/routers/news.py` with:

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/news", tags=["news"])

# -------------------------------------------------------
# Team 4 — News & Blog
# This is your router. All your endpoints go here.
#
# News posts are stories, articles, and updates from the centre.
# A news post can optionally reference a RoleModel — coordinate
# with Team 3 on the RoleModel model and its ID field.
#
# Your team will define the NewsPost model in app/models/news.py
#
# Example protected endpoint:
#
# @router.get("/")
# def get_news(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def news_placeholder():
    return {"message": "News router is working — Team 4 builds here"}
```

- [ ] **Step 2: Verify import works**

```bash
cd backend
python -c "from app.routers.news import router; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/routers/news.py
git commit -m "feat: add news stub router"
```

---

## Task 9: Delete forum.py and rewrite main.py

**Files:**
- Delete: `backend/app/routers/forum.py`
- Rewrite: `backend/app/main.py`

- [ ] **Step 1: Delete forum.py**

```bash
rm backend/app/routers/forum.py
```

- [ ] **Step 2: Rewrite main.py**

Replace the entire contents of `backend/app/main.py` with:

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.core.config import settings
from app.database import create_db
from app.routers import auth, mentoring, workshops, profiles, role_models, news
from app.core.security import get_current_user
from app.models.user import User

create_db()

security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="Platform backend for Girls in Science centre",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(workshops.router)
app.include_router(mentoring.router)
app.include_router(role_models.router)
app.include_router(news.router)
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running"}

@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role
    }
```

- [ ] **Step 3: Start the server and verify all routes load**

```bash
cd backend
uvicorn app.main:app --reload
```

Expected: server starts with no errors. Visit `http://localhost:8000/docs` and confirm these routes appear:
- `GET /`
- `POST /auth/register`
- `POST /auth/login`
- `GET /me`
- `GET /workshops/`
- `GET /mentoring/`
- `GET /role-models/`
- `GET /news/`
- `GET /profiles/`

No `/forum/` route should appear.

- [ ] **Step 4: Test auth still works**

With the server running, register a user and verify you get a token back:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "full_name": "Test User", "password": "secret123"}'
```

Expected: `{"access_token": "<token>", "token_type": "bearer"}`

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py
git rm backend/app/routers/forum.py
git commit -m "feat: replace forum with role_models and news routers, wire up SQLModel create_db"
```

---

## Task 10: Delete the old SQLite database file

**Files:**
- Delete: `backend/girls_in_science.db`

The old database was created by SQLAlchemy. SQLModel will recreate it fresh on next startup.

- [ ] **Step 1: Delete the old database**

```bash
rm backend/girls_in_science.db
```

- [ ] **Step 2: Restart the server and confirm the database is recreated**

```bash
cd backend
uvicorn app.main:app --reload
```

Expected: server starts, `girls_in_science.db` is recreated, no errors in console.

- [ ] **Step 3: Confirm the users table exists**

```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('girls_in_science.db')
tables = conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
print(tables)
"
```

Expected: `[('users',)]`

- [ ] **Step 4: Confirm db is gitignored**

The `.gitignore` already contains `*.db`, so `girls_in_science.db` is not tracked by git. No commit needed for this step — the deletion is local only.
