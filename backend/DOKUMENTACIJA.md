# Girls in Science — Backend Dokumentacija

---

## 1. Struktura Backend Projekta

```
backend/
├── app/
│ ├── main.py (ulazna tačka aplikacije, registracija routera)
│ ├── auth.py (JWT autentifikacija, kreiranje i dekodiranje tokena)
│ ├── database.py (konfiguracija baze podataka i sesije)
│ ├── routers/
│ │ └── profiles.py (endpointi za upravljanje profilima)
│ └── models/
│   └── profile.py (SQLModel modeli i Pydantic sheme)
└── static/
  └── avatars/ (direktorij za pohranu avatar slika)
```

---

## 2. Opis Baze Podataka

### 2.1 Entiteti i ključne tabele

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

| Funkcionalnost               | Opis                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| Automatsko kreiranje profila | Profil se automatski kreira pri prvom pristupu ako ne postoji (`get_or_create_profile`)    |
| Čitanje vlastitog profila    | Autentifikovani korisnik može dohvatiti sve podatke svog profila                           |
| Ažuriranje profila           | Parcijalno ažuriranje – mijenjaju se samo proslijeđena polja                               |
| Upload avatara               | Podržani formati JPG/JPEG/PNG, max 2MB, UUID naziv fajla                                   |
| Privacy podešavanja          | `show_biography`, `show_field`, `show_location` kontrolišu vidljivost na javnom profilu    |
| Deaktivacija naloga          | Korisnik može sam deaktivirati nalog; `deactivated_by` bilježi ko je deaktivirao           |
| Reaktivacija naloga          | Korisnik može reaktivirati nalog putem login provjere s lozinkom                           |
| Login provjera               | Provjera kredencijala uz detekciju deaktiviranog naloga i ponudu reaktivacije              |
| Javni profil                 | Javni prikaz profila uz poštovanje privacy polja; email vidljiv samo logovanim korisnicima |
| JWT autentifikacija          | Bearer token autentifikacija na zaštićenim endpointima                                     |
| Validacija unosa             | Prazno ime i biografija duža od 500 znakova se odbijaju                                    |

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

### 5.4 Pomoćni modeli

| Model             | Polja                                                                        | Opis               |
| ----------------- | ---------------------------------------------------------------------------- | ------------------ |
| `LanguageEntry`   | `name: str`, `level: Optional[str]`                                          | Jezična kompetenca |
| `ExperienceEntry` | `title`, `organization`, `location`, `start_date`, `end_date`, `description` | Radno iskustvo     |
| `EducationEntry`  | `degree`, `institution`, `start_date`, `end_date`, `description`             | Obrazovanje        |

---

## 6. Autentifikacija

API koristi JWT (JSON Web Token) autentifikaciju. Token se dobija pri uspješnom loginu i šalje u `Authorization` headeru svakog zaštićenog zahtjeva.

**Format headera:**

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

| Endpoint                        | Autentifikacija                         |
| ------------------------------- | --------------------------------------- |
| `GET /profiles/me`              | Obavezna                                |
| `PUT /profiles/me`              | Obavezna                                |
| `POST /profiles/me/avatar`      | Obavezna                                |
| `PATCH /profiles/me/deactivate` | Obavezna                                |
| `POST /profiles/login-check`    | Nije potrebna                           |
| `POST /profiles/reactivate`     | Nije potrebna                           |
| `GET /profiles/{user_id}`       | Opcionalna (utiče na vidljivost emaila) |
