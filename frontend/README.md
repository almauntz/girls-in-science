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

#### Servisi (`services/mentoring.js`)
 
| Funkcija | Endpoint | Opis |
|---|---|---|
| `getMentors(skip, limit)` | `GET /mentoring/mentors` | Dohvata listu odobrenih mentorica |
| `getMentorById(id)` | `GET /mentoring/mentors/{id}` | Dohvata detaljan profil jedne mentorice |
| `registerStudent(formData)` | `POST /mentoring/students/register` | Šalje prijavu studentice (zahtijeva JWT token u headeru) |
| `applyAsMentor(formData)` | `POST /mentoring/apply` | Šalje prijavu mentorice sa priloženim CV-jem |
| `getMentorApplications()` | `GET /mentoring/my-applications` | Dohvata sve pristigle zahtjeve studentica za prijavljenu mentoricu (zahtijeva JWT token) |
| `updateApplicationStatus(applicationId, status, rejectionReason)` | `PUT /mentoring/applications/{id}/status` | Mijenja status zahtjeva u ACCEPTED ili REJECTED uz opcioni razlog (zahtijeva JWT token) |

#### Rute (`router/index.js`)
 
| Putanja | Komponenta | Pristup |
|---|---|---|
| `/mentoring` | MentoringView.vue | Javno (lista mentorica), automatski redirect za mentorice |
| `/mentoring/:id` | MentorProfileView.vue | Javno (profil mentorice) |
| `/mentoring/:id/zahtjev` | MentorshipRequestView.vue | Zahtijeva login |
| `/mentoring/my-applications` | MentorApplicationsView.vue | Zahtijeva login | 
`/mentoring/apply` | MentorRegistration.vue | Javno | 

#### Komunikacija sa backendom
 
Autentifikacija preko JWT tokena spremljenog u `localStorage`. Token se dekodira na frontendu (`JSON.parse(atob(token.split('.')[1]))`) radi čitanja `role` polja za uslovni prikaz (npr. admin dugme, redirect mentorice).
 
---