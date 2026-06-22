# Girls in Science — Backend

Izgrađeno sa FastAPI, SQLModel i SQLite (za razvoj).

## Postavljanje projekta

1. Kreiraj i aktiviraj virtualno okruženje:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instaliraj zavisnosti:
```bash
pip install -r requirements.txt
```

3. Pokreni server:
```bash
cd backend
uvicorn app.main:app --reload
```

4. Otvori API dokumentaciju:
```
http://127.0.0.1:8000/docs
```

## Struktura projekta

```
app/
  core/
    config.py       — postavke aplikacije, čita iz .env fajla
    security.py     — hashiranje lozinki, JWT tokeni
  models/
    user.py         — tabela korisnika (dijele sve ekipe)
  routers/
    auth.py         — registracija i prijava (ne mijenjati)
    workshops.py    — Projektni tim 1
    mentoring.py    — Projektni tim 2
    role_models.py  — Projektni tim 3
    news.py         — Projektni tim 3
    profiles.py     — Projektni tim 4
  main.py           — ulazna tačka aplikacije
  database.py       — konekcija na bazu podataka
```

## Autentifikacija

Svi zaštićeni endpointi zahtijevaju Bearer token u headeru:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

Token se dobija pozivom `POST /auth/login`.

## Migracije baze podataka (Alembic)

**Ako ste već klonirali projekat i radili na svojoj grani**, povucite nove promjene i primijenite migracije:

```bash
git pull origin main
alembic upgrade head
```

Nakon što dodate novi model ili izmijenite postojeći, pokrenite:

```bash
# Iz backend/ foldera, s aktiviranim virtualnim okruženjem
alembic revision --autogenerate -m "kratak opis promjene"
alembic upgrade head
```

Primjer:
```bash
alembic revision --autogenerate -m "dodaj tabelu workshops"
alembic upgrade head
```

## Za projektne timove

1. Vaš router fajl je već kreiran i registrovan u aplikaciji
2. Dodajte svoje modele u `app/models/`
3. Pokrenite migracije da kreirate tabele u bazi (pogledaj sekciju iznad)
4. Dodajte svoje endpointe u vaš router fajl
5. Koristite `Depends(get_current_user)` da dobijete prijavljenog korisnika
6. Kreirajte vlastite `.env` varijable ako je potrebno


---
### Mentoring
---

#### Modeli

**`Mentor`** (`app/models/mentor.py`)
SQLAlchemy model koji čuva podatke o mentoricama prijavljenim na program.

| Polje | Tip | Opis |
|---|---|---|
| id | Integer | Primarni ključ |
| first_name, last_name | String | Ime i prezime |
| email | String (unique) | Email mentorice |
| institution, position | String | Institucija i pozicija |
| field_of_expertise | String | Oblast ekspertize |
| years_of_experience | Integer | Godine iskustva |
| bio | String | Biografija |
| profile_img_url | String | Fallback slika (koristi se ako Profile.avatar ne postoji) |
| is_approved | Boolean | Da li je admin odobrio prijavu |
| status | Enum | PENDING / APPROVED / REJECTED / DELETED |

**`Student`** (`app/models/student.py`)
SQLAlchemy model koji čuva prijave studentica za mentorski program.

| Polje | Tip | Opis |
|---|---|---|
| id | Integer | Primarni ključ |
| full_name | String | Ime i prezime |
| email | String (unique) | Email studentice |
| university, faculty, year_of_study | String | Akademski podaci |
| areas_of_interest | String | Oblasti interesovanja |
| expectations, skills_to_improve | String | Očekivanja od programa |
| preferred_session_format | String | Online / Uživo / Kombinovano |
| consent_data, consent_evaluation | Boolean | Saglasnosti |
| status | Enum | PENDING / APPROVED / REJECTED / DELETED |

#### Endpointi (`app/routers/mentoring.py`)

**`GET /mentoring/mentors`**
Vraća listu odobrenih mentorica (`is_approved == True`).
Query parametri: `skip` (default 0), `limit` (default 10, max 100)

Primjer odgovora:
```json
[
  {
    "id": 1,
    "full_name": "Amina Hodžić",
    "field_of_expertise": "Softverski inženjering",
    "bio": "...",
    "avatar_url": "http://localhost:8000/uploads/avatars/...",
    "is_available": true
  }
]
```

**`GET /mentoring/mentors/{id}`**
Vraća detaljan profil jedne mentorice (za `MentorProfileView.vue`).

**`POST /mentoring/students/register`**
Prima prijavu studentice za mentorski program. Zahtijeva autentifikaciju (JWT). Vraća `400` ako email već postoji u bazi.

Telo zahtjeva (multipart/form-data): `full_name`, `email`, `university`, `faculty`, `year_of_study`, `city_country`, `areas_of_interest`, `has_business_idea`, `expectations`, `skills_to_improve`, `preferred_session_format`, `session_commitment`, `consent_data`, `consent_evaluation`

#### Integracija sa Tim 4 (Profili)

Funkcija `get_avatar_url(mentor, db)` povezuje `Mentor.email` sa `User.email` (Tim 4), pronalazi pripadajući `Profile.avatar`, i vraća punu URL putanju do slike. Ako profil ili avatar ne postoji, koristi se `Mentor.profile_img_url` kao fallback.

#### Admin endpointi za prijave studentica (`app/routers/admin.py`)

Proširio sam postojeći admin panel (koji je inicijalno razvijen za odobravanje mentorica) endpointima za upravljanje prijavama studentica:

- `GET /api/v1/admin/student-applications` — prijave na čekanju
- `GET /api/v1/admin/student-applications-approved` / `-rejected` / `-deleted` — filtrirane liste po statusu
- `GET /api/v1/admin/student-applications/{id}` — detalji jedne prijave
- `PATCH /api/v1/admin/student-applications/{id}/approve` / `/reject` / `/restore` — promjena statusa
- `DELETE /api/v1/admin/student-applications/{id}` — soft delete (status se postavlja na DELETED, podatak ostaje u bazi)

Svi endpointi zahtijevaju ulogu `admin` (provjereno preko `require_admin` dependency-ja).

---

