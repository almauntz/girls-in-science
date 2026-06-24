# Girls in Science — Backend Dokumentacija

---

## 1. Struktura Backend Projekta

```
backend/
├── app/
│ ├── main.py (ulazna tačka aplikacije, registracija routera)
│ ├── auth.py (JWT autentifikacija, kreiranje i dekodiranje tokena)
│ ├── database.py (konfiguracija baze podataka i sesije)
│ ├── core/
│   └── security.py (Autentifikacija, enkripcija lozinki i centralni Auth Guard)
│ ├── routers/
│   ├── admin_users.py (Upravljanje korisnicama, statusima i ulogama)
│ │ └── profiles.py (endpointi za upravljanje profilima)
│ └── models/
│   └── profile.py (SQLModel modeli i Pydantic sheme)
└── static/
  └── avatars/ (direktorij za pohranu avatar slika)
```

---

## 2. Opis Baze Podataka

### 2.1 Entiteti i ključne tabele

#### Tabela: `users`

| Kolona           | Tip                     | Opis                                        |
| ---------------- | ----------------------- | ------------------------------------------- |
| `id`             | INTEGER (PK)            | Jedinstveni identifikator profila           |
| `full_name`      | VARCHAR                 | Puno ime i prezime korisnice                |
| `email`          | VARCHAR (Unique)        | Elektronska pošta (koristi se za prijavu)   |
| `password_hash`  | VARCHAR                 | Hashirana vrijednost lozinke                |
| `role`           | VARCHAR (Enum)          | Uloga u sistemu (user, mentor, admin)       |
| `created_at`     | DATETIME                | Vrijeme kreiranja zapisa                    |

#### Tabela: `profiles`

| Kolona           | Tip                     | Opis                                        |
| ---------------- | ----------------------- | ------------------------------------------- |
| `id`             | INTEGER (PK)            | Jedinstveni identifikator profila           |
| `user_id`        | INTEGER (FK → users.id) | Veza s korisnikom, unique                   |
| `biography`      | TEXT                    | Biografija (max 500 znakova)                |
| `field`          | VARCHAR                 | Oblast rada / struke                        |
| `avatar`         | VARCHAR                 | Putanja do avatar slike                     |
| `location`       | VARCHAR                 | Lokacija korisnika                          |
| `is_active`      | BOOLEAN                 | Da li je nalog aktivan (default: true)      |
| `deactivated_by` | VARCHAR                 | Ko je deaktivirao: `'user'` ili `'admin'`   |
| `show_biography` | BOOLEAN                 | Privacy: prikaži biografiju (default: true) |
| `show_field`     | BOOLEAN                 | Privacy: prikaži oblast (default: true)     |
| `show_location`  | BOOLEAN                 | Privacy: prikaži lokaciju (default: true)   |
| `languages`      | TEXT (JSON)             | Lista jezika – serializovana JSON lista     |
| `experience`     | TEXT (JSON)             | Lista iskustava – serializovana JSON lista  |
| `education`      | TEXT (JSON)             | Lista edukacija – serializovana JSON lista  |
| `skills`         | TEXT (JSON)             | Lista vještina – JSON niz stringova         |
| `linkedin_url`   | VARCHAR                 | LinkedIn URL                                |
| `github_url`     | VARCHAR                 | GitHub URL                                  |
| `twitter_url`    | VARCHAR                 | Twitter/X URL                               |

### 2.2 Relacije

- **users ↔ profiles:** Jedan-na-jedan (1:1). Svaki korisnik ima tačno jedan profil. Veza je ostvarena putem `user_id` stranog ključa u tabeli `profiles`.
- **users ↔ workshops:** Više-na-više (M:N). Relacija implementirana preko spojne tabele WorkshopRegistration, omogućavajući praćenje prijava korisnica na radionice.
- **JSON polja:** Kolone `languages`, `experience`, `education` i `skills` pohranjuju strukturirane podatke kao JSON stringove u bazi, a pri čitanju se parsiraju u Python objekte.

### 2.3 JSON struktura složenih polja

**`languages` (niz LanguageEntry objekata):**

```json
[
  { "name": "Bosanski", "level": "Maternji" },
  { "name": "Engleski", "level": "C1" }
]
```

**`experience` (niz ExperienceEntry objekata):**

```json
[
  {
    "title": "Frontend Developer",
    "organization": "TechCo",
    "location": "Sarajevo",
    "start_date": "2022-01",
    "end_date": null,
    "description": "Razvoj React aplikacija"
  }
]
```

**`education` (niz EducationEntry objekata):**

```json
[
  {
    "degree": "Bachelor IT",
    "institution": "Univerzitet u Sarajevu",
    "start_date": "2018-09",
    "end_date": "2022-06",
    "description": null
  }
]
```

**`skills` (niz stringova):**

```json
["Python", "FastAPI", "React", "PostgreSQL"]
```

---

## 3. Pregled Implementiranih Funkcionalnosti

| Funkcionalnost               | Opis                                                                                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- |
| Automatsko kreiranje profila | Profil se automatski kreira pri prvom pristupu ako ne postoji (`get_or_create_profile`)               |
| Čitanje vlastitog profila    | Autentifikovani korisnik može dohvatiti sve podatke svog profila                                      |
| Ažuriranje profila           | Parcijalno ažuriranje – mijenjaju se samo proslijeđena polja                                          |
| Upload avatara               | Podržani formati JPG/JPEG/PNG, max 2MB, UUID naziv fajla                                              |
| Brisanje avatara             | Fizičko brisanje slike sa diska unutar try-except bloka i reset polja u bazi na None.                 |
| Validacija fajlova           | Ograničenje uvoza slika isključivo na JPG/JPEG/PNG formate i veličinu do maksimalno 2MB.              |
| Privacy podešavanja          | `show_biography`, `show_field`, `show_location` kontrolišu vidljivost na javnom profilu               |
| Deaktivacija naloga          | Korisnik može sam deaktivirati nalog; `deactivated_by` bilježi ko je deaktivirao                      |
| Reaktivacija naloga          | Korisnik može reaktivirati nalog putem login provjere s lozinkom                                      |
| Login provjera               | Provjera kredencijala uz detekciju deaktiviranog naloga i ponudu reaktivacije                         |
| Javni profil                 | Javni prikaz profila uz poštovanje privacy polja; email vidljiv samo logovanim korisnicima            |
| JWT autentifikacija          | Bearer token autentifikacija na zaštićenim endpointima                                                |
| Validacija unosa             | Prazno ime i biografija duža od 500 znakova se odbijaju                                               |
| Sigurnosni Auth Guard        | Centralni presretač (get_current_user) koji provjerava token i blokira deaktivirane korisnice (403).  |
| Dinamička reaktivacija       | Vraća reactivatable: true samo ako je korisnica sama ugasila nalog, a false ako ju je blokirao admin. |
| Tabelarni admin pregled      | Spajanje users i profiles tabele za prikaz svih korisnica sa stvarnim statusom aktivnosti.            |
| Admin upravljanje statusom   | Endpoint za administrativno paljenje/gašenje računa uz bilježenje deactivated_by = "admin".           |
| Menadžment uloga             | PUT endpoint koji validira i mijenja ulogu korisnice iz user u admin ili mentor.            |
| Broj nepročitanih notifikacija | Endpoint za prikaz brojčanog badge-a bez mijenjanja statusa pročitanosti.                  |
| Lista notifikacija           | Vraća nepročitane notifikacije obogaćene podacima o radionici (naziv, datum, slobodna mjesta). |
| Brisanje notifikacija        | Markira sve nepročitane notifikacije korisnice kao pročitane.                                |
| Promjena lozinke             | Korisnica mijenja lozinku uz provjeru stare lozinke, podudaranje potvrde i minimalnu dužinu. |
| Historija aktivnosti         | Vraća listu završenih radionica na koje je korisnica bila prijavljena.                       |


---

## 4. Opis Endpointa

Svi endpointi su pod baznom putanjom `/profiles`.

### 4.1 `GET /profiles/me`

**Svrha:** Vraća kompletan profil trenutno autentifikovanog korisnika. Ako profil ne postoji u bazi, automatski ga kreira s defaultnim vrijednostima.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
GET /profiles/me
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):**

```json
{
  "id": 1,
  "user_id": 5,
  "full_name": "Amina Hodžić",
  "email": "amina@example.com",
  "biography": "Full-stack developer s 3 godine iskustva.",
  "field": "Software Engineering",
  "avatar": "/static/avatars/abc123.jpg",
  "role": "user",
  "location": "Sarajevo, BiH",
  "show_biography": true,
  "show_field": true,
  "show_location": true,
  "languages": [{ "name": "Bosanski", "level": "Maternji" }],
  "experience": [{ "title": "Dev", "organization": "TechCo", "...": "..." }],
  "education": [{ "degree": "BSc IT", "institution": "UNSA", "...": "..." }],
  "skills": ["Python", "React"],
  "linkedin_url": "https://linkedin.com/in/amina",
  "github_url": "https://github.com/amina",
  "twitter_url": null
}
```

**Mogući odgovori:**

| HTTP status      | Opis                                          |
| ---------------- | --------------------------------------------- |
| 200 OK           | Profil uspješno vraćen (ili kreiran i vraćen) |
| 401 Unauthorized | Token nije proslijeđen ili je nevažeći        |

---

### 4.2 `PUT /profiles/me`

**Svrha:** Parcijalno ažuriranje profila korisnika. Šalju se samo polja koja se mijenjaju – polja koja nisu uključena u request ostaju nepromijenjena.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request body (sva polja su opcionalna):**

```json
{
  "full_name": "Amina Hodžić",
  "biography": "Ažurirana biografija.",
  "field": "Backend Engineering",
  "location": "Mostar, BiH",
  "email": "novi_email@example.com",
  "show_biography": true,
  "show_field": false,
  "show_location": true,
  "languages": [{ "name": "Engleski", "level": "B2" }],
  "experience": [
    { "title": "Dev", "organization": "Co", "start_date": "2021-01" }
  ],
  "education": [
    { "degree": "BSc", "institution": "UNSA", "start_date": "2018" }
  ],
  "skills": ["Python", "FastAPI"],
  "linkedin_url": "https://linkedin.com/in/amina",
  "github_url": null,
  "twitter_url": null
}
```

**Validacijska pravila:**

- `full_name` ne smije biti prazan string
- `biography` ne smije biti duža od 500 karaktera

**Uspješan odgovor (200 OK):** Isti format kao `GET /profiles/me` – vraća ažurirani `ProfileResponse` objekt.

**Mogući odgovori:**

| HTTP status              | Opis                                          |
| ------------------------ | --------------------------------------------- |
| 200 OK                   | Profil uspješno ažuriran                      |
| 400 Bad Request          | Prazno ime ili biografija prelazi 500 znakova |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći        |
| 422 Unprocessable Entity | Neispravna struktura request body-a           |

---

### 4.3 `POST /profiles/me/avatar`

**Svrha:** Upload profilne slike (avatara). Fajl se čuva na serveru u direktoriju `static/avatars/` s UUID nazivom. URL slike se pohranjuje u profil korisnika.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request (multipart/form-data):**

```http
POST /profiles/me/avatar
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

file: [binaran fajl slike]
```

**Ograničenja:**

- Podržani formati: JPG, JPEG, PNG
- Maksimalna veličina fajla: 2 MB
- Naziv fajla se generiše kao UUID (npr. `a1b2c3d4-...-uuid.jpg`)

**Uspješan odgovor (200 OK):**

```json
{
  "avatar_url": "/static/avatars/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg"
}
```

**Mogući odgovori:**

| HTTP status      | Opis                                         |
| ---------------- | -------------------------------------------- |
| 200 OK           | Avatar uspješno uploadovan                   |
| 400 Bad Request  | Nepodržani format fajla ili fajl veći od 2MB |
| 401 Unauthorized | Token nije proslijeđen ili je nevažeći       |

---

### 4.4 `PATCH /profiles/me/deactivate`

**Svrha:** Korisnik deaktivira vlastiti nalog. Nakon deaktivacije, nalog postaje nevidljiv na javnom profilu i onemogućen je login. Polje `deactivated_by` se postavlja na `'user'`.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
PATCH /profiles/me/deactivate
Authorization: Bearer <jwt_token>
```

Nema request body-a.

**Uspješan odgovor (200 OK):**

```json
{
  "message": "Vaš nalog je uspješno deaktiviran."
}
```

**Mogući odgovori:**

| HTTP status      | Opis                                   |
| ---------------- | -------------------------------------- |
| 200 OK           | Nalog uspješno deaktiviran             |
| 401 Unauthorized | Token nije proslijeđen ili je nevažeći |

---

### 4.5 `POST /profiles/login-check`

**Svrha:** Provjera korisničkih kredencijala pri logovanju. Ako je nalog deaktiviran, vraća poseban odgovor s informacijom o mogućnosti reaktivacije. Endpoint ne zahtijeva autentifikaciju.

**Autentifikacija:** Nije potrebna (javni endpoint)

**Request body:**

```json
{
  "email": "amina@example.com",
  "password": "lozinka123"
}
```

**Uspješan odgovor (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Odgovor za deaktiviran nalog (403):**

```json
{
  "detail": {
    "message": "Vaš nalog je deaktiviran. Želite li ga reaktivirati?",
    "reactivatable": true
  }
}
```

**Mogući odgovori:**

| HTTP status              | Opis                                                        |
| ------------------------ | ----------------------------------------------------------- |
| 200 OK                   | Kredencijali ispravni, vraća JWT token                      |
| 401 Unauthorized         | Neispravni email ili lozinka                                |
| 403 Forbidden            | Nalog je deaktiviran; response sadrži `reactivatable: true` |
| 422 Unprocessable Entity | Nedostaje email ili password u body-u                       |

---

### 4.6 `POST /profiles/reactivate`

**Svrha:** Reaktivacija prethodno deaktiviranog naloga. Korisnik mora proslijediti ispravne kredencijale. Po uspješnoj reaktivaciji, vraća se novi JWT token.

**Autentifikacija:** Nije potrebna (javni endpoint)

**Request body:**

```json
{
  "email": "amina@example.com",
  "password": "lozinka123"
}
```

**Uspješan odgovor (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Mogući odgovori:**

| HTTP status              | Opis                               |
| ------------------------ | ---------------------------------- |
| 200 OK                   | Nalog reaktiviran, vraća JWT token |
| 401 Unauthorized         | Neispravni kredencijali            |
| 404 Not Found            | Profil nije pronađen u bazi        |
| 422 Unprocessable Entity | Nedostaje email ili password       |

---

### 4.7 `GET /profiles/{user_id}`

**Svrha:** Dohvatanje javnog profila korisnika po ID-u. Poštuju se privacy podešavanja (`show_biography`, `show_field`, `show_location`). Email korisnika je vidljiv samo ako je zahtjev poslan s važećim JWT tokenom. Admin nalozi i deaktivirani profili nisu vidljivi.

**Autentifikacija:** Opcionalna – Bearer token za prikaz email adrese

**Request:**

```http
GET /profiles/42
Authorization: Bearer <jwt_token>   ← opcionalno
```

**Uspješan odgovor (200 OK) – logovani korisnik:**

```json
{
  "full_name": "Amina Hodžić",
  "field": "Software Engineering",
  "biography": "Full-stack developer...",
  "avatar": "/static/avatars/abc123.jpg",
  "email": "amina@example.com",
  "location": "Sarajevo",
  "languages": [{ "name": "Bosanski", "level": "Maternji" }],
  "experience": ["..."],
  "education": ["..."],
  "skills": ["Python", "React"],
  "linkedin_url": "https://linkedin.com/in/amina",
  "github_url": null,
  "twitter_url": null
}
```
---

### 4.8 `GET /profiles/dashboard`

**Svrha:** Generiše i vraća personalizovane podatke za dashboard u zavisnosti od uloge trenutno autentifikovane korisnice (user, mentor, admin).

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
GET /profiles/dashboard
Authorization: Bearer <jwt_token>
```

**Mogući odgovori:**

| HTTP status              | Opis                                                                      |
| ------------------------ | ------------------------------------------------------------------------- |
| 200 OK                   | Podaci za ulogovanu ulogu (Korisnica/Mentorica/Admin) uspješno generisani |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći                                    |

**Napomena:** Struktura odgovora se dinamički mijenja u zavisnosti od uloge u tokenu.

---

### 4.9 `POST /profiles/dashboard/register`

**Svrha:** Prijava na radionicu preko query parametra workshop_id. Ova akcija je strogo rezervisana samo za ulogu "user", dok mentorice i admini nemaju pravo prijave kao polaznici.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
POST /profiles/dashboard/register?workshop_id=1
Authorization: Bearer <jwt_token>
```
**Validacijska pravila:**

- Radionica mora postojati u bazi podataka.
- Ulogovana osoba mora imati ulogu user (u suprotnom sistem baca 403).
- Datum održavanja radionice ne smije biti u prošlosti.
- Korisnica ne smije biti već prijavljena na istu radionicu.
- Broj trenutno prijavljenih korisnica mora biti manji od maksimalnog kapaciteta radionice.

**Mogući odgovori:**

| HTTP status              | Opis                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------ |
| 201 Created              | Prijava na radionicu uspješno kreirana                                               |
| 400 Bad Request          | Radionica je prošla, popunjen je kapacitet ili je korisnica već prijavljena          |      
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći                                               |                
| 403 Forbidden            | Pristup odbijen (Mentorice i admini se ne mogu prijaviti na radionice kao polaznici) |
| 404 Not Found            | Radionica sa proslijeđenim ID-em ne postoji                                          |            

---

### 4.10 `DELETE /profiles/me/avatar`

**Svrha:** Sigurno i trajno brisanje profilne slike sa servera i iz baze podataka. Metoda provjerava postojanje fajla na disku unutar zaštićenog bloka, vrši fizičko brisanje i resetuje polje avatar na null.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
DELETE /profiles/me/avatar
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):** Vraća očišćeni ProfileResponse objekat gdje je polje avatar postavljeno na null.

```json
{
  "id": 1,
  "user_id": 5,
  "full_name": "Amina Hodžić",
  "email": "amina@example.com",
  "biography": "Full-stack developer s 3 godine iskustva.",
  "field": "Software Engineering",
  "avatar": null,
  "role": "user"
}
```

**Mogući odgovori:**

| HTTP status              | Opis                                              |
| ------------------------ | ------------------------------------------------- |
| 200 OK                   | Avatar uspješno obrisan sa diska i baze podataka  |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći            |                

---

### 4.11 `GET /admin/users`

**Svrha:** Administratorski pregled svih registrovanih korisnica. Sistem spaja bazične podatke iz tabele User sa stanjem aktivnosti računa iz tabele Profile.

**Autentifikacija:** Bearer JWT token + Uloga ADMIN (obavezno)

**Request:**

```http
GET /admin/users
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):** 

```json
{
    "id": 5,
    "full_name": "Amina Hodžić",
    "email": "amina@example.com",
    "role": "user",
    "is_active": true
}
```

**Mogući odgovori:**

| HTTP status              | Opis                                                               |
| ------------------------ | ------------------------------------------------------------------ |
| 200 OK                   | Lista korisnica sa proširenim profilnim podacima uspješno vraćena  |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći                             |   
| 403 Forbidden            | Pristup odbijen (Ulogovana korisnica nema ulogu administratora)    |             

---

### 4.12 `PUT /admin/{user_id}/status`

**Svrha:** Omogućava administratoru da ručno aktivira ili deaktivira račun bilo koje korisnice preko query parametra is_active. Ukoliko admin ugasi nalog, polje deactivated_by se postavlja na 'admin'.

**Autentifikacija:** Bearer JWT token + Uloga ADMIN (obavezno)

**Request:**

```http
PUT /admin/5/status?is_active=false
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):** 

```json
{
  "message": "Status korisnice je uspješno promijenjen na: deaktivirana.",
  "user_id": 5,
  "is_active": false
}
```

**Mogući odgovori:**

| HTTP status              | Opis                                                |
| ------------------------ | --------------------------------------------------- |
| 200 OK                   | Status aktivnosti korisnice uspješno izmijenjen     |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći              |   
| 403 Forbidden            | Samo administratori mogu mijenjati status korisnika |             

---

### 4.13 `PUT /admin/{user_id}/role`

**Svrha:** Administrativna promjena sistemske uloge korisnice na osnovu proslijeđenog tijela zahtjeva (UpdateRoleRequest). Admin može dodijeliti ulogu user, mentor ili admin.

**Autentifikacija:** Bearer JWT token + Uloga ADMIN (obavezno)

**Request:**

```json
{
  "role": "mentor"
}
```

**Uspješan odgovor (200 OK):** 

```json
{
  "message": "Uloga korisnice Amina Hodžić je uspješno promijenjena.",
  "user_id": 5,
  "role": "mentor"
}
```

**Mogući odgovori:**

| HTTP status              | Opis                                                               |
| ------------------------ | ------------------------------------------------------------------ |
| 200 OK                   | Uloga uspješno ažurirana i pohranjena u bazu  |
| 401 Unauthorized         | Token nije proslijeđen ili je nevažeći                             |   
| 403 Forbidden            | Samo administrator ima dozvolu za mijenjanje uloga                 |    
| 404 Not Found            | Korisnica sa proslijeđenim ID-em nije pronađena                    |
| 422 Unprocessable Entity | Proslijeđena nepostojeća ili nevalidna uloga u body-u              |

---

### 4.14 `GET /profiles/notifications/count`

**Svrha:** Vraća broj nepročitanih notifikacija za trenutno ulogovanog korisnika. Ne mijenja stanje pročitanosti notifikacija — koristi se isključivo za prikaz badge-a.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
GET /profiles/notifications/count
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):**

```json
{ "count": 3 }
```

**Mogući odgovori:**

| HTTP status      | Opis                                    |
| ----------------- | ---------------------------------------- |
| 200 OK            | Broj nepročitanih notifikacija vraćen   |
| 401 Unauthorized  | Token nije proslijeđen ili je nevažeći  |

**Napomena:** Endpoint mora biti definiran prije rute `GET /{user_id}` u `profiles.py` (vidi sekciju 7.2).

---

### 4.15 `GET /profiles/notifications`

**Svrha:** Vraća listu nepročitanih notifikacija korisnika, obogaćenu podacima o radionici. Naziv radionice se izdvaja iz teksta notifikacije pomoću regex-a, nakon čega se radionica pronalazi u bazi i dodaju se njen datum i broj slobodnih mjesta.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
GET /profiles/notifications
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Nova radionica je dostupna!",
    "body": "Objavljena je radionica: 'Python za početnike'. Prijavite se na vrijeme!",
    "workshop": {
      "title": "Python za početnike",
      "date": "2026-07-15T10:00:00",
      "free_spots": 12
    }
  }
]
```

**Mogući odgovori:**

| HTTP status      | Opis                                    |
| ----------------- | ---------------------------------------- |
| 200 OK            | Lista nepročitanih notifikacija vraćena |
| 401 Unauthorized  | Token nije proslijeđen ili je nevažeći  |

**Napomena:** Endpoint ne markira notifikacije automatski kao pročitane — to se vrši tek pozivom `DELETE /profiles/notifications`. Mora biti definiran prije rute `GET /{user_id}` (vidi sekciju 7.2).

---

### 4.16 `DELETE /profiles/notifications`

**Svrha:** Markira sve nepročitane notifikacije korisnika kao pročitane (`is_read = True`).

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
DELETE /profiles/notifications
Authorization: Bearer <jwt_token>
```

**Uspješan odgovor (200 OK):**

```json
{ "deleted": 3 }
```

**Mogući odgovori:**

| HTTP status      | Opis                                       |
| ----------------- | -------------------------------------------- |
| 200 OK            | Notifikacije uspješno markirane kao pročitane |
| 401 Unauthorized  | Token nije proslijeđen ili je nevažeći       |

---

### 4.17 `PATCH /profiles/me/change-password`

**Svrha:** Omogućava korisnici promjenu vlastite lozinke uz provjeru identiteta putem stare lozinke.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request body (`ChangePasswordRequest`):**

```json
{
  "old_password": "staralozinka",
  "new_password": "novalozinka123",
  "confirm_new_password": "novalozinka123"
}
```

**Validacijska pravila:**

- Stara lozinka mora biti ispravna (provjera putem `verify_password` nad `password_hash`)
- Nova lozinka i potvrda nove lozinke moraju biti identične
- Nova lozinka mora imati najmanje 8 karaktera

**Uspješan odgovor (200 OK):**

```json
{ "message": "Lozinka uspješno promijenjena." }
```

**Mogući odgovori:**

| HTTP status      | Opis                                              |
| ----------------- | --------------------------------------------------- |
| 200 OK            | Lozinka uspješno promijenjena                       |
| 400 Bad Request   | Stara lozinka nije tačna                            |
| 400 Bad Request   | Nova lozinka i potvrda se ne poklapaju              |
| 400 Bad Request   | Nova lozinka mora imati najmanje 8 karaktera        |
| 401 Unauthorized  | Token nije proslijeđen ili je nevažeći              |

---

### 4.18 `GET /profiles/me/history`

**Svrha:** Vraća listu radionica koje je korisnica pohađala — odnosno radionica čiji je datum završetka već prošao, a na koje je korisnica bila prijavljena.

**Autentifikacija:** Bearer JWT token (obavezan)

**Request:**

```http
GET /profiles/me/history
Authorization: Bearer <jwt_token>
```

**Logika upita:**

- JOIN između `Workshop` i `WorkshopRegistration` tabele po `WorkshopRegistration.workshop_id == Workshop.ID_workshop`
- Filter: korisnica je prijavljena na radionicu (`user_id == current_user.id`)
- Filter: radionica je završena — koristi se `func.coalesce(Workshop.end_time, Workshop.date) < datetime.utcnow()`, jer neke radionice nemaju `end_time` pa se u tom slučaju koristi `date` kao fallback
- Sortiranje: od najnovije prema najstarijoj (`Workshop.date.desc()`)

**Uspješan odgovor (200 OK):** Lista `Workshop` objekata (`title`, `date`, `description`, `capacity`, itd.)

**Mogući odgovori:**

| HTTP status      | Opis                                       |
| ----------------- | -------------------------------------------- |
| 200 OK            | Historija radionica uspješno vraćena         |
| 401 Unauthorized  | Token nije proslijeđen ili je nevažeći       |

---

> **Napomena:** Polja `field`, `biography` i `location` vraćaju `null` ako korisnik ima isključena odgovarajuća privacy podešavanja (npr. `show_biography: false`).

**Mogući odgovori:**

| HTTP status   | Opis                                                             |
| ------------- | ---------------------------------------------------------------- |
| 200 OK        | Javni profil uspješno vraćen                                     |
| 404 Not Found | Korisnik ne postoji, nalog je deaktiviran, ili je korisnik admin |

---

## 5. Opis Shema (Pydantic/SQLModel modeli)

### 5.1 `ProfileUpdate` – Shema za ažuriranje profila

Sve vrijednosti su opcionalne. Validira se samo ono što je proslijeđeno.

| Polje            | Tip                               | Validacija / Napomena        |
| ---------------- | --------------------------------- | ---------------------------- |
| `full_name`      | `Optional[str]`                   | Ne smije biti prazan string  |
| `biography`      | `Optional[str]`                   | Maksimalno 500 karaktera     |
| `field`          | `Optional[str]`                   | Oblast struke                |
| `location`       | `Optional[str]`                   | Lokacija                     |
| `email`          | `Optional[str]`                   | Nova email adresa            |
| `show_biography` | `Optional[bool]`                  | Privacy podešavanje          |
| `show_field`     | `Optional[bool]`                  | Privacy podešavanje          |
| `show_location`  | `Optional[bool]`                  | Privacy podešavanje          |
| `languages`      | `Optional[List[LanguageEntry]]`   | Lista jezičnih kompetenci    |
| `experience`     | `Optional[List[ExperienceEntry]]` | Lista radnih iskustava       |
| `education`      | `Optional[List[EducationEntry]]`  | Lista edukacija              |
| `skills`         | `Optional[List[str]]`             | Lista vještina kao stringovi |
| `linkedin_url`   | `Optional[str]`                   | URL LinkedIn profila         |
| `github_url`     | `Optional[str]`                   | URL GitHub profila           |
| `twitter_url`    | `Optional[str]`                   | URL Twitter/X profila        |

### 5.2 `ProfileResponse` – Odgovor za vlastiti profil

Vraća se pri `GET /me` i `PUT /me`.

| Polje                                             | Tip                               | Opis                    |
| ------------------------------------------------- | --------------------------------- | ----------------------- |
| `id`                                              | `int`                             | ID profila              |
| `user_id`                                         | `int`                             | ID korisnika            |
| `full_name`                                       | `str`                             | Puno ime                |
| `email`                                           | `str`                             | Email adresa            |
| `role`                                            | `str`                             | Uloga: `user` / `admin` |
| `biography`                                       | `Optional[str]`                   | Biografija              |
| `field`                                           | `Optional[str]`                   | Oblast                  |
| `avatar`                                          | `Optional[str]`                   | URL avatara             |
| `location`                                        | `Optional[str]`                   | Lokacija                |
| `show_biography` / `show_field` / `show_location` | `bool`                            | Privacy podešavanja     |
| `languages`                                       | `Optional[List[LanguageEntry]]`   | Jezici                  |
| `experience`                                      | `Optional[List[ExperienceEntry]]` | Iskustvo                |
| `education`                                       | `Optional[List[EducationEntry]]`  | Obrazovanje             |
| `skills`                                          | `Optional[List[str]]`             | Vještine                |
| `linkedin_url` / `github_url` / `twitter_url`     | `Optional[str]`                   | Društvene mreže         |

### 5.3 `PublicProfileResponse` – Odgovor za javni profil

Vraća se pri `GET /profiles/{user_id}`. Email je vidljiv samo uz autentifikaciju.

| Polje                                               | Tip              | Napomena                                    |
| --------------------------------------------------- | ---------------- | ------------------------------------------- |
| `full_name`                                         | `str`            | Uvijek vidljivo                             |
| `field`                                             | `Optional[str]`  | Vidljivo samo ako je `show_field: true`     |
| `biography`                                         | `Optional[str]`  | Vidljivo samo ako je `show_biography: true` |
| `avatar`                                            | `Optional[str]`  | Uvijek vidljivo (ako postoji)               |
| `email`                                             | `Optional[str]`  | Vidljivo samo uz Bearer token               |
| `location`                                          | `Optional[str]`  | Vidljivo samo ako je `show_location: true`  |
| `languages` / `experience` / `education` / `skills` | `Optional[List]` | Uvijek vidljivo (ako postoji)               |
| `linkedin_url` / `github_url` / `twitter_url`       | `Optional[str]`  | Uvijek vidljivo (ako postoji)               |

### 5.4 `UpdateRoleRequest` – Zahtjev za promjenu uloge korisnice

Koristi se kao Request Body pri administrativnoj izmjeni uloge na endpointu PUT /admin/{user_id}/role.

| Polje                                               | Tip              | Napomena                                               |
| --------------------------------------------------- | ---------------- | ------------------------------------------------------ |
| `role`                                              | UserRole (Enum)  | Prima samo vrijednosti: "user", "mentor" ili "admin".  |

### 5.5 Pomoćni modeli

| Model             | Polja                                                                        | Opis               |
| ----------------- | ---------------------------------------------------------------------------- | ------------------ |
| `LanguageEntry`   | `name: str`, `level: Optional[str]`                                          | Jezična kompetenca |
| `ExperienceEntry` | `title`, `organization`, `location`, `start_date`, `end_date`, `description` | Radno iskustvo     |
| `EducationEntry`  | `degree`, `institution`, `start_date`, `end_date`, `description`             | Obrazovanje        |

### 5.6 `ChangePasswordRequest` – Zahtjev za promjenu lozinke

Koristi se kao Request Body pri endpointu `PATCH /profiles/me/change-password`. Definiran u `backend/app/models/profile.py`.

| Polje                   | Tip   | Napomena                                    |
| ------------------------ | ----- | -------------------------------------------- |
| `old_password`           | `str` | Trenutna lozinka korisnice (provjera identiteta) |
| `new_password`           | `str` | Nova lozinka, minimalno 8 karaktera          |
| `confirm_new_password`   | `str` | Mora se podudarati s `new_password`          |

---

## 6. Autentifikacija

API koristi JWT (JSON Web Token) autentifikaciju. Token se dobija pri uspješnom loginu i šalje u `Authorization` headeru svakog zaštićenog zahtjeva.

**Format headera:**

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

| Endpoint                            | Autentifikacija                         |
| ----------------------------------- | --------------------------------------- |
| `GET /profiles/me`                  | Obavezna                                |
| `PUT /profiles/me`                  | Obavezna                                |
| `POST /profiles/me/avatar`          | Obavezna                                |
| `PATCH /profiles/me/deactivate`     | Obavezna                                |
| `POST /profiles/login-check`        | Nije potrebna                           |
| `POST /profiles/reactivate`         | Nije potrebna                           |
| `GET /profiles/{user_id}`           | Opcionalna (utiče na vidljivost emaila) |
| `GET /profiles/dashboard`           | Obavezna                                |
| `POST /profiles/dashboard/register` | Obavezna (samo za ulogu "user")         |
| `DELETE /profiles/me/avatar`        | Obavezna                                |
| `GET /admin/users`                  | Obavezna (samo za ulogu "admin")        |
| `PUT /admin/{user_id}/status`       | Obavezna (samo za ulogu "admin")        |
| `PUT /admin/{user_id}/role`         | Obavezna (samo za ulogu "admin")        |
| `GET /profiles/notifications/count` | Obavezna                                |
| `GET /profiles/notifications`       | Obavezna                                |
| `DELETE /profiles/notifications`    | Obavezna                                |
| `PATCH /profiles/me/change-password`| Obavezna                                |
| `GET /profiles/me/history`          | Obavezna                                |

---
