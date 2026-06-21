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

# Modul: Upravljanje listom čekanja za radionice (waiting list)
## Svrha modula

Ovaj modul omogućava efikasno upravljanje prijavama na radionice u slučajevima kada je kapacitet popunjen. Kada radionica dostigne maksimalan broj učesnika, korisnici se automatski preusmjeravaju na listu čekanja. Modul prati redoslijed prijava i omogućava automatsko prebacivanje korisnika sa liste čekanja na radionicu kada se oslobodi mjesto.



## Pregled implementiranih funkcionalnosti :

Ograničavanje prijava na radionicu u skladu sa definisanim kapacitetom
Dodavanje korisnika na listu čekanja kada je kapacitet popunjen, korisnik
se sam mora prijaviti na listu čekanja.
Prikaz trenutnog statusa prijave (prijavljen / lista čekanja)
Automatsko prebacivanje korisnika sa liste čekanja na radionicu kada se oslobodi mjesto
Slanje obavijesti korisniku prilikom prelaska sa liste čekanja na radionicu.


---

## Opis baze podataka — entitet `WaitingList`

| Kolona | Tip | Opis |
|---|---|---|
| `id`| Integer, PK | Jedinstveni identifikator zapisa na listi čekanja |
| `user_id` | Integer, FK     | ID korisnika koji se nalazi na listi čekanja |
| `workshop_id` | Integer, FK | ID radionice za koju korisnik čeka slobodno mjesto |
| `created_at`  | DateTime    | Vrijeme kada je korisnik dodat na listu čekanja    |

**Relacije:**

* `WaitingList.user_id` → referencira `users.id`
* `WaitingList.workshop_id` → referencira `Workshop.ID_workshop`

---

## Endpoint 1 — Prijava na listu čekanja

**`POST /workshops/waiting-list/join/{workshop_id}`**

**Namjena:** Dodavanje autentifikovanog korisnika na listu čekanja za određenu radionicu ukoliko je radionica popunjena ili korisnik nije mogao ostvariti direktnu prijavu.

**Autentifikacija:** Potrebna

**Path parametri:** workshop_id

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK`| Uspješno dodavanje na listu čekanja | `{"message": "Uspješno ste dodani na listu čekanja.", "position": 3, "total_in_queue": 10}` |
| `400 Bad Request`  | Korisnik je već prijavljen na radionicu | `{"detail": "Već ste prijavljeni na ovu radionicu."}`                        |
| `400 Bad Request`  | Korisnik je već na listi čekanja        | `{"detail": "Već ste na listi čekanja."}`                                    |
| `401 Unauthorized` | Korisnik nije autentifikovan            | `{"detail": "Not authenticated"}`                                            |


## Endpoint 2 — Status liste čekanja za korisnika

**GET /workshops/waiting-list/status/{workshop_id}**

**Namjena:** Provjera da li je prijavljeni korisnik na listi čekanja za određenu radionicu i, ako jeste, prikaz njegove pozicije u redu.

**Autentifikacija:** Potrebna

**Path parametri:** workshop_id

**Mogući responses:**

| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK`| Korisnik je na listi čekanja   | `{"on_waiting_list": true, "position": 2}` |
| `200 OK`| Korisnik nije na listi čekanja | `{"on_waiting_list": false}`               |
| `401 Unauthorized`| Korisnik nije autentifikovan   | `{"detail": "Not authenticated"}`|

---

## Endpoint 3 — Moja lista čekanja

**GET /workshops/waiting-list/me**

**Namjena:** Dohvatanje svih radionica na kojima se trenutno prijavljeni korisnik nalazi na listi čekanja.

**Autentifikacija:** Potrebna

**Query parametri:** Nema


| Status | Slučaj | Primjer body-ja |
|---|---|---|
| `200 OK`| Uspješan prikaz liste čekanja korisnika  | `[{"workshop_id": 5}, {"workshop_id": 8}]`|
| `200 OK`| Korisnik nije ni na jednoj listi čekanja | `[]`|
| `401 Unauthorized`| Korisnik nije autentifikovan   | `{"detail": "Not authenticated"} |

---

## Endpoint 4 — Status promocije na radionici

**GET /workshops/my-promotion**

**Namjena:** Provjera statusa prijave korisnika i informacija da li je korisnik promovisan sa liste čekanja na radionicu.

**Autentifikacija:** Potrebna

**Query parametri:** Nema

| Status | Slučaj | Primjer body-ja |
|---|---|---|
|`200 OK`| Korisnik ima aktivnu prijavu | `{"promotion": {"user_id": 1, "workshop_id": 5, "workshop_title": "Uvod u Python", "status": "registered", "is_promoted": true}}` |
|`200 OK`| Korisnik nema prijavu        | `{"promotion": null}` |
|`401 Unauthorized` | Korisnik nije autentifikovan | `{"detail": "Not authenticated"}` |

---

## Endpoint 5 — Napuštanje liste čekanja

**DELETE /workshops/waiting-list/{workshop_id}**

**Namjena:** Uklanjanje prijavljenog korisnika sa liste čekanja za određenu radionicu.

**Autentifikacija:** Potrebna

**Path parametri:** workshop_id



| Status | Slučaj | Primjer body-ja |
| --- | ---| ---|
| `200 OK` | Uspješno uklanjanje sa liste čekanja | `{"message": "Uspješno ste napustili listu čekanja."}` |
| `404 Not Found`    | Korisnik nije na listi čekanja za datu radionicu | `{"detail": "Niste na listi čekanja za ovu radionicu."}` |
| `401 Unauthorized` | Korisnik nije autentifikovan | `{"detail": "Not authenticated"}` |

---