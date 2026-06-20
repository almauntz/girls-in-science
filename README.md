# Girls in Science — Platform

Platforma za Girls in Science centar koja omogućava članicama da se prijave na workshops, pronađu mentora, istražuju direktorij inspirativnih žena u STEM-u, prate vijesti i upravljaju svojim profilom.

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

| PRojektni tim | Funkcionalnost      | Folder                                                                  |
| ------------- | ------------------- | ----------------------------------------------------------------------- |
| Tim 1         | Workshops           | `backend/app/routers/workshops.py`, `frontend/src/views/workshops/`     |
| Tim 2         | Mentoring           | `backend/app/routers/mentoring.py`, `frontend/src/views/mentoring/`     |
| Tim 3         | Role Models         | `backend/app/routers/role_models.py`, `frontend/src/views/role_models/` |
| Tim 3         | Vijesti & Blog      | `backend/app/routers/news.py`, `frontend/src/views/news/`               |
| Tim 4         | Profili & Dashboard | `backend/app/routers/profiles.py`, `frontend/src/views/profiles/`       |

## Tehnologije

- **Backend:** Python, FastAPI, SQLModel, JWT
- **Frontend:** Vue 3, Vite, Tailwind CSS, Vue Router
- **Baza:** SQLite (development), PostgreSQL (produkcija)

## Autentifikacija

Platforma koristi JWT tokene. Nakon prijave token se čuva u `localStorage` i šalje sa svakim API pozivom u headeru:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Git Workflow

- Radite na grani `dev` — ne raditi commit direktno na `main`
- Konvencija za imenovanje grana: `timX/naziv-funkcionalnosti/naziv-featurea`
  - Primjeri: `tim1/workshops/prijava`, `tim3/rolemodels/lista`, `tim2/mentoring/pretraga`
- Commit poruke trebaju biti smislene i opisivati šta je promijenjeno
- Radite commit često — ne čekajte da sve bude gotovo pa onda jedan veliki commit
- Pull request prema `main` grani se radi tek na kraju sprinta, nakon pregleda asistentice

## Za projektne timove

Detaljne upute za backend i frontend nalaze se u:

- `backend/README.md`
- `frontend/README.md`

## Git Workflow za projektne timove

### Kloniranje projekta

```bash
git clone https://github.com/almauntz/girls-in-science.git
cd girls-in-science
git checkout dev
```

### Pravila rada

- **Nikad ne raditi push direktno na `main` ili `dev`**
- **Uvijek kreirati novi branch za svaku funkcionalnost (feature)**
- **Kad završite rad na branch-u, otvoriti Pull Request prema `dev`**

### Imenovanje brancheva

```
tim1/naziv-featurea
tim2/naziv-featurea
tim3/naziv-featurea
tim4/naziv-featurea
```

Primjeri:

```
tim1/workshop-listing
tim1/workshop-registration
tim2/mentor-profile
tim3/forum-posts
tim4/user-dashboard
```

### Dnevni workflow

**1 — Uvijek početi sa ažuriranjem lokalnog `dev` brancha:**

```bash
git checkout dev
git pull origin dev
```

**2 — Kreirati novi branch za funckionalnost (feature):**

```bash
git checkout -b tim1/naziv-featurea
```

**3 — Raditi na svom kodu, pa raditi commit redovno:**

```bash
git add .
git commit -m "Opis šta je uradjeno"
```

**4 — Uraditi push branch-a:**

```bash
git push origin tim1/naziv-featurea
```

**5 — Otvori Pull Request na GitHubu:**

- Idi na GitHub repo
- Klikni **"Compare & pull request"**
- Base branch: `dev`
- Opisati šta je implementirano
- Dodati članove tima kao reviewere, te obavezno asistenticu

### Commit poruke — kako pisati

```
✅ "Dodaj listu workshopa"
✅ "Popravi bug u registraciji mentora"
✅ "Dodaj validaciju forme za prijavu"

❌ "fix"
❌ "changes"
❌ "asdfgh"
```

### Rješavanje konflikata

Ako naiđete na konflikt pri merge-u:

```bash
git checkout dev
git pull origin dev
git checkout tim1/tvoj-branch
git merge dev
```

Otvori konfliktne fajlove, riješiti konflikte, pa:

```bash
git add .
git commit -m "Resolve merge conflicts"
git push origin tim1/tvoj-branch
```

### Važno

- Radite commit **često** — bolje više manjih commitova nego jedan veliki
- Nikad ne raditi commit `.env` file-a
- Svaki dan na početku rada pokreni `git pull origin dev`

## Napomena za testiranje

Sljedeće komande služe isključivo za lokalno testiranje različitih korisničkih uloga i scenarija tokom razvoja.

## Testiranje — Promjena uloge korisnika

Za testiranje različitih uloga (member/mentor/admin), rolu korisnika možete promijeniti direktno u bazi:

```bash
# Promjena u admina
sqlite3 database.db "UPDATE users SET role='admin' WHERE email='email@example.com';"

# Promjena u mentora
sqlite3 database.db "UPDATE users SET role='mentor' WHERE email='email@example.com';"

# Promjena u member (obični korisnik)
sqlite3 database.db "UPDATE users SET role='member' WHERE email='email@example.com';"
```

**Napomena:** Promjena role u `users` tabeli utiče samo na login/pristup. Za mentor dashboard funkcionalnost (zahtjevi mentoringa, dodijeljene studentice), potrebno je da postoji i odgovarajući red u `mentors` tabeli sa istim emailom.

## Testiranje — Kreiranje test mentora

Za testiranje mentorskog dashboarda (prikaz zahtjeva, prihvatanje/odbijanje), potrebno je da korisnik s `role='mentor'` ima odgovarajući profil u `mentors` tabeli:

```bash
sqlite3 database.db "INSERT INTO mentors (first_name, last_name, email, field_of_expertise, years_of_experience, linkedin_url, bio, cv_url, is_approved) VALUES ('Ime', 'Prezime', 'email@example.com', 'Software Engineering', 8, 'https://linkedin.com/in/primjer', 'Kratka biografija mentora.', 'test-cv.pdf', 1);"
```

`email` mora biti identičan emailu korisnika u `users` tabeli da bi se veza prepoznala.

## Testiranje — Kreiranje test studentice (za slanje zahtjeva mentoru)

Da bi studentica mogla poslati zahtjev za mentorstvo, mora prvo biti dodana u `students` tabelu (isti princip kao i kod mentora — `email` mora biti identičan emailu korisnice u `users` tabeli):

```bash
sqlite3 database.db "INSERT INTO students (first_name, last_name, email, faculty, year_of_study, areas_of_interest, has_business_idea, expectations, skills_to_improve, preferred_session_format, session_commitment, consent_data, consent_evaluation, created_at) VALUES ('Ime', 'Prezime', 'email@example.com', 'FET', '3. godina', 'IT i digitalne tehnologije', 'Ne', 'Test', 'Test', 'Online', 1, 1, 1, datetime('now'));"
```

**Napomena:** `status` kolona se ne navodi eksplicitno — koristi se default vrijednost `PENDING`.
