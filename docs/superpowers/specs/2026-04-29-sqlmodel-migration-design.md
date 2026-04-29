# SQLModel Migration Design

**Date:** 2026-04-29  
**Project:** Girls in Science — backend restructure

## Goal

Migrate the FastAPI backend from SQLAlchemy + Pydantic models to SQLModel, and replace the `forum` feature with two new stub routers: `role_models` and `news`.

## Scope

- Structural migration only — no feature logic implemented
- Student teams will build out models and endpoints on top of this scaffold
- No Alembic; tables are created via `SQLModel.metadata.create_all(engine)` on startup

## Out of Scope

- Feature models (Workshop, MentoringSession, RoleModel, NewsPost) — owned by student teams
- Any endpoint logic beyond auth

## Changes

### `requirements.txt`
- Remove `SQLAlchemy` as a direct dependency (SQLModel bundles it)
- Remove `alembic`
- Add `sqlmodel`

### `app/database.py`
- Replace `declarative_base()`, `SessionLocal`, and `create_engine` (SQLAlchemy) with SQLModel equivalents
- `get_db` yields a SQLModel `Session` instead of a SQLAlchemy session
- `Base` is removed; tables are registered via `SQLModel, table=True` on each model

### `app/models/user.py`
- Rewrite `User` as a SQLModel model (`SQLModel, table=True`)
- Same fields: `id`, `email`, `full_name`, `password_hash`, `role` (enum), `created_at`
- Auth code in `app/core/security.py` continues to work unchanged

### `app/routers/forum.py`
- Deleted

### `app/routers/role_models.py` (new)
- Stub router at `/role-models`, tagged `role_models`
- One placeholder GET `/` endpoint with a comment block for the student team

### `app/routers/news.py` (new)
- Stub router at `/news`, tagged `news`
- One placeholder GET `/` endpoint with a comment block for the student team
- Comment notes the optional relationship to RoleModel (a news post can reference a role model)

### `app/main.py`
- Remove `forum` router import and registration
- Add `role_models` and `news` router imports and registration
- Update `create_all` call to use SQLModel

## Feature Summary

| Feature | Router prefix | Team | Status |
|---|---|---|---|
| Auth | `/auth` | — | implemented |
| Workshops | `/workshops` | Team 1 | stub |
| Mentoring | `/mentoring` | Team 2 | stub |
| Role Models | `/role-models` | Team 3 | stub (new) |
| News | `/news` | Team 4 | stub (new) |
| Profiles | `/profiles` | Team 5 | stub |

## Data Relationship Note

`NewsPost` and `RoleModel` are meant to be linked — a news article can optionally reference a role model. Student teams building these two routers should coordinate on this FK relationship when they define their models.
