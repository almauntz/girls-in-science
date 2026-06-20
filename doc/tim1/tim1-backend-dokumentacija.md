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
| `200 OK` | Uspješna odjava | `{"message": "Uspješno ste odustali od radionice."}` |
| `404 Not Found` | Prijava ne postoji za tog korisnika/radionicu | `{"detail": "Nije pronađena vaša prijava za ovu radionicu."}` |

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






//mahir