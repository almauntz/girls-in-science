# Girls in Science — Frontend Dokumentacija

## 1. Pregled aplikacije

Frontend pokriva sljedeće module:

- Lični i javni profil korisnice (pregled, uređivanje, slika profila)
- Dashboard sa pregledom i prijavom na radionice
- Mentorski dashboard (pregled zahtjeva, prihvatanje/odbijanje polaznica)

---

## 2. Struktura projekta

```
frontend/
└── src/
    ├── views/
    │   ├── LoginView.vue
    │   └── profiles/
    │       ├── ProfilesView.vue         (wrapper komponenta — renderuje ProfileForm, DashboardTab, ActivityHistory ili AdminView ovisno o aktivnom tabu)
    │       ├── PublicProfileView.vue    (javni profil druge korisnice)
    │       └── AdminView.vue            (admin panel)
    ├── components/
    │   ├── SideBar.vue          (ProfileSidebar — bočna navigacija)
    │   ├── ProfileForm.vue      (forma za uređivanje profila, lozinke, avatara)
    │   ├── DashboardTab.vue     (prikaz i prijava na radionice)
    │   └── ActivityHistory.vue
    ├── services/
    │   └── api.js               (centralizovani API pozivi)
    └── router/
        └── index.js             (definicije ruta)
```

Pristup uređivanju profila organiziran je kroz roditeljsko-dijete (parent-child) komunikaciju: `ProfilesView.vue` učitava podatke i prosljeđuje ih kao props u `ProfileForm.vue` i `ProfileSidebar.vue`, dok se promjene vraćaju nazad putem emitovanih događaja (npr. `profile-updated`, `avatar-uploaded`, `avatar-deleted`, `tab-change`).

---

## 3. Pregled implementiranih funkcionalnosti

### 3.1 Upravljanje nalogom

- Detekcija deaktiviranog naloga prilikom prijave (`isDeactivated` stanje na `LoginView`).
- Reaktivacija naloga — korisnica unosi email i lozinku, backend ponovo aktivira nalog i odmah se izvrši prijava.
- Deaktivacija naloga iz profila, uz modalnu potvrdu (`showDeactivateModal`), nakon čega se token briše i korisnica se preusmjerava na prijavu.
- Promjena lozinke (`staraNovaPotvrda`) sa validacijom (minimalno 8 karaktera, poklapanje nove i potvrđene lozinke).

### 3.2 Lični profil (`ProfilesView` + `ProfileForm`)

- Prikaz i uređivanje osnovnih podataka: ime i prezime, oblast (polje iz unaprijed definisane liste struka), biografija (do 500 karaktera), lokacija, email.
- Validacija forme prije slanja: obavezno ime, dužina biografije, format email adrese.
- Upravljanje vidljivošću podataka na javnom profilu (`show_biography`, `show_field`, `show_location`).
- Strukturirani podaci profila u obliku nizova: jezici (`languages`), radno iskustvo (`experience`), obrazovanje (`education`) i vještine (`skills`).
- Društvene mreže / linkovi: LinkedIn, GitHub, Twitter.
- Upload profilne slike (JPG/PNG, maksimalno 2MB) sa validacijom na frontendu prije slanja na backend, te brisanje profilne slike uz potvrdu.

### 3.3 Javni profil (`PublicProfileView`)

- Prikaz javnog profila druge korisnice na osnovu `user_id` iz rute, uz poštovanje polja vidljivosti koje je postavila vlasnica profila.
- Administratorski nalozi se ne prikazuju kroz javni profil (preusmjeravanje, odnosno poruka da profil nije dostupan).

---

## 4. Pregled ruta i navigacije

| Putanja              | Naziv rute       | Opis / komponenta                                                                                           |
| -------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------- |
| `/profiles`          | `profiles`       | `ProfilesView.vue` — glavni ekran nakon prijave (profil, dashboard, mentorstvo). Zahtijeva autentifikaciju. |
| `/profiles/:user_id` | `public-profile` | `PublicProfileView.vue` — javni profil korisnice po ID-u.                                                   |

Navigacija unutar `ProfilesView.vue` ostvarena je putem internog stanja `activeTab` (npr. `'dashboard'`, `'info'`, itd.), a ne kroz odvojene rute — `ProfileSidebar` emituje događaj `tab-change` koji mijenja aktivni prikaz bez ponovnog učitavanja stranice.

---

## 5. Komunikacija sa backendom

Backend je razvijen u FastAPI + SQLModel (SQLite baza). Komunikacija sa frontenda ide na osnovnu adresu `http://localhost:8000`, kombinovano kroz `axios` (servisni sloj i dio dashboard logike) i nativni `fetch` (profil, avatar, lozinka, deaktivacija).

### 5.1 Autentifikacija

- Token se dobija prilikom prijave (POST na login endpoint) i čuva se u `localStorage` pod ključem `token`.
- Svi autentifikovani pozivi šalju zaglavlje `Authorization: Bearer <token>` — u `ProfilesView.vue` ovo je centralizovano kroz pomoćnu metodu `getAuthHeaders()`.
- Uz token, u `localStorage` se čuvaju i `username` i `user_role` radi brže provjere uloge bez dodatnog poziva backendu (npr. `PublicProfileView` preusmjerava admina bez čekanja na odgovor servera).

### 5.2 Pregled glavnih endpointa

| Metoda      | Endpoint                             | Svrha                                                                  |
| ----------- | ------------------------------------ | ---------------------------------------------------------------------- |
| `POST`      | `/profiles/reactivate`               | Reaktivacija deaktiviranog naloga                                      |
| `GET`       | `/profiles/me`                       | Dohvat podataka prijavljene korisnice (`getMyProfile`)                 |
| `PUT/PATCH` | `/profiles/me`                       | Ažuriranje profila (`updateProfile`)                                   |
| `GET`       | `/profiles/:user_id`                 | Dohvat javnog profila druge korisnice                                  |
| `POST`      | `/profiles/me/avatar`                | Upload profilne slike (`multipart/form-data`)                          |
| `DELETE`    | `/profiles/me/avatar`                | Brisanje profilne slike                                                |
| `PATCH`     | `/profiles/me/change-password`       | Promjena lozinke                                                       |
| `PATCH`     | `/profiles/me/deactivate`            | Deaktivacija naloga                                                    |
| `GET`       | `/profiles/dashboard`                | Podaci za dashboard (moje, nove i dostupne radionice)                  |
| `POST`      | `/profiles/dashboard/register`       | Prijava na radionicu (query parametar `workshop_id`)                   |
| `GET`       | `/mentoring/my-applications`         | Dohvat svih mentorskih zahtjeva (filtrirano na `ACCEPTED` / `PENDING`) |
| `PUT`       | `/mentoring/applications/:id/status` | Promjena statusa zahtjeva (`ACCEPTED` / `REJECTED`)                    |

### 5.3 Statički fajlovi

Avatari i ostali otpremljeni fajlovi posluženi su preko FastAPI `StaticFiles` montiranog na rutu `/static`, a frontend ih prikazuje kroz puni URL oblika:

```
http://localhost:8000<putanja_iz_baze>
```
