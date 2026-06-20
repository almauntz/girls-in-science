//amel













//elma
# Modul: Prijava i odjava sa radionice (Registration)

## Svrha modula

Ovaj dio backend-a omogućava ulogovanim korisnicima da se prijave na radionicu, odjave sa radionice na koju su prijavljeni, te provjera da li su već prijavljeni na određenu radionicu. Sva tri endpointa zahtijevaju autentifikaciju (`Depends(get_current_user)`).

## Pregled implementiranih funkcionalnosti

- Prijava na radionicu, sa validacijama: postojanje radionice, slobodan kapacitet,
- Odjava sa radionice na koju je korisnik prijavljen
- Provjera statusa prijave (da li je korisnik već prijavljen na konkretnu radionicu)


---

## Opis baze podataka — entitet `Registration`

| Kolona | Tip | Opis |
|---|---|---|
| `id` | Integer, PK | Jedinstveni identifikator prijave |
| `user_id` | Integer, FK → `users.id` | Korisnik koji je izvršio prijavu |
| `first_name` | String | Ime |
| `last_name` | String | Prezime |
| `email` | String | Email korišten prilikom prijave |
| `phone` | String | Broj telefona |
| `workshop_id` | Integer | ID radionice na koju se prijava odnosi (referenca na `Workshop`) |
| `previous_experience` | String, nullable | Opcioni opis prethodnog iskustva |
| `github_profile` | String, nullable | Opcioni link na GitHub profil |
| `status` | String, default `"registered"` | Status prijave |
| `created_at` | DateTime, default `utcnow` | Vrijeme kreiranja prijave |
| `was_promoted` | Boolean, default `False` | Indikator da li je prijava promovisana sa liste čekanja (koristi se u dijelu sistema za listu čekanja, nije obuhvaćeno ovim modulom) |

**Relacije:**
- `Registration.user_id` →  `User` (jedan korisnik može imati više prijava, za različite radionice)
- `Registration.workshop_id` →  `Workshop`, koristi se za provjeru kapaciteta

**Indeks:**
```
idx_workshop_status_created (workshop_id, status, created_at)
```
Kompozitni indeks koji ubrzava upite po radionici i statusu, te omogućava obradu liste čekanja (funkcionalnost koja je implementirana u drugom dijelu sistema, ne u ovom modulu).

---

## Endpoint 1 — Prijava na radionicu

**`POST /registration`**

**Namjena:** Prijavljuje ulogovanog korisnika na radionicu, uz provjeru kapaciteta i sprečavanje duplih prijava.

**Autentifikacija:** Obavezna (Bearer token / ulogovan korisnik)

**Request body:**
```json
{
  "first_name": "Amina",
  "last_name": "Hodžić",
  "email": "amina.hodzic@example.com",
  "phone": "061123456",
  "workshop_id": 3,
  "previous_experience": "Završen kurs Pythona",
  "github_profile": "https://github.com/aminahodzic"
}
```

**Mogući responses:**

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `201 Created` | Uspješna prijava | `{"message": "Uspješna prijava!", "free_spots_left": 4}` |
| `404 Not Found` | Radionica ne postoji | `{"detail": "Radionica nije pronađena"}` |
| `400 Bad Request` | Nema slobodnih mjesta | `{"detail": "Nažalost, sva mjesta su popunjena!"}` |
| `400 Bad Request` | Email već prijavljen na tu radionicu | `{"detail": "Ovaj email već je registrovan!"}` |
| `400 Bad Request` | Korisnik (account) već prijavljen na tu radionicu | `{"detail": "Već ste prijavljeni (user)!"}` |

---

## Endpoint 2 — Odjava sa radionice

**`DELETE /cancellation/{workshop_id}`**

**Namjena:** Briše prijavu ulogovanog korisnika za navedenu radionicu (identifikacija po email-u trenutnog korisnika).

**Autentifikacija:** Obavezna

**Path parametar:** `workshop_id` (int)

**Mogući responses:**


| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Uspješna odjava, niko na waiting listi | `{"message": "Uspješno ste odustali od radionice.", "promoted_user_id": null}` |
| `200 OK` | Uspješna odjava, korisnik sa waiting liste promovisan | `{"message": "Uspješno ste odustali od radionice.", "promoted_user_id": 7}` |
| `404 Not Found` | Korisnik nema prijavu za tu radionicu | `{"detail": "Nije pronađena vaša prijava za ovu radionicu."}` |

---

## Endpoint 3 — Provjera statusa prijave

**`GET /registration/check/{workshop_id}`**

**Namjena:** Provjerava da li je ulogovani korisnik već prijavljen na navedenu radionicu (koristi se npr. da frontend prikaže dugme "Prijavi se" ili "Odjavi se").

**Autentifikacija:** Obavezna

**Path parametar:** `workshop_id` (int)

**Mogući response:**

| Status | Primjer body-ja |
|---|---|
| `200 OK` | `{"registered": true}` ili `{"registered": false}` |







//maida

# Modul: Pregled, pretraga i ocjenjivanje radionica

## Svrha modula

Ovaj dio backend-a omogućava javni pregled i pretragu radionica (filteri po nazivu, lokaciji i datumu), prikaz detalja radionice sa informacijom o slobodnim mjestima, automatsko ažuriranje statusa radionice nakon isteka vremena održavanja, te ocjenjivanje radionice od strane korisnica koje su na njoj bile prijavljene.

## Pregled implementiranih funkcionalnosti

- Pretraga i filtriranje radionica po nazivu, lokaciji i rasponu datuma
- Pregled svih aktivnih (nadolazećih i završenih) radionica
- Prikaz detalja jedne radionice, uključujući broj slobodnih mjesta
- Automatsko ažuriranje statusa radionice u "completed" nakon isteka vremena održavanja
- Ostavljanje ocjene (1–5) za radionicu nakon njenog završetka, sa provjerom da je korisnica bila prijavljena i da nije već ocijenila
- Pregled svih ocjena za radionicu, sa imenom korisnice
- Prikaz prosječne ocjene i broja ocjena za radionicu

---

## Opis baze podataka — entitet `Workshop`

| Kolona | Tip | Opis |
|---|---|---|
| `ID_workshop` | Integer, PK | Jedinstveni identifikator radionice |
| `title` | String | Naziv radionice |
| `description` | String | Opis radionice |
| `location` | String | Lokacija održavanja |
| `date` | DateTime | Datum i vrijeme početka |
| `end_time` | DateTime | Datum i vrijeme završetka |
| `capacity` | Integer | Maksimalan broj mjesta |
| `status` | Enum (`upcoming`, `cancelled`, `completed`) | Status radionice, default `upcoming` |
| `created_by_id` | Integer, nullable | ID admina koji je kreirao radionicu |
| `created_at` | DateTime | Vrijeme kreiranja |
| `organizer_name` | String, nullable | Ime organizatora |
| `organizer_email` | String, nullable | Email organizatora |
| `organizer_phone` | String, nullable | Telefon organizatora |

**Relacije:**
- `Workshop.ID_workshop` ← referenciran iz `Registration.workshop_id`, `WaitingList.workshop_id` i `WorkshopRating.workshop_id`

---

## Opis baze podataka — entitet `WorkshopRating`

| Kolona | Tip | Opis |
|---|---|---|
| `id` | Integer, PK | Jedinstveni identifikator ocjene |
| `registration_id` | Integer, FK → `registration.id`, UNIQUE | Prijava na koju se ocjena odnosi (jedna ocjena po prijavi) |
| `user_id` | Integer, FK → `users.id` | Korisnica koja je ostavila ocjenu |
| `workshop_id` | Integer | Radionica koja se ocjenjuje (referenca na `Workshop`) |
| `score` | Integer | Ocjena, 1–5 |
| `comment` | String, nullable | Opcioni komentar |
| `created_at` | DateTime | Vrijeme kreiranja ocjene |

**Relacije:**
- `WorkshopRating.registration_id` → `Registration`
- `WorkshopRating.user_id` → `User`
- `WorkshopRating.workshop_id` → `Workshop`

---

## Endpoint 1 — Pretraga radionica

**`GET /workshops/search`**

**Namjena:** Pretraga/filtriranje radionica po nazivu, lokaciji i rasponu datuma.

**Autentifikacija:** Nije potrebna

**Query parametri** (svi opcionalni): `title`, `location`, `date_from`, `date_to`

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Uspješna pretraga | `[{"ID_workshop": 5, "title": "Uvod u Python", "date": "2026-07-10T17:00:00", "location": "Sarajevo", "free_spots": 12, "status": "upcoming"}]` |

---

## Endpoint 2 — Aktivne radionice

**`GET /workshops/active`**

**Namjena:** Lista radionica sa statusom `upcoming` ili `completed`.

**Autentifikacija:** Nije potrebna

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Lista aktivnih radionica | Isti format kao `/search` |

---

## Endpoint 3 — Detalji radionice

**`GET /workshops/{workshop_id}`**

**Namjena:** Detalji jedne radionice — datum, lokacija, opis, kapacitet, slobodna mjesta.

**Autentifikacija:** Nije potrebna

**Path parametar:** `workshop_id` (int)

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Radionica pronađena | `{"ID_workshop": 5, "title": "Uvod u Python", "capacity": 20, "free_spots": 12, "status": "upcoming"}` |
| `404 Not Found` | Radionica ne postoji | `{"detail": "Radionica nije pronađena."}` |

---

## Endpoint 4 — Automatsko ažuriranje statusa

**`POST /workshops/auto-complete`**

**Namjena:** Automatski mijenja status radionica čiji je `end_time` prošao u `completed`.

**Autentifikacija:** Nije potrebna.

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Uspješno izvršeno | `{"message": "3 radionica označeno kao završeno."}` |

---

## Endpoint 5 — Ocjenjivanje radionice

**`POST /workshops/{workshop_id}/ratings`**

**Namjena:** Korisnica ostavlja ocjenu nakon završene radionice.

**Autentifikacija:** Obavezna (mora biti bila prijavljena na tu radionicu)

**Path parametar:** `workshop_id` (int)

**Request body:**
```json
{ "score": 5, "comment": "Odlična radionica, puno sam naučila!" }
```

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `201 Created` | Uspješno ocjenjeno | `{"id": 12, "score": 5, "comment": "...", "user_name": null}` |
| `404 Not Found` | Radionica ne postoji | `{"detail": "Radionica nije pronađena."}` |
| `400 Bad Request` | Radionica još nije završena | `{"detail": "Radionica još nije završena."}` |
| `403 Forbidden` | Korisnica nije bila prijavljena | `{"detail": "Niste bili prijavljeni na ovu radionicu."}` |
| `409 Conflict` | Već ocjenjeno | `{"detail": "Već ste ocjenili ovu radionicu."}` |

---

## Endpoint 6 — Pregled ocjena

**`GET /workshops/{workshop_id}/ratings`**

**Namjena:** Lista svih ocjena za radionicu, najnovije prve, sa imenom korisnice.

**Autentifikacija:** Nije potrebna

**Path parametar:** `workshop_id` (int)

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK` | Lista ocjena | `[{"id": 12, "score": 5, "comment": "Odlična radionica!", "user_name": "Maida Kamenčić"}]` |

---

## Endpoint 7 — Prosječna ocjena

**`GET /workshops/{workshop_id}/ratings/average`**

**Namjena:** Prosječna ocjena i broj ocjena za radionicu.

**Autentifikacija:** Nije potrebna

**Path parametar:** `workshop_id` (int)

**Mogući responses:**

| Status | Primjer body-ja |
|---|---|
| `200 OK` | `{"average": 4.67, "count": 3}` |





//mahir