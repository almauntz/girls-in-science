
# Backend Dokumentacija — Girls in Science Platform (Tim 3)

## 1. Pregled projekta
Girls in Science Platform je web aplikacija Centra za podršku studenticama u STEM oblastima Univerziteta u Tuzli. Backend predstavlja REST API koji opslužuje Vue 3 frontend aplikaciju i upravlja svim podacima platforme — korisnicima, profilima uzorima, blog objavama, radionicama, mentorstvom i dashboard funkcionalnostima.

## 2. Tehnologije

Framework: FastAPI
ORM: SQLModel
Baza podataka (development): SQLite
Baza podataka (produkcija): PostgreSQL
Autentifikacija: JWT (python-jose)
Migracije: Alembic
Python: 3.10+


## 3. Struktura projekta

backend/
├── app/
│   ├── core/
│   │   ├── config.py        # Učitavanje .env varijabli
│   │   └── security.py      # JWT logika, get_current_user dependency
│   ├── models/
│   │   ├── user.py          # User model i UserRole enum
│   │   ├── role_model.py    # RoleModel, RoleModelCreate, RoleModelUpdate
│   │   ├── news.py          # NewsPost, NewsCategory, vezne tabele, sheme
│   │   ├── bookmark.py      # Bookmark model
│   │   ├── mentor.py        # Mentor model
│   │   ├── profile.py       # Profile model
│   │   ├── student.py       # Student model
│   │   └── workshops_models.py
│   ├── routers/
│   │   ├── auth.py          # Registracija i login
│   │   ├── role_models.py   # CRUD za profile uzora
│   │   ├── news.py          # CRUD za blog objave i kategorije
│   │   ├── bookmarks.py     # Upravljanje favoritima
│   │   ├── mentoring.py
│   │   ├── workshops.py
│   │   ├── profiles.py
│   │   ├── students.py
│   │   ├── admin.py
│   │   └── admin_users.py
│   ├── database.py          # Konfiguracija konekcije, create_db()
│   └── main.py              # FastAPI app, registracija routera, CORS, static files
├── alembic/                 # Alembic migracijski fajlovi
├── uploads/                 # Upload folder za slike (automatski se kreira)
├── requirements.txt
└── alembic.ini


## 4. Konfiguracija i pokretanje

Kloniranje repozitorija: 
git clone https://github.com/almauntz/girls-in-science
cd girls-in-science

Kreiranje virtualnog okruženja i instalacija zavisnosti
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt

Pokretanje servera
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload
Server je dostupan na http://127.0.0.1:8000. Swagger API dokumentacija dostupna na http://127.0.0.1:8000/docs.

Alembic migracije
cd backend
alembic upgrade head


## 5. Baza podataka

Korisničke uloge:
Sistem podržava tri uloge definisane kroz UserRole enum u user.py: student, mentor i admin. Uloga određuje šta korisnica može raditi na platformi — admin ima puni pristup svim CRUD operacijama, dok studentice i mentorice imaju ograničen pristup prema funkcionalnosti.

Ključne tabele (Tim 3)
role_models — čuva profile inspirativnih žena iz STEM oblasti. Polja: id, first_name, last_name, stem_field, institution, position, biography (TEXT), achievements (TEXT, jedan red = jedno postignuće), image_url (nullable), created_at (automatski timestamp).
news_posts — čuva blog objave i vijesti centra. Polja: id, title, content (TEXT), author (nullable), image_url (nullable), created_at (automatski timestamp).
news_categories — kategorije za blog objave. Polja: id, name (unique).
news_category_links — vezna tabela many-to-many između news_posts i news_categories. Polja: news_post_id (FK → news_posts.id), category_id (FK → news_categories.id).
news_post_role_model_links — vezna tabela many-to-many između news_posts i role_models, omogućava povezivanje blog objave sa profilima uzora. Polja: news_post_id (FK → news_posts.id), role_model_id (FK → role_models.id).
bookmarks — čuva favorite korisnica. Polja: id, user_id (FK → users.id), role_model_id (FK → role_models.id).

## 6. Autentifikacija
Autentifikacija je implementirana putem JWT tokena. Nakon uspješnog logina endpoint POST /auth/login vraća access_token. Token se šalje u Authorization: Bearer <token> headeru uz svaki zaštićeni zahtjev.
Zaštićeni endpointi koriste Depends(get_current_user) dependency definisan u app/core/security.py koji automatski vraća 401 Unauthorized ako token nedostaje ili je nevažeći. Endpointi koji zahtijevaju admin ulogu dodatno provjeravaju current_user.role != UserRole.admin i vraćaju 403 Forbidden ako korisnica nije administratorica.

## 7. Član 1 - Dženan Čerkezović

Modeli
*Pojedini modeli rađeni timski. Naglašeno kod ostalih članova da su i oni radili.
RoleModel — dizajnirao shemu i kreirao model u backend/app/models/role_model.py. Model sadrži polja: id, first_name, last_name, stem_field, institution, position, biography (TEXT), achievements (TEXT, jedan red = jedno postignuće), image_url (nullable), created_at (automatski timestamp). Kreirao RoleModelCreate i RoleModelUpdate Pydantic sheme.
NewsPost i NewsPostRoleModelLink — kreirao model u backend/app/models/news.py. NewsPost sadrži polja id, title, content (TEXT), author (nullable), image_url (nullable), created_at. NewsPostRoleModelLink je vezna tabela many-to-many između news_posts i role_models sa poljima news_post_id (FK → news_posts.id) i role_model_id (FK → role_models.id). Kreirao NewsPostCreate, NewsPostUpdate, NewsPostRead i RoleModelSimple sheme.

Endpointi — Role Models
POST /role-models/
Kreira novi profil uzora. Zahtijeva JWT autentifikaciju i admin ulogu.
Primjer requesta:
{
  "first_name": "Marie",
  "last_name": "Curie",
  "stem_field": "Fizika i hemija",
  "institution": "Univerzitet u Parizu",
  "position": "Profesorica",
  "biography": "Dobitnica dvije Nobelove nagrade...",
  "achievements": "Nobelova nagrada za fiziku 1903\nNobelova nagrada za hemiju 1911",
  "image_url": "/uploads/rolemodels/marie.jpg"
}
Mogući responsi: 200 OK sa kreiranim objektom uključujući generisani id i created_at, 403 Forbidden sa { "detail": "Samo administratorica može dodavati profile" }.


DELETE /role-models/{id}
Briše profil uzora. Zahtijeva JWT i admin ulogu.
Mogući responsi: 200 OK sa { "message": "Profil je uspješno obrisan" }, 403 Forbidden sa { "detail": "Samo administratorica može brisati profile" }, 404 Not Found sa { "detail": "Profil nije pronađen" }.
POST /role-models/upload-image
Upload profilne slike uzora na server. Zahtijeva JWT i admin ulogu. Content-Type je multipart/form-data, form polje je file. Slika se sprema u uploads/rolemodels/.
Primjer responsa: { "image_url": "/uploads/rolemodels/naziv_fajla.jpg" }.

Endpointi — News
GET /news/{id}
Dohvata detalje pojedinačne blog objave prema ID-u. Uključuje povezane profile uzora kroz RoleModelSimple shemu (id, ime, prezime, stem_field, image_url) i kategorije. Javno dostupno.
Primjer responsa:
{
  "id": 1,
  "title": "Uspjeh studentice FET-a",
  "content": "...",
  "author": "Adminica",
  "image_url": "/uploads/news/slika.jpg",
  "created_at": "2025-05-10T12:00:00Z",
  "role_models": [
    {
      "id": 3,
      "first_name": "Marie",
      "last_name": "Curie",
      "stem_field": "Fizika i hemija",
      "image_url": "/uploads/rolemodels/marie.jpg"
    }
  ],
  "categories": [
    { "id": 1, "name": "Uspjesi" }
  ]
}
Mogući responsi: 200 OK, 404 Not Found sa { "detail": "Objava nije pronađena" }.

POST /news/
Kreira novu blog objavu. Zahtijeva JWT i admin ulogu. Opciono prima role_model_ids za povezivanje sa profilima uzora i category_ids za dodjelu kategorija.
Primjer requesta:
{
  "title": "Nova radionica u maju",
  "content": "Centar organizuje novu radionicu...",
  "author": "Adminica",
  "image_url": "/uploads/news/radionica.jpg",
  "role_model_ids": [1, 3],
  "category_ids": [2]
}
Mogući responsi: 200 OK sa kreiranom objavom uključujući role_models i categories, 403 Forbidden sa { "detail": "Samo administratorica može kreirati objave" }.

PATCH /news/{id}
Ažurira postojeću blog objavu. Zahtijeva JWT i admin ulogu. Podržava parcijalno ažuriranje. Posebno ponašanje za role_model_ids: prazna lista briše sve veze sa profilima, izostavljeno polje ostavlja postojeće veze nepromijenjenim.
Primjer requesta:
{
  "title": "Ažurirani naslov",
  "role_model_ids": [1]
}
Mogući responsi: 200 OK sa ažuriranim objektom, 403 Forbidden, 404 Not Found.

POST /news/upload-image
Upload naslovne slike za blog objavu. Zahtijeva JWT i admin ulogu. Content-Type je multipart/form-data, form polje je file. Slika se sprema u uploads/news/.
Primjer responsa: { "image_url": "/uploads/news/naziv_fajla.jpg" }.


## 8. Član 2 - Amina Sarhatlić

Modeli
NewsCategory i NewsCategoryLink — kreirala modele u backend/app/models/news.py. NewsCategory tabela sadrži polja id i name (unique). NewsCategoryLink je vezna tabela many-to-many između news_posts i news_categories sa poljima news_post_id (FK → news_posts.id) i category_id (FK → news_categories.id).
Bookmark — kreirala model u backend/app/models/bookmark.py sa poljima id, user_id (FK → users.id) i role_model_id (FK → role_models.id).

Endpointi — Role Models
GET /role-models/{id}
Dohvata detalje jednog profila prema ID-u. Javno dostupno, autentifikacija nije potrebna.
Mogući responsi: 200 OK sa objektom profila, 404 Not Found sa { "detail": "Profil nije pronađen" }.

PATCH /role-models/{id}
Ažurira postojeći profil uzora. Zahtijeva JWT autentifikaciju i admin ulogu. Podržava parcijalno ažuriranje.
Primjer requesta:
{
  "position": "Vanredna profesorica",
  "institution": "Univerzitet u Sarajevu"
}
Mogući responsi: 200 OK sa ažuriranim objektom, 403 Forbidden sa { "detail": "Samo administratorica može uređivati profile" }, 404 Not Found.


Endpointi — News
GET /news/
Dohvata listu svih blog objava sortiranih od najnovije prema najstarijoj. Svaka objava uključuje listu kategorija. Javno dostupno.
Primjer responsa:
[
  {
    "id": 1,
    "title": "Naslov objave",
    "content": "Sadržaj...",
    "author": "Autorica",
    "image_url": null,
    "created_at": "2026-06-01T10:00:00",
    "role_models": [],
    "categories": [
      { "id": 1, "name": "STEM" }
    ]
  }
]

DELETE /news/{id}
Briše blog objavu. Zahtijeva JWT autentifikaciju i admin ulogu.
Mogući responsi: 200 OK sa { "message": "Objava je uspješno obrisana" }, 403 Forbidden sa { "detail": "Samo administratorica može brisati objave" }, 404 Not Found.


Endpointi — Kategorije
GET /news/categories
Dohvata sve dostupne kategorije. Javno dostupno.
Primjer responsa: [{ "id": 1, "name": "STEM" }, { "id": 2, "name": "Edukacija" }]

POST /news/categories
Kreira novu kategoriju. Zahtijeva JWT i admin ulogu.
Primjer requesta: { "name": "Nova kategorija" }
Mogući responsi: 200 OK sa kreiranom kategorijom, 400 Bad Request sa { "detail": "Kategorija sa ovim nazivom već postoji" }, 403 Forbidden.
Endpointi — Bookmarks

GET /bookmarks/
Dohvata listu profila uzora koje je trenutna korisnica sačuvala u favourite. Zahtijeva JWT.
Response 200 OK: lista RoleModel objekata.

POST /bookmarks/{role_model_id}
Dodaje profil uzora u favourite trenutne korisnice. Zahtijeva JWT.
Mogući responsi: 200 OK sa { "message": "Profil dodan u favorite" }, 400 Bad Request sa { "detail": "Profil je već dodan u favorite" }, 404 Not Found.

DELETE /bookmarks/{role_model_id}
Uklanja profil uzora iz favourita. Zahtijeva JWT.
Mogući responsi: 200 OK sa { "message": "Profil uklonjen iz favorita" }, 404 Not Found sa { "detail": "Bookmark nije pronađen" }.



## 9. Član 3 - Šejla Valjevac

Modeli
RoleModel — Kreiranje modela u backend/app/models/role_model.py za čuvanje podataka o ženama u nauci.
NewsPost — Kreiranje modela u backend/app/models/news.py sa podrškom za many-to-many vezu prema RoleModel entitetu kroz NewsPostRoleModelLink veznu tabelu.

Endpointi — Role Models

GET /role-models/
Dohvata listu svih profila uzora, sortiranih po prezimenu pa imenu. Javno dostupno, autentifikacija nije potrebna.

Endpointi — News
POST /news/
Kreira novu blog objavu. Zahtijeva JWT autentifikaciju i admin ulogu. Podržava opciono povezivanje sa profilima uzora kroz role_model_ids listu.
Primjer requesta:
{
  "title": "Nova radionica u maju",
  "content": "Centar organizuje novu radionicu...",
  "author": "Adminica",
  "image_url": "/uploads/news/radionica.jpg",
  "role_model_ids": [1, 3],
  "category_ids": [2]
}
{
  "title": "Nova radionica u maju",
  "content": "Centar organizuje novu radionicu...",
  "author": "Adminica",
  "image_url": "/uploads/news/radionica.jpg",
  "role_model_ids": [1, 3],
  "category_ids": [2]
}
Mogući responsi: 200 OK sa kreiranom objavom uključujući role_models i categories, 403 Forbidden sa { "detail": "Samo administratorica može kreirati objave" }.