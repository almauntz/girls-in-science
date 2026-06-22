# Tim 2 — Mentoring: Frontend Dokumentacija

**Projekat:** Girls in Science Platform  
**Tim:** Tim 2 — Mentoring  
**Tehnologije:** Vue 3, Vite, Tailwind CSS, Axios, Vue Router

---

## Sadržaj

1. [Pregled modula](#1-pregled-modula)
2. [Postavljanje i pokretanje](#2-postavljanje-i-pokretanje)
3. [Struktura fajlova](#3-struktura-fajlova)
4. [Stranice i komponente](#4-stranice-i-komponente)
5. [Servisi — komunikacija sa backendom](#5-servisi--komunikacija-sa-backendom)
6. [Rute i navigacija](#6-rute-i-navigacija)
7. [Autentifikacija i role-based prikaz](#7-autentifikacija-i-role-based-prikaz)
8. [Česti problemi i rješenja](#8-česti-problemi-i-rješenja)

---

## 1. Pregled modula

Frontend mentoring modula pokriva:

- **Hero sekcija** na `/mentoring` — dva CTA dugmeta sa gradijentom i SVG grafikom
- **Lista mentorica** — responzivni grid sa filterom po oblasti ekspertize
- **Profil mentorice** — detaljan prikaz sa biografijom, iskustvom i dugmetom za zahtjev
- **Forma za prijavu mentorice** — multi-step forma sa CV uploadom *(implementirala kolegica)*
- **Forma za prijavu studentice** — 5-sekcijska forma usklađena sa Google formom
- **Panel mentorice** — pregled i obrada pristiglih zahtjeva *(implementirala kolegica)*
- **Admin panel** — odobravanje/odbijanje prijava mentorica i studentica, sa tabovima

---

## 2. Postavljanje i pokretanje

### Preduvjeti

- Node.js (preporučeno v18+)
- npm

### Koraci

```bash
# Iz root foldera projekta
cd frontend

# Instalacija zavisnosti
npm install

# Pokretanje dev servera
npm run dev
```

Aplikacija je dostupna na: `http://localhost:5173`

> **Napomena:** Backend mora biti pokrenut na `http://127.0.0.1:8000` jer frontend šalje API pozive direktno na tu adresu.

### Environment varijable

Trenutno nema `.env` fajla — API URL je hardkodovan u servisnom sloju (`src/services/mentoring.js`). Ako se backend pokrene na drugom portu, treba ažurirati `API_URL` u tom fajlu.

---

## 3. Struktura fajlova

Relevantni fajlovi za Tim 2 unutar `frontend/src/`:

```
src/
  components/
    MentorCard.vue           — Kartica mentorice (slika, ime, oblast, dugme)
  services/
    mentoring.js             — Svi API pozivi za mentoring modul
  views/
    mentoring/
      MentoringView.vue      — Glavna stranica (hero + filter + grid)
      MentorProfileView.vue  — Detaljan profil mentorice
      MentorRegistration.vue — Forma za prijavu mentorice (kolegica)
      StudentRegistration.vue — Forma za prijavu studentice
      MentorApplicationsView.vue — Admin panel za mentorice i studentice
      MentoringRequestView.vue — Slanje zahtjeva za mentorstvo (kolegica)
      MyApplicationsView.vue — Panel mentorice (kolegica)
  router/
    index.js                 — Definicija svih ruta
```

---

## 4. Stranice i komponente

### `MentoringView.vue` — `/mentoring`

Glavna stranica mentoring modula. Sadrži tri funkcionalne cjeline:

**1. Hero sekcija**
- Puna širina ekrana (izlazi van `max-width` containera iz `App.vue` koristeći `w-full` bez padding-a)
- Gradient pozadina (ljubičasta → roza)
- Prilagođena SVG grafika u sredini
- Lijevo dugme: "Postani Mentor" (vodi na `/mentoring/apply-mentor`)
- Desno dugme: "Prijavi se kao Studentica" (vodi na `/student/apply`)
- Dugmad su skrivena za korisnike sa ulogom `admin`

**2. Filter i grid**
- Dugmad za filter po oblasti ekspertize (klik na aktivni filter ga isključuje)
- Prikaz broja rezultata
- Responzivni grid: 1 kolona (mobile), 3 kolone (desktop)
- Loading spinner dok se dohvaćaju podaci
- Poruka "Trenutno nema dostupnih mentora" ako je lista prazna
- Poruka greške ako API poziv ne uspije

**3. Role-based preusmjeravanje**

U `onMounted` hook-u, **prije** učitavanja liste, dekodira se JWT token:
- Ako je uloga `mentor` → odmah preusmjerava na `/mentoring/my-applications`
- Ako je uloga `admin` → prikazuje se "Admin Panel" dugme umjesto hero dugmadi
- Za ostale uloge (`member`) → normalan prikaz

---

### `MentorCard.vue` — kartica mentorice

Prikazuje jednu mentoricu u gridu. Prima `mentor` objekat kao prop.

**Prikazuje:**
- Profilna slika iz `mentor.avatar_url` (fallback na `mentor.profile_img_url`, pa na `👤` ikonu)
- Ime i prezime (`mentor.full_name`)
- Bedž oblasti ekspertize (boja bedža se bira iz `BADGE_COLORS` mape prema oblasti)
- Dugme "Pogledaj profil" → vodi na `/mentoring/{mentor.id}`

**Props:**
```javascript
defineProps({
  mentor: { type: Object, required: true }
})
```

---

### `MentorProfileView.vue` — `/mentoring/:id`

Detaljan profil jedne mentorice. Dohvata podatke sa `GET /mentoring/mentors/{id}`.

**Prikazuje:**
- Profilna slika (`mentor.avatar_url`)
- Ime, oblast ekspertize (razdvojeno po zarezu u tagove)
- LinkedIn link
- Indikator popunjenosti kapaciteta (zeleni/crveni krug)
- Preferirani format sesija
- Biografija
- Timeline iskustva (pozicija, institucija, godine)
- Dugme "Zatraži mentorstvo" → vodi na `/mentoring/{id}/zahtjev`
  - Dugme je onemogućeno (`disabled`) ako je kapacitet popunjen
  - Dugme se zaključava sa porukom "Status: Na čekanju" ako je zahtjev već poslan

---

### `StudentRegistration.vue` — `/student/apply`

Forma za prijavu studentice na mentorski program. **Zahtijeva login** (`meta: { requiresAuth: true }`).

**Podijeljena u 5 sekcija:**
1. Lični podaci (ime, email, univerzitet, fakultet, godina studija, grad/država)
2. Akademski i profesionalni interesi (oblast, poslovna ideja)
3. Očekivanja od programa (slobodan tekst)
4. Dostupnost i obaveze (format sesija, commitment)
5. Saglasnosti (GDPR, evaluacija)

**Ponašanje:**
- HTML `required` atributi sprečavaju slanje neispunjene forme
- Nakon uspješnog slanja → poruka potvrde + reset forme
- Na grešku → prikazuje se poruka sa `err.response?.data?.detail`
- Forma pakuje podatke u `FormData` i šalje na `POST /mentoring/students/register`

---

### `MentorApplicationsView.vue` — `/admin/mentor-applications`

Admin panel za upravljanje prijavama. **Zahtijeva login + admin ulogu.**

**Struktura:**

Dva glavna taba:
- **Mentorice** — prijave mentorica za program
- **Studentice** — prijave studentica za mentorski program

Pod-tabovi za svaki tab:
- Na čekanju | Prihvaćene | Odbijene | Obrisane

**Akcije za mentorice:**
- ✓ Odobri | ✕ Odbij (za PENDING)
- 🔍 Pregledaj → vodi na `/admin/mentor-applications/{id}`
- Obriši (za APPROVED/REJECTED)
- Vrati (za DELETED)

**Akcije za studentice:**
- ✓ Odobri | ✕ Odbij (za PENDING)
- 🔍 Pregledaj → otvara modal sa svim detaljima prijave
- Obriši (za ostale statuse)
- Vrati (za DELETED)

**Detail modal za studentice** prikazuje sva polja prijave: ime, email, fakultet, godina studija, interesovanja, očekivanja, motivacijska poruka, vještine, format sesije, commitment.

---

## 5. Servisi — komunikacija sa backendom

**Fajl:** `src/services/mentoring.js`

| Funkcija | HTTP metoda | Endpoint | Auth | Opis |
|---|---|---|---|---|
| `getMentors(skip, limit)` | GET | `/mentoring/mentors` | Ne | Lista odobrenih mentorica |
| `applyAsMentor(formData)` | POST | `/mentoring/apply` | Ne | Prijava mentorice |
| `getMentorById(id)` | GET | `/mentoring/mentors/{id}` | Ne | Profil jedne mentorice |
| `registerStudent(formData)` | POST | `/mentoring/students/register` | Da | Prijava studentice |

**Primjer poziva sa autentifikacijom:**
```javascript
export const registerStudent = (formData) => {
  const token = localStorage.getItem('token')
  return axios.post(`${API_URL}/students/register`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
}
```

> **Napomena:** `Content-Type` header se ne postavlja ručno za `FormData` — `axios` ga automatski postavlja na `multipart/form-data` sa ispravnim `boundary`.

---

## 6. Rute i navigacija

Definirane u `src/router/index.js`:

| Putanja | Komponenta | Auth | Opis |
|---|---|---|---|
| `/mentoring` | `MentoringView.vue` | Ne | Javna lista; redirect za mentoricu |
| `/mentoring/:id` | `MentorProfileView.vue` | Ne | Profil mentorice |
| `/mentoring/:id/zahtjev` | `MentoringRequestView.vue` | Da | Slanje zahtjeva za mentorstvo |
| `/mentoring/my-applications` | `MyApplicationsView.vue` | Da | Panel mentorice |
| `/mentoring/apply-mentor` | `MentorRegistration.vue` | Ne | Prijava mentorice |
| `/student/apply` | `StudentRegistration.vue` | Da | Prijava studentice |
| `/admin/mentor-applications` | `MentorApplicationsView.vue` | Da | Admin panel |
| `/admin/mentor-applications/:id` | `MentorApplicationDetailView.vue` | Da | Detalji prijave mentorice |

**Router guard** u `index.js`:
- Rute sa `meta: { requiresAuth: true }` → preusmjerava na `/login` ako nema tokena
- Rute sa `meta: { guestOnly: true }` → preusmjerava na `/` ako je korisnik prijavljen

---

## 7. Autentifikacija i role-based prikaz

JWT token se čuva u `localStorage` pod ključem `'token'` nakon prijave.

**Dekodiranje tokena za čitanje uloge:**
```javascript
const token = localStorage.getItem('token')
const payload = JSON.parse(atob(token.split('.')[1]))
const role = payload.role // 'member', 'mentor', 'admin'
```

**Koristi se za:**

| Situacija | Ponašanje |
|---|---|
| `role === 'admin'` | Prikazuje se "Admin Panel" dugme; hero dugmad skrivena |
| `role === 'mentor'` | Preusmjeravanje na `/mentoring/my-applications` |
| `role === 'member'` | Normalan prikaz (hero, lista, forma za studenticu) |
| Nije prijavljen | Lista mentorica vidljiva, ali forma za studenticu zahtijeva login |

---

## 8. Česti problemi i rješenja

### `axios` nije instaliran

```bash
npm install axios
```

### `Failed to resolve import "../../services/mentoring.js"`

Fajl `src/services/mentoring.js` ne postoji. Kreiraj ga prema sekciji 5 ove dokumentacije.

### `Failed to resolve import ".../MentorProfileView.vue"`

Komponenta referencirana u routeru ne postoji. Provjeri da li je fajl kreiran na ispravnoj putanji.

### Mentoring stranica se ne učitava (bijeli ekran)

Najvjerovatnije syntax greška u nekom Vue fajlu. Provjeri Vite terminal output — greška će pokazati tačan fajl i liniju.

### Forma za studenticu vraća 401

Korisnik nije prijavljen ili token je istekao. Provjeri `localStorage.getItem('token')` u browser konzoli.

### Profilna slika mentorice se ne prikazuje

`avatar_url` je `null` ako:
- Mentorica nema korisnički nalog na platformi sa istim emailom, **ili**
- Korisnica nije uploadovala profilnu sliku (Tim 4 funkcionalnost)

U tom slučaju prikazuje se fallback `👤` ikona — ovo je očekivano ponašanje.

### Mentoring stranica prikazuje samo hero, bez liste

Backend nije pokrenut. Provjeri da li `uvicorn` radi na `http://127.0.0.1:8000`.
