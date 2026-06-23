# Girls in Science — Frontend

Izgrađeno sa Vue 3, Vite i Tailwind CSS.

## Postavljanje projekta

1. Instaliraj zavisnosti:
```bash
cd frontend
npm install
```

2. Pokreni dev server:
```bash
npm run dev
```

3. Otvori u browseru:
```
http://localhost:5173
```

## Struktura projekta

```
src/
  components/
    NavBar.vue          — navigacija (ne mijenjati)
    FooterBar.vue       — footer (ne mijenjati)
  views/
    HomeView.vue        — početna stranica
    LoginView.vue       — forma za prijavu
    RegisterView.vue    — forma za registraciju
    workshops/          — Tim 1
    mentoring/          — Tim 2
    rolemodels/         — Tim 3
    news/               - Tim 3
    profiles/           — Tim 4
  router/
    index.js            — rute aplikacije
  services/
    api.js              — komunikacija sa backendom
```

## Autentifikacija

Token se čuva u `localStorage` nakon prijave.
Svaki API poziv koji zahtijeva auth šalje token u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Za projektne timove

1. Vaš folder je već kreiran u `src/views/`
2. Kreirajte svoje komponente u `src/components/`
3. Dodajte svoje rute u `src/router/index.js`
4. Za API pozive koristite `src/services/api.js` kao primjer
5. Sve stranice vaše funkcionalnosti trebaju `meta: { requiresAuth: true }`

## Boje

```
Primary:   #7c3aed  (ljubičasta)
Secondary: #a78bfa  (svjetlija ljubičasta)
```

Koristite Tailwind klase `text-primary`, `bg-primary` za konzistentan dizajn.


# Girls in Science — Frontend

Izgrađeno sa Vue 3, Vite i Tailwind CSS.

## Postavljanje projekta

1. Instaliraj zavisnosti:
```bash
cd frontend
npm install
```

2. Pokreni dev server:
```bash
npm run dev
```

3. Otvori u browseru:
```
http://localhost:5173
```

## Struktura projekta

```
src/
  components/
    NavBar.vue          — navigacija (ne mijenjati)
    FooterBar.vue       — footer (ne mijenjati)
  views/
    HomeView.vue        — početna stranica
    LoginView.vue       — forma za prijavu
    RegisterView.vue    — forma za registraciju
    workshops/          — Tim 1
    mentoring/          — Tim 2
    rolemodels/         — Tim 3
    news/               - Tim 3
    profiles/           — Tim 4
  router/
    index.js            — rute aplikacije
  services/
    api.js              — komunikacija sa backendom
```

## Autentifikacija

Token se čuva u `localStorage` nakon prijave.
Svaki API poziv koji zahtijeva auth šalje token u headeru:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Za projektne timove

1. Vaš folder je već kreiran u `src/views/`
2. Kreirajte svoje komponente u `src/components/`
3. Dodajte svoje rute u `src/router/index.js`
4. Za API pozive koristite `src/services/api.js` kao primjer
5. Sve stranice vaše funkcionalnosti trebaju `meta: { requiresAuth: true }`

## Boje

```
Primary:   #7c3aed  (ljubičasta)
Secondary: #a78bfa  (svjetlija ljubičasta)
```

Koristite Tailwind klase `text-primary`, `bg-primary` za konzistentan dizajn.



---
### Mentoring
--- 
 
#### Komponente i stranice
 
**`views/mentoring/MentoringView.vue`**
Glavna stranica mentoring modula. Sadrži:
- Hero sekciju (puna širina ekrana, gradient pozadina, SVG grafika, dugmad "Postani Mentor" / "Prijavi se kao Studentica")
- Responzivni grid kartica mentorica (1 kolona mobile, 3 desktop)
- Loading i empty state
- Automatsko preusmjeravanje: ako je ulogovani korisnik mentorica (role iz JWT tokena), stranica je odmah preusmjerava na `/mentoring/my-applications` umjesto da prikaže javnu listu
**`components/MentorCard.vue`**
Kartica pojedinačne mentorice — slika (`avatar_url` sa fallback na `profile_img_url`), ime, bedž oblasti ekspertize (boja zavisi od oblasti), dugme "Pogledaj profil".
 
**`views/mentoring/StudentRegistration.vue`**
Forma za prijavu studentice na mentorski program, podijeljena u 5 sekcija (lični podaci, akademski interesi, očekivanja, dostupnost, saglasnosti), usklađena sa wireframeom i originalnom Google formom profesorice. Klijentska validacija obaveznih polja, prikaz statusa slanja (uspjeh/greška), reset forme nakon uspješnog slanja.

**`views/mentoring/MentorProfileView.vue`**
Detaljan profil mentorice na ruti `/mentoring/:id`. Prikazuje profilnu sliku, ime, oblast ekspertize, LinkedIn link, indikator popunjenosti kapaciteta, preferirani format sesija, biografiju i timeline iskustva. Dugme "Zatraži mentorstvo" vodi na `/mentoring/{id}/zahtjev` i deaktivira se ako je kapacitet popunjen ili je zahtjev već poslan.

**`views/mentoring/MentorshipRequestView.vue`**
Forma za slanje zahtjeva za mentorstvo na ruti `/mentoring/:id/zahtjev`. Dohvata osnovne podatke o mentorici, omogućava unos očekivanja i vještina koje studentica želi unaprijediti, upload CV-a i potvrdu saglasnosti za sesije. Prilikom slanja koristi JWT autentifikaciju i `multipart/form-data`.
 
**`views/mentoring/MentorRegistration.vue`**
Javna forma za prijavu mentorica na ruti `/mentoring/apply`. Omogućava unos ličnih podataka, odabir STEM oblasti, unos godina iskustva, biografije i LinkedIn URL-a, uz Drag & Drop zonu za upload CV-ja (PDF/DOCX do 5MB). Koristi reaktivnu validaciju u realnom vremenu i šalje podatke kao `multipart/form-data` bez potrebe za autentifikacijom.

**`views/mentoring/MyApplicationsView.vue`**
Panel za mentorice na ruti `/mentoring/my-applications` koji omogućava upravljanje zahtjevima studentica kroz tri tabova (`PENDING`, `ACCEPTED`, `REJECTED`). Prikazuje kartice sa osnovnim podacima i relativnim vremenom, nudi detaljan modalni pregled profila studentice sa opcijom preuzimanja CV-ja, te modal za odbijanje zahtjeva uz unos obrazloženja.

**`views/admin/MentorApplicationsView.vue`**
Admin panel za upravljanje prijavama mentorica na ruti `/admin/mentor-applications`. Prikazuje prijave u tabovima po statusu (Na čekanju, Prihvaćene, Odbijene, Obrisane) sa brojem prijava u svakom tabu. Svaki red sadrži dugme "Pregledaj" za otvaranje detalja, te akcijska dugmad ✓ / ✗ za direktno odobravanje/odbijanje iz tabele. Pristup ograničen na ulogu `admin`.

**`views/admin/MentorApplicationDetailView.vue`**
Detaljan pregled jedne prijave mentorice na ruti `/admin/mentor-applications/:id`. Prikazuje sve podatke iz prijave, dugme "Preuzmi CV" sa direktnim linkom na backend, textarea za unos razloga odbijanja (vidljiva samo za prijave na čekanju), prikaz razloga odbijanja ako postoji, te dugme "Pošalji ponovo na pregled" za odbijene prijave. Pristup ograničen na ulogu `admin`.

#### Servisi (`services/mentoring.js`)
 
| Funkcija | Endpoint | Opis |
|---|---|---|
| `getMentors(skip, limit)` | `GET /mentoring/mentors` | Dohvata listu odobrenih mentorica |
| `getMentorById(id)` | `GET /mentoring/mentors/{id}` | Dohvata detaljan profil jedne mentorice |
| `registerStudent(formData)` | `POST /mentoring/students/register` | Šalje prijavu studentice (zahtijeva JWT token u headeru) |
| `applyAsMentor(formData)` | `POST /mentoring/apply` | Šalje prijavu mentorice sa priloženim CV-jem |
| `getMentorApplications()` | `GET /mentoring/my-applications` | Dohvata sve pristigle zahtjeve studentica za prijavljenu mentoricu (zahtijeva JWT token) |
| `updateApplicationStatus(applicationId, status, rejectionReason)` | `PUT /mentoring/applications/{id}/status` | Mijenja status zahtjeva u ACCEPTED ili REJECTED uz opcioni razlog (zahtijeva JWT token) |
| `getMentorApplications()` (admin verzija u `admin.js` ili direktno fetch) | `GET /api/v1/admin/mentor-applications` | Dohvata sve prijave mentorica za admin panel |
| — | `PATCH /api/v1/admin/mentor-applications/{id}/approve` | Odobrava prijavu, mijenja role korisnika u `mentor` |
| — | `PATCH /api/v1/admin/mentor-applications/{id}/reject` | Odbija prijavu uz razlog, mijenja role korisnika u `member` |
| — | `PATCH /api/v1/admin/mentor-applications/{id}/resubmit` | Vraća odbijenu prijavu u status `PENDING` |
| — | `DELETE /api/v1/admin/mentor-applications/{id}` | Soft delete prijave |
| — | `GET /mentoring/cv/{filename}` | Preuzimanje CV fajla mentorice |

#### Rute (`router/index.js`)
 
| Putanja | Komponenta | Pristup |
|---|---|---|
| `/mentoring` | MentoringView.vue | Javno (lista mentorica), automatski redirect za mentorice |
| `/mentoring/:id` | MentorProfileView.vue | Javno (profil mentorice) |
| `/mentoring/:id/zahtjev` | MentorshipRequestView.vue | Zahtijeva login |
| `/mentoring/my-applications` | MentorApplicationsView.vue | Zahtijeva login | 
`/mentoring/apply` | MentorRegistration.vue | Javno | 
| `/admin/mentor-applications` | MentorApplicationsView.vue | Zahtijeva ulogu `admin` |
| `/admin/mentor-applications/:id` | MentorApplicationDetailView.vue | Zahtijeva ulogu `admin` |
#### Komunikacija sa backendom
 
Autentifikacija preko JWT tokena spremljenog u `localStorage`. Token se dekodira na frontendu (`JSON.parse(atob(token.split('.')[1]))`) radi čitanja `role` polja za uslovni prikaz (npr. admin dugme, redirect mentorice).
 
---