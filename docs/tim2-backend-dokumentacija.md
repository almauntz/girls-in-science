# Tim 2 — Mentoring: Backend Dokumentacija

**Projekat:** Girls in Science Platform  
**Tim:** Tim 2 — Mentoring  
**Tehnologije:** Python, FastAPI, SQLAlchemy, SQLite (dev) / PostgreSQL (produkcija)

---

## Sadržaj

1. [Pregled modula](#1-pregled-modula)
2. [Postavljanje okruženja](#2-postavljanje-okruženja)
3. [Pokretanje backenda](#3-pokretanje-backenda)
4. [Testni podaci](#4-testni-podaci)
5. [Struktura fajlova](#5-struktura-fajlova)
6. [Baza podataka — modeli i relacije](#6-baza-podataka--modeli-i-relacije)
7. [API endpointi](#7-api-endpointi)
8. [Admin endpointi](#8-admin-endpointi)
9. [Integracija sa Tim 4 (Profili)](#9-integracija-sa-tim-4-profili)
10. [Česti problemi i rješenja](#10-česti-problemi-i-rješenja)

---

## 1. Pregled modula

Mentoring modul pokriva sljedeće funkcionalnosti:

- **Javni pregled mentorica** — lista svih odobrenih mentorica sa filterom po oblasti
- **Profil mentorice** — detaljan prikaz biografije, iskustva i dostupnosti
- **Prijava mentorice** — forma za prijavu u program (čeka odobrenje admina)
- **Prijava studentice** — forma za učešće u mentorskom programu (čeka odobrenje admina)
- **Zahtjev za mentorstvo** — studentica šalje zahtjev konkretnoj mentorici *(implementirala kolegica)*
- **Panel mentorice** — mentorica pregleda i obrađuje pristigle zahtjeve *(implementirala kolegica)*
- **Admin panel** — odobravanje/odbijanje prijava mentorica i studentica

---

## 2. Postavljanje okruženja

### Preduvjeti

- **Python 3.12** (ne koristiti Python 3.14 — nekompatibilnost sa SQLModel/Pydantic)
- Git

### Koraci

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/almauntz/girls-in-science.git
cd girls-in-science

# 2. Prebaci se u backend folder
cd backend

# 3. Kreiraj virtualno okruženje sa Python 3.12
py -3.12 -m venv venv

# 4. Aktiviraj virtualno okruženje
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 5. Instaliraj zavisnosti
pip install -r requirements.txt
```

### Napomena o Windowsu

Na Windowsu, ako `Activate.ps1` baci grešku o izvršavanju skripti, pokreni:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 3. Pokretanje backenda

```bash
# Iz backend/ foldera, sa aktiviranim venv-om
uvicorn app.main:app --reload
```

- API dostupan na: `http://127.0.0.1:8000`
- Swagger dokumentacija: `http://127.0.0.1:8000/docs`
- ReDoc dokumentacija: `http://127.0.0.1:8000/redoc`

Tabele se kreiraju **automatski** pri prvom pokretanju (`Base.metadata.create_all`). Nije potrebno ručno pokretati migracije za inicijalno postavljanje.

### Alembic migracije

Ako si povukao izmjene sa grane koje uključuju novi model ili promjenu sheme:

```bash
# Iz backend/ foldera
alembic upgrade head
```

Ako si dodao/izmijenio model i trebaš kreirati novu migraciju:

```bash
alembic revision --autogenerate -m "kratki opis promjene"
alembic upgrade head
```

---

## 4. Testni podaci

### Kreiranje admin korisnika

Admin korisnik se ne kreira automatski. Pokreni sljedeću komandu jednom (sa aktiviranim venv-om, iz `backend/` foldera):

```bash
python -c "from app.database import SessionLocal; from app.models.user import User, UserRole; from passlib.context import CryptContext; pwd = CryptContext(schemes=['bcrypt']); db = SessionLocal(); admin = User(email='admin@gis.com', full_name='Admin', password_hash=pwd.hash('admin123'), role=UserRole.admin); db.add(admin); db.commit(); db.close(); print('Admin kreiran')"
```

**Kredencijali:**
- Email: `admin@gis.com`
- Lozinka: `admin123`

### Seed skripta za mentorice

Seed skripta popunjava bazu sa 3 testne odobrene mentorice i 1 neodobrenom:

```bash
# Iz backend/ foldera, sa aktiviranim venv-om
python seed_mentors.py
```

> **Napomena:** Seed skriptu pokreni **nakon** što si pokrenuo backend (da se tabele kreiraju). Ako dobiješ grešku `UNIQUE constraint failed`, seed je već jednom pokrenut — nije potrebno ponovo.

### Pristup aplikaciji sa testnim podacima

Nakon seed skripte, na `http://localhost:5173/mentoring` trebaju biti vidljive kartice sljedećih mentorica:
- Amina Hodžić (Softverski inženjering)
- Lejla Kovačević (Mašinsko učenje)
- Sara Begić (Bioinformatika)

---

## 5. Struktura fajlova

Relevantni fajlovi za Tim 2 unutar `backend/` foldera:

```
backend/
  app/
    models/
      mentor.py          — SQLAlchemy model za mentorice
      student.py         — SQLAlchemy model za prijave studentica
      mentorship_request.py — Model za zahtjeve za mentorstvo (Tim 2 kolegica)
    routers/
      mentoring.py       — Javni i zaštićeni endpointi za mentoring
      admin.py           — Admin endpointi (odobravanje mentorica i studentica)
  seed_mentors.py        — Skripta za testne podatke
```

---

## 6. Baza podataka — modeli i relacije

### `Mentor` tabela (`app/models/mentor.py`)

Čuva podatke o mentoricama prijavljenim na program.

| Polje | Tip | Opis |
|---|---|---|
| id | Integer | Primarni ključ |
| first_name, last_name | String | Ime i prezime |
| email | String (unique) | Email — koristi se i za spajanje sa `User`/`Profile` tabelama |
| institution, position | String | Institucija i pozicija |
| city_country, linkedin_url | String | Lokacija i LinkedIn |
| academic_title | String | Akademska titula |
| field_of_expertise | String | Oblast ekspertize (koristi se za filter na frontendu) |
| years_of_experience | Integer | Godine iskustva |
| bio | String | Biografija |
| cv_url | String | Putanja do CV fajla (čuva se u `uploads/cv/`) |
| has_mentoring_experience | Boolean | Da li ima prethodno iskustvo u mentorstvu |
| motivation | String | Motivacija za učešće |
| max_mentees | Integer | Maksimalan broj studentica |
| preferred_session_format | String | Online / Uživo / Kombinovano |
| profile_img_url | String | Fallback slika (ako `Profile.avatar` ne postoji) |
| is_approved | Boolean | Da li je admin odobrio prijavu |
| status | Enum | PENDING / APPROVED / REJECTED / DELETED |
| rejection_reason | Text | Razlog odbijanja |

### `Student` tabela (`app/models/student.py`)

Čuva prijave studentica za mentorski program.

| Polje | Tip | Opis |
|---|---|---|
| id | Integer | Primarni ključ |
| full_name | String | Ime i prezime |
| email | String (unique) | Email studentice |
| university, faculty, year_of_study, city_country | String | Akademski i lokacijski podaci |
| areas_of_interest | String | Oblasti interesovanja |
| has_business_idea | String | Da / Ne / Other |
| expectations | String | Šta očekuje od programa |
| skills_to_improve | String | Vještine koje želi razviti |
| preferred_session_format | String | Online / Uživo / Kombinovano |
| session_commitment | Boolean | Potvrda min. 2 sesije |
| consent_data, consent_evaluation | Boolean | GDPR saglasnosti |
| status | Enum | PENDING / APPROVED / REJECTED / DELETED |

### `MentorshipRequest` tabela (`app/models/mentorship_request.py`)

Čuva zahtjeve studentica prema konkretnoj mentorici. *(Implementirala kolegica — Tim 2)*

| Polje | Tip | Opis |
|---|---|---|
| id | Integer | Primarni ključ |
| mentor_id | Integer (FK → mentors.id) | Mentorica kojoj je zahtjev upućen |
| student_user_id | Integer (FK → students.id) | Studentica koja je poslala zahtjev |
| message | String | Poruka studentice |
| expectations, skills_to_improve | String | Detalji zahtjeva |
| cv_file_path | String | Putanja do CV fajla |
| status | Enum | PENDING / ACCEPTED / REJECTED |
| created_at | DateTime | Datum kreiranja |
| rejection_reason | String | Razlog odbijanja |

### Relacije između tabela

```
users ──────────────────────────────── profiles (Tim 4)
  │                                        │
  │ email spajanje                         │ user_id FK
  │                                        │
mentors ──── mentorship_requests ──── students
  (mentor_id FK)      (student_user_id FK)
```

> **Važno:** `Mentor` i `Profile` (Tim 4) nemaju direktni strani ključ — spajaju se po `email` polju kroz `get_avatar_url()` funkciju u `mentoring.py`.

---

## 7. API endpointi

Svi endpointi imaju prefiks `/mentoring`.

### `GET /mentoring/mentors`

Javno dostupno. Vraća paginiranu listu odobrenih mentorica (`is_approved == True`).

**Query parametri:**
- `skip` (default: 0)
- `limit` (default: 10, max: 100)

**Primjer poziva:**
```
GET http://127.0.0.1:8000/mentoring/mentors?skip=0&limit=10
```

**Primjer odgovora (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "Amina Hodžić",
    "field_of_expertise": "Softverski inženjering",
    "bio": "Senior developer sa 8 godina iskustva.",
    "linkedin_url": "https://linkedin.com/in/...",
    "preferred_session_format": "Online",
    "max_mentees": 3,
    "current_applications_count": 0,
    "is_available": true,
    "years_of_experience": 8,
    "position": "Senior Developer",
    "institution": "Univerzitet u Tuzli",
    "avatar_url": "http://localhost:8000/uploads/avatars/abc.jpg"
  }
]
```

---

### `GET /mentoring/mentors/{id}`

Javno dostupno. Vraća detaljan profil jedne mentorice.

**Mogući odgovori:**
- `200 OK` — profil mentorice
- `404 Not Found` — mentorica sa tim ID-em ne postoji

---

### `POST /mentoring/apply`

Prijava mentorice za program. **Nije potrebna autentifikacija.**  
Prima `multipart/form-data` (zbog CV upload-a).

**Polja forme:**
`first_name`, `last_name`, `email`, `field_of_expertise`, `years_of_experience`, `linkedin_url`, `bio`, `cv_file`

**Mogući odgovori:**
- `201 Created` — prijava primljena
- `400 Bad Request` — email već postoji u bazi

**Napomena:** CV fajl se sprema u `backend/uploads/cv/` sa UUID nazivom.

---

### `GET /mentoring/cv/{filename}`

Preuzimanje CV fajla mentorice. Vraća fajl za download.

---

### `POST /mentoring/students/register`

Prijava studentice za mentorski program. **Zahtijeva JWT autentifikaciju.**  
Prima `multipart/form-data`.

**Polja forme:**
`full_name`, `email`, `university`, `faculty`, `year_of_study`, `city_country`, `areas_of_interest`, `has_business_idea`, `expectations`, `skills_to_improve`, `preferred_session_format`, `session_commitment`, `consent_data`, `consent_evaluation`

**Mogući odgovori:**
- `201 Created`:
```json
{ "message": "Prijava uspješno poslana!", "id": 12 }
```
- `400 Bad Request` — email već postoji
- `401 Unauthorized` — korisnik nije prijavljen

---

### `GET /mentoring/my-applications`

Mentoricin panel — lista zahtjeva studentica upućenih toj mentorici. **Zahtijeva JWT.**

Mentorica se pronalazi po emailu iz tokena → traži se njen `Mentor` zapis → vraćaju se njeni `MentorshipRequest` zapisi.

*(Endpoint implementirala kolegica — Tim 2)*

---

### `PUT /mentoring/applications/{application_id}/status`

Mentorica prihvata ili odbija zahtjev studentice. **Zahtijeva JWT.**

**Body (JSON):**
```json
{
  "status": "ACCEPTED",
  "rejection_reason": "Opciono — samo uz REJECTED"
}
```

**Mogući statusi:** `PENDING`, `ACCEPTED`, `REJECTED`

---

## 8. Admin endpointi

Svi admin endpointi imaju prefiks `/api/v1/admin` i zahtijevaju JWT token sa ulogom `admin`. Pristup bez admin uloge vraća `403 Forbidden`.

### Mentorice

| Metoda | Ruta | Opis |
|---|---|---|
| GET | `/api/v1/admin/mentor-applications?status=PENDING` | Lista prijava (po statusu) |
| GET | `/api/v1/admin/mentor-applications/{id}` | Detalji jedne prijave |
| PATCH | `/api/v1/admin/mentor-applications/{id}/approve` | Odobravanje — postavlja `is_approved=True`, mijenja ulogu korisnika u `mentor` |
| PATCH | `/api/v1/admin/mentor-applications/{id}/reject` | Odbijanje — prima opcioni `rejection_reason` |
| PATCH | `/api/v1/admin/mentor-applications/{id}/resubmit` | Vraća prijavu na `PENDING` |
| DELETE | `/api/v1/admin/mentor-applications/{id}` | Soft delete — status `DELETED`, zapis ostaje u bazi |

### Studentice

| Metoda | Ruta | Opis |
|---|---|---|
| GET | `/api/v1/admin/student-applications` | Prijave na čekanju (PENDING) |
| GET | `/api/v1/admin/student-applications-approved` | Odobrene prijave |
| GET | `/api/v1/admin/student-applications-rejected` | Odbijene prijave |
| GET | `/api/v1/admin/student-applications-deleted` | Soft-deletirane prijave |
| GET | `/api/v1/admin/student-applications/{id}` | Detalji jedne prijave |
| PATCH | `/api/v1/admin/student-applications/{id}/approve` | Odobravanje |
| PATCH | `/api/v1/admin/student-applications/{id}/reject` | Odbijanje |
| PATCH | `/api/v1/admin/student-applications/{id}/restore` | Vraća na PENDING |
| DELETE | `/api/v1/admin/student-applications/{id}` | Soft delete |

---

## 9. Integracija sa Tim 4 (Profili)

`Mentor` tabela i `Profile` tabela (Tim 4) nisu direktno povezane stranim ključem. Spajanje se radi po `email` polju kroz `get_avatar_url()` funkciju:

```python
def get_avatar_url(mentor: Mentor, db: Session) -> str | None:
    user = db.query(User).filter(User.email == mentor.email).first()
    if not user:
        return mentor.profile_img_url  # fallback
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile or not profile.avatar:
        return mentor.profile_img_url  # fallback
    return f"http://localhost:8000{profile.avatar}"
```

**Tok:** `Mentor.email` → `User.email` → `User.id` → `Profile.user_id` → `Profile.avatar`

Ovo omogućava da slika uploadovana na korisničkom profilu bude automatski vidljiva na mentorskoj kartici, bez ponovnog uploada.

---

## 10. Česti problemi i rješenja

### `python` nije prepoznat na Windowsu

Koristiti `py` umjesto `python`:
```bash
py -3.12 -m venv venv
py seed_mentors.py
```

### `no such table: mentors`

Tabela nije kreirana. Pokreni backend prvo (`uvicorn app.main:app --reload`), pa onda seed skriptu.

### `UNIQUE constraint failed`

Seed je već pokrenut. Nije potrebno ponovo — podaci su u bazi.

### `401 Unauthorized` na zaštićenim rutama

Token nije u headeru. U Swagger-u (`/docs`) klikni "Authorize" i unesi token u formatu:
```
Bearer <tvoj_token>
```

Token dobijaš pozivom `POST /auth/login`.

### Python 3.14 nekompatibilnost

`pydantic-core` i `SQLModel` nemaju prebuilovane wheel-ove za Python 3.14 na Windowsu. Rješenje je Python 3.12 (provjeri verziju: `py --version`).

### Alembic greška `No script_location key found`

`alembic.ini` fajl nije na trenutnoj grani. Pokreni:
```bash
git checkout main -- alembic.ini
git checkout main -- alembic/
```
