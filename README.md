# Girls in Science — Platform

Platforma za Girls in Science centar koja omogućava članicama da se prijave na workshops, pronađu mentora, učestvuju u forumu i upravljaju svojim profilom.

## Struktura projekta

```
girls-in-science/
  backend/       — FastAPI backend
  frontend/      — Vue 3 frontend
```

## Pokretanje projekta

### Backend
```bash
python3 -m venv venv
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API dostupan na: `http://127.0.0.1:8000`
Dokumentacija: `http://127.0.0.1:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Aplikacija dostupna na: `http://localhost:5173`

## Timovi i funkcionalnosti

| PRojektni tim | Funkcionalnost | Folder |
|-----|---------------|--------|
| Tim 1 | Workshops | `backend/app/routers/workshops.py`, `frontend/src/views/workshops/` |
| Tim 2 | Mentoring | `backend/app/routers/mentoring.py`, `frontend/src/views/mentoring/` |
| Tim 3 | Forum | `backend/app/routers/forum.py`, `frontend/src/views/forum/` |
| Tim 4 | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/` |

## Tehnologije

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic, JWT
- **Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router
- **Baza:** SQLite (development), PostgreSQL (produkcija)

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Za projektne timove

Detaljne upute za backend i frontend nalaze se u:
- `backend/README.md`
- `frontend/README.md`
