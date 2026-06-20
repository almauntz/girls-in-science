//amel


//elma
# Frontend dokumentacija — Prijava na radionice, Kalendar, Notifikacije

Dokumentacija obuhvata komponente: `RegistrationForm.vue`, `Calendar.vue`, `Notifications.vue`, te dio `WorkshopDetail.vue` vezan za otvaranje forme za prijavu.

---

## 1. RegistrationForm.vue

### Svrha
Forma za prijavu korisnika na radionicu. Prikazuje se kao forma preko `WorkshopDetail.vue` stranice.

### Props / Emits
- **Emits:**
  - `cancel` — emituje se klikom na dugme "Odustani" (zatvara modal, ne poziva backend)
  - `success` — emituje se nakon uspješne prijave (parent zatvara modal i refetch-uje podatke o radionici)

### Polja forme

| Polje | Tip | Obavezno | Validacija (frontend) |
|---|---|---|---|
| Ime | text | ✅ | ne smije biti prazno |
| Prezime | text | ✅ | ne smije biti prazno |
| Email | email | ✅ | ne smije biti prazno |
| Telefon | tel | ✅ | regex `^\d{9,}$` — minimalno 9 cifara |
| GitHub profil | text | opciono | nema validaciju |
| Prethodno iskustvo | textarea | opciono | nema validaciju |

Polja Ime, Prezime, Email i Telefon se **automatski popunjavaju** pri otvaranju forme (`fillUserData()`), pozivom `getMe(token)`, na osnovu podataka ulogovanog korisnika.

### Validacija prije slanja

| Provjera | Poruka korisniku |
|---|---|
| Nema tokena u `localStorage` | "Morate se prijaviti na nalog da biste izvršili prijavu na radionicu." |
| Neko obavezno polje je prazno | "Popunite obavezna polja." |
| Telefon ne prolazi regex `^\d{9,}$` | "Broj telefona mora imati najmanje 9 cifara." |

### API pozivi
- `registerForWorkshop(formData.value)` → `POST /workshops/registration`
- `getMe(token)` → dohvat podataka ulogovanog korisnika (za auto-popunjavanje)

### Obrada odgovora backend-a

**Uspješna prijava (201):**
```js
await Swal.fire({
  title: 'Uspješno! 🎉',
  text: 'Prijavljeni ste na radionicu.',
  icon: 'success'
})
emit('success')
```
- Prikazuje se confetti animacija (`triggerConfetti()`)


**Neuspješna prijava (400 / 404):**
```js
const message =
  err?.response?.data?.detail ||
  err?.data?.detail ||
  err?.detail ||
  'Došlo je do greške.'

Swal.fire('Greška', message, 'error')
```
- `detail` poruka iz backend-a se **direktno prikazuje korisniku, bez izmjene**.

| Backend status | Backend `detail` | Šta korisnik vidi |
|---|---|---|
| `404` | "Radionica nije pronađena" | Swal "Greška" / "Radionica nije pronađena" |
| `400` | "Nažalost, sva mjesta su popunjena!" | Swal "Greška" / "Nažalost, sva mjesta su popunjena!" |
| `400` | "Ovaj email već je registrovan!" | Swal "Greška" / "Ovaj email već je registrovan!" |
| `400` | "Već ste prijavljeni (user)!" | Swal "Greška" / "Već ste prijavljeni (user)!" |

### Dugme "Odustani"
```html
<button type="button" @click="$emit('cancel')">Odustani</button>
```
Samo zatvara formu (`showForm.value = false` u parent komponenti). — nije vezano za odjavu, već za odustajanje od popunjavanja forme.

---

## 2. WorkshopDetail.vue — dio vezan za prijavu

### Otvaranje forme za prijavu

```js
const handleRegistrationClick = () => {
  if (wasRegistered.value) return

  const token = localStorage.getItem('token')
  if (!token) {
    Swal.fire({
      title: 'Niste prijavljeni!',
      text: 'Morate biti prijavljeni na svoj nalog da biste rezervisali mjesto na radionici.',
      icon: 'info',
      showCancelButton: true,
      confirmButtonText: 'Prijavi se odmah',
      cancelButtonText: 'Odustani'
    }).then((result) => {
      if (result.isConfirmed) router.push('/login')
    })
  } else {
    showForm.value = true
  }
}
```

**Logika klika na dugme "🎟 Prijavi se":**

| Stanje | Šta se desi |
|---|---|
| Korisnik je već prijavljen (`wasRegistered === true`) | Klik ne radi ništa (dugme je i vizuelno `disabled`) |
| Korisnik nema token (nije ulogovan) | Swal popup s pitanjem — "Prijavi se odmah" → redirect na `/login`, "Odustani" → zatvara popup |
| Korisnik ima token | Otvara modal sa `<WorkshopRegistrationForm>` |

### Provjera statusa prijave (pri učitavanju stranice)

```js
const regRes = await fetch(`${BASE_URL}/workshops/registration/check/${route.params.id}`, {
  headers: { Authorization: `Bearer ${token}` }
})
const regData = await regRes.json()
wasRegistered.value = regData.registered
```

Poziva `GET /workshops/registration/check/{workshop_id}` i postavlja `wasRegistered` na osnovu polja `registered` (`true`/`false`).

### Vizuelni prikaz dugmeta za prijavu

```html
<button :disabled="wasRegistered">
  {{ wasRegistered ? '✓ Prijavljeni' : '🎟 Prijavi se' }}
</button>
```

| `wasRegistered` | Tekst dugmeta | Klikabilno |
|---|---|---|
| `true` | "✓ Prijavljeni" | ❌ disabled |
| `false` | "🎟 Prijavi se" | ✅ |

### Nakon uspješne prijave

```js
const handleSuccess = () => {
  showForm.value = false      // zatvori modal
  wasRegistered.value = true   // dugme odmah postaje "Prijavljeni"
  fetchWorkshop()              // refetch radionice (ažurira free_spots, itd.)
}
```

### Odjava sa radionice — dugme "✕ Odustani"

Ovo nije isto dugme "Odustani" iz `RegistrationForm.vue` (ono samo zatvara formu i ostaje nepromijenjeno). Ovo je novo dugme koje se prikazuje **kad je korisnik već prijavljen** i poziva backend da ga odjavi.


#### Tok korisničke akcije 

1. Korisnik je prijavljen na radionicu → vidi dugme **"✕ Odustani"**
2. Klik → SweetAlert2 popup: *"Da li ste sigurni?"* sa opcijama "Da, odustani" / "Ne, ostani prijavljen"
3. Ako klikne "Ne" → popup se zatvara, ništa se ne mijenja
4. Ako klikne "Da" → poziva se `DELETE /workshops/cancellation/{workshop_id}`
5. **Uspjeh** → popup "Odjavljeni ste", dugme se vraća na "🎟 Prijavi se", podaci o radionici se refetch-uju (ažurira `free_spots`)
6. **Greška** → popup "Greška" sa porukom iz backend-a (`err.detail`)

## 3. Calendar.vue

### Svrha
Mjesečni kalendarski prikaz svih radionica sa vizuelnim statusima, pretragom i upozorenjima.

### Props

| Prop | Tip | Default | Opis |
|---|---|---|---|
| `workshops` | Array | `[]` | Lista svih radionica |
| `registrations` | Object | `{}` | Mapa `{ [workshop_id]: true/false }` — da li je korisnik prijavljen |

Komponenta **ne poziva API direktno** — sve podatke prima kroz props od parent komponente.

### Navigacija
- Promjena mjeseca: `←` / `→` dugmad (`updateMonth(-1/1)`)
- Promjena godine: `«` / `»` dugmad (`updateYear(-1/1)`)
- Dugme "Danas" — vraća prikaz na trenutni mjesec/godinu

### Pretraga
`searchQuery` (v-model na input polju) — filtrira radionice po `title` i `location` (case-insensitive `includes()`), unutar trenutno prikazanog mjeseca.

### Vizuelno bojenje radionica (`getFinalStyle()`)

| Stanje radionice | Boja | Uslov |
|---|---|---|
| Istekla (datum u prošlosti) | Sivo (`#f3f4f6`) | `workshop.date < danas` |
| Korisnik prijavljen | Ljubičasto (`#7c3aed`) | `checkIsRegistered(id) === true` |
| Popunjeno | Crveno (`#fee2e2`) | `free_spots <= 0` |
| Slobodno | Zeleno (`#dcfce7`) | `free_spots > 0` i nije prijavljen |

### Klik na radionicu (`handleWorkshopClick`)

```js
const handleWorkshopClick = (workshop) => {
  const isExpired = new Date(workshop.date) < new Date(new Date().setHours(0, 0, 0, 0))
  if (isExpired) {
    showExpiredModal.value = true
  } else {
    router.push(`/workshops/${workshop.ID_workshop}`)
  }
}
```

| Stanje | Akcija |
|---|---|
| Radionica istekla | Prikazuje modal "Radionica je istekla 😔" |
| Radionica aktivna | Redirect na `/workshops/{id}` (otvara `WorkshopDetail.vue`) |

### Banner upozorenja (`upcomingWarnings`)
Prikazuje upozorenje za radionice na koje je korisnik prijavljen, a počinju u narednih **0–3 dana**:

> ⚠️ Podsjetnik: Radionica počinje **za X dan(a)!** / **danas!** — *naziv radionice*, 📍 lokacija

### Statistika (header)
- `stats.registeredCount` — broj radionica na koje je korisnik prijavljen (računa se iz `registrations` props-a)

### Legenda boja (footer kalendara)
🟢 Slobodno · 🔴 Popunjeno · 🟣 Prijava · ⚪ Isteklo · ✨ Danas

---

## 4. Notifications.vue

### Svrha
Pozadinska komponenta (bez vizuelnog UI-a) koja periodično provjerava nove notifikacije i prikazuje ih kao toast obavještenja.

### Ponašanje
- Komponenta je vizuelno sakrivena (`display: none`)
- Pri `mounted()`: odmah pozove `checkNotifications()`, zatim postavlja **polling svakih 10 sekundi** (`setInterval`)
- Pri `beforeUnmount()`: čisti interval (`clearInterval`) — sprečava memory leak

### API poziv
```js
GET /workshops/unread-notifications
Headers: Authorization: Bearer {token}
```

| Slučaj | Ponašanje |
|---|---|
| Nema tokena | Funkcija se prekida (`return`), ne radi ništa, bez greške korisniku |
| Response nije `ok` | `console.error` u konzoli, korisnik ne vidi ništa |
| Response sadrži notifikacije | Za svaku se prikazuje toast |

### Prikaz toast notifikacije (SweetAlert2)

```js
Swal.fire({
  title: notif.title,
  html: `<p>${notif.body}</p>`,
  icon: 'info',
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 5000,
  timerProgressBar: true,
  background: '#7c3aed',
  color: '#ffffff'
})
```

| Svojstvo | Vrijednost |
|---|---|
| Pozicija | gornji desni ugao ekrana |
| Trajanje | 5 sekundi, auto-zatvaranje, sa progress bar-om |
| Boja | ljubičasta pozadina, bijeli tekst |
| Sadržaj | `notif.title` (naslov) i `notif.body` (tekst) — direktno iz backend response-a |

### Veza sa backendom
Backend endpoint (`GET /unread-notifications`) markira notifikacije kao pročitane (`is_read = True`) **odmah nakon** što ih vrati — zato se svaka notifikacija prikaže korisniku samo jednom (osim ako se desi race condition sa refresh-om stranice).

---

## Sažetak — koje su komponente urađene,

| Funkcionalnost | Komponenta | Status |
|---|---|---|
| Prikaz forme za prijavu | `RegistrationForm.vue` | ✅ Gotovo |
| Validacija forme (frontend) | `RegistrationForm.vue` | ✅ Gotovo |
| Prikaz greške/uspjeha prijave | `RegistrationForm.vue` | ✅ Gotovo  |
| Otvaranje forme sa detalja radionice | `WorkshopDetail.vue` | ✅ Gotovo |
| Provjera da li je korisnik već prijavljen | `WorkshopDetail.vue` | ✅ Gotovo |
| Kalendarski prikaz radionica | `Calendar.vue` | ✅ Gotovo |
| Pretraga radionica u kalendaru | `Calendar.vue` | ✅ Gotovo |
| Upozorenja za nadolazeće radionice | `Calendar.vue` | ✅ Gotovo |
| Toast notifikacije (polling) | `Notifications.vue` | ✅ Gotovo |
| Odjava sa radionice (dugme "✕ Odustani" + potvrda) | `WorkshopDetail.vue` | ✅ Implementirano (vidi sekciju iznad) |



//maida

# Frontend dokumentacija — WorkshopsView.vue (Pregled, pretraga, ocjenjivanje)

## Svrha

Glavna stranica za pregled radionica — pretraga uživo, filteri (lokacija, datum), prikaz aktivnih i završenih radionica, modal za ocjenjivanje završenih radionica.

## State (relevantan za ovaj dio)

| Varijabla | Tip | Opis |
|---|---|---|
| `workshops` | Array | Lista radionica sa backend-a |
| `error` | String/null | Poruka kad nema rezultata ili API ne radi |
| `searchQuery` / `searchResults` | String / Array | Live pretraga (dropdown) |
| `searchTimeout` | Timer | Debounce handle za pretragu |
| `filterLocation`, `filterDateFrom`, `filterDateTo` | String | Aktivni filteri |
| `dateOpen` | Boolean | Da li je panel za datum otvoren |
| `locationChips` | Array | `'Sve'` + unikatne lokacije iz **trenutno učitanih** radionica (ne svih mogućih lokacija u bazi) |
| `filtersActive` | Computed (Boolean) | Da li je bilo koji filter aktivan (kontroliše prikaz "aktivnih filter tagova") |
| `showRatingModal`, `selectedWorkshopId`, `selectedWorkshopTitle` | Boolean / Number / String | Koja radionica se ocjenjuje |
| `ratingForm` | Object `{ score, comment }` | Forma za ocjenu |
| `ratingSubmitting` | Boolean | Sprečava dupli submit dok je zahtjev u toku |

---

## 1. Pretraga uživo (dropdown)

**Tok:**
1. Korisnik kuca u search bar → `v-model="searchQuery"` → `@input="handleSearch"`
2. `handleSearch()` čisti prethodni `searchTimeout` (debounce) i, ako je `searchQuery` prazan, odmah resetuje `searchResults` na `[]` bez API poziva
3. Nakon 400ms bez nove izmjene → `fetchSearchResults(title)` → `GET /workshops/search?title={title}`
4. Rezultati se prikazuju u dropdown-u ispod search bara — svaki red: naziv, formatiran datum (`formatDate`), lokacija
5. Klik na rezultat (`@mousedown.prevent="goToWorkshop"`) — koristi `mousedown.prevent` umjesto `click` da bi se izbjeglo da `@blur` na input-u zatvori dropdown prije nego se klik registruje
6. `goToWorkshop()` čisti pretragu i radi `router.push('/workshops/{id}')`


---

## 2. Filteri (lokacija + datum)

- **Lokacija:** chips dugmad, klik (`selectLocation`) odmah primjenjuje filter (`applyFilters()`) — bez posebnog "Primijeni" dugmeta
- **Datum:** klik na "Datum" otvara panel sa "Od" i "Do (opciono)" poljima — ovdje je potrebno  kliknuti "Primijeni" da se filter pošalje
- `applyFilters()`:
  - Gradi query parametre samo za aktivne filtere (location, date_from, date_to)
  - Ako je bar jedan filter aktivan → `GET /workshops/search?...`
  - Ako nijedan nije aktivan → `GET /workshops/active` (search se ne zove sa praznim parametrima)
  - Ako je rezultat prazna lista → prikazuje se poruka "Nema radionica koje odgovaraju filterima."
  - Poziva `checkAllRegistrations()` da ažurira "Prijavljen ✓" oznake za novu listu
- **Aktivni filter tagovi** (ispod chips-a, prikazuju se samo ako `filtersActive`): tag za lokaciju (× briše samo lokaciju), tag za datum raspon (× briše oba datuma), i "Resetuj sve ✕" (vraća sve na default i refetch-uje listu)

---

## 3. Prikaz liste

Dvije kolone: **Aktivne radionice** (`status === 'upcoming'`) i **Završene radionice** (`status === 'completed'`).

**Kartica aktivne radionice prikazuje:**

| Element | Uslov | Izgled |
|---|---|---|
| Status bedž | `free_spots > 0` | Zeleno — "Slobodna mjesta" |
| Status bedž | `free_spots <= 0` | Žuto/amber — "Popunjeno" |
| "Prijavljen ✓" bedž | `registrations[id] === true` | Ljubičasto |
| Brojač slobodnih mjesta | `free_spots > 0` i nije prijavljen | Tekst "{n} slobodnih" (zeleno, bold) |
| Link "Saznaj više →" | uvijek | Vodi na `/workshops/{id}` |

**Kartica završene radionice prikazuje:** sivi bedž "Završena", naziv, datum, lokaciju, link "Pogledaj ocjene →" (na `/workshops/{id}`), i dugme "Ocijeni ★".

---

## 4. Ocjenjivanje (rating modal)

**Otvaranje:** `openRatingModal(workshopId, title)` — resetuje formu na `{ score: 0, comment: '' }` i otvara modal.

**UI modala:** pozadina za zatvaranje klikom, X dugme, naslov radionice, 5 zvjezdica (klik postavlja `ratingForm.score`, žute do izabranog broja), textarea za komentar (opciono, max 500 karaktera, 3 reda), dugme za slanje.

**Validacija prije slanja:**

| Provjera | Ponašanje |
|---|---|
| Ocjena nije izabrana (`score === 0`) | Dugme za slanje je `disabled` |
| Nema tokena u `localStorage` | Swal "Greška" / "Morate biti prijavljeni da biste ocijenili radionicu." — poziv se ne šalje |

**API poziv:** `POST /workshops/{id}/ratings` sa body `{ score, comment: comment || null }`

**Obrada odgovora:**

| Slučaj | Ponašanje |
|---|---|
| Uspjeh (201) | Modal se zatvara, confetti animacija (120 čestica), Swal "Hvala!" / "Vaša ocjena je uspješno poslana." |
| Greška, `detail === "Could not validate credentials"` | Swal "Greška" / "Morate biti prijavljeni da biste ocijenili radionicu." |
| Greška, ostali `detail` | Swal "Greška" sa porukom direktno iz `data.detail` |
| Bilo koji ishod | `ratingSubmitting` se vraća na `false` (dugme se ponovo aktivira) |

---

## API pozivi (sažetak)

| Endpoint | Metod | Kada se poziva | Auth |
|---|---|---|---|
| `/workshops/search` | GET | Live pretraga, primjena filtera | Ne |
| `/workshops/active` | GET | Default lista, reset filtera | Ne |
| `/workshops/{id}/ratings` | POST | Slanje ocjene | Da (token iz localStorage) |

# Frontend dokumentacija — WorkshopDetailView.vue (Prikaz detalja radionice, ocjenjivanje)

## Svrha

Stranica za prikaz pojedinačne radionice (ruta `/workshops/:id`) — header sa statusom, opis, podaci o organizatoru, detalji (datum, kapacitet, slobodna mjesta), traka popunjenosti, i — za završene radionice — prikaz i slanje ocjena.


## State

| Varijabla | Tip | Opis |
|---|---|---|
| `workshop` | Object | Podaci o radionici sa backend-a |
| `loading` | Boolean | Prikazuje "Učitavanje..." dok traje fetch |
| `error` | String/null | Poruka pri grešci učitavanja |
| `showRatingModal` | Boolean | Modal za ocjenjivanje |
| `ratings` | Array | Lista ocjena za radionicu |
| `ratingsAverage` | Object `{average, count}` | Prosjek i broj ocjena |
| `alreadyRated` | Boolean | Da li je trenutni korisnik već ocijenio |
| `ratingForm` | Object `{score, comment}` | Forma za novu ocjenu |
| `ratingSubmitting` | Boolean | Sprečava dupli submit |
| `ratingError` | String | Inline poruka greške u modalu za ocjenjivanje |

---

## 1. Header (vizuelni prikaz statusa)

| `workshop.status` | Tekst bedža | Boja tačke |
|---|---|---|
| `'completed'` | "Završena" | zelena (`#86efac`) |
| ostalo (`'upcoming'`) | "Aktivna" | žuta (`#fde68a`) |


Header dalje prikazuje: naslov (`workshop.title`), datum (`formatDate(workshop.date)`), lokaciju (`workshop.location`), i kapacitet (`workshop.capacity`).

---

## 2. Učitavanje podataka (`fetchWorkshop`)

**Tok pri otvaranju stranice (`onMounted`):**

1. `GET /workshops/{id}` — ako odgovor nije `ok`, baca se greška i `error.value` se postavlja na generičku poruku **"Greška pri učitavanju."**
2. Ako postoji token u `localStorage` → `GET /workshops/registration/check/{id}` → postavlja status prijave (koristi se za prikaz dugmeta "Prijavi se" / "✓ Prijavljeni", dokumentovano u postojećoj sekciji o prijavi)
3. Ako je `workshop.status === 'completed'` → poziva se `fetchRatings()`

---

## 3. Kartice sa detaljima

### Opis
Prikazuje `workshop.description` kao običan tekst.

### Organizator
Avatar (prvo slovo `organizer_name`, uppercase, fallback `'O'`), `organizer_name`, `organizer_email` (uvijek), `organizer_phone` (samo ako postoji — `v-if`).

### Detalji radionice

| Polje | Izvor |
|---|---|
| Datum početka | `formatDate(workshop.date)` |
| Završetak | `formatDate(workshop.end_time)` |
| Kapacitet | `workshop.capacity` |
| Slobodna mjesta | `workshop.free_spots` — crveno ako `=== 0`,  u suprotnom je zeleno|

Dugme "⬅ Nazad" (`router-link` na `/workshops`).

### Popunjenost
Traka napretka: širina = `(capacity - free_spots) / capacity * 100%`, boja crvena ako popunjeno, u suprotnom ljubičasto. Ispod, veliki broj `free_spots` sa tekstom "Popunjeno" ili "slobodnih mjesta".

---

## 4. Ocjenjivanje radionice (samo ako `workshop.status === 'completed'`)

### Prosjek ocjena
Prikazuje `ratingsAverage.average` (zaokruženo na 1 decimalu), broj zvjezdica (`Math.round(average)`), traka napretka (`average/5*100%`), i `ratingsAverage.count`.

### Provjera "već ocijenjeno" (`alreadyRated`)
Računa se unutar `fetchRatings()` poređenjem imena:
```js
const username = localStorage.getItem('username')
alreadyRated.value = ratings.value.some(r => r.user_name === username)
```

### Dugme "★ Ocijeni ovu radionicu"
Prikazuje se samo ako `!alreadyRated`. Klik direktno postavlja `showRatingModal = true` (forma se ne resetuje eksplicitno pri otvaranju — zadržava prethodne vrijednosti `score`/`comment` ako je modal ranije bio otvoren i zatvoren bez slanja).

### Lista ocjena
Za svaku ocjenu: avatar (prvo slovo `user_name`, fallback `'U'`), ime (`user_name`, fallback "Nepoznat"), zvjezdice prema `score`, komentar (`comment`, fallback "Bez komentara"). Ako nema ocjena: "Još nema ocjena za ovu radionicu."

### Rating modal — UI
5 zvjezdica (klik → `ratingForm.score = n`, žute do izabranog broja), textarea za komentar (opciono, max 500 karaktera,), inline poruka greške (`ratingError`, crveno), dugme za slanje — `disabled` ako `!ratingForm.score || ratingSubmitting`.

### `submitRating()` — slanje ocjene

| Korak | Ponašanje |
|---|---|
| Nema tokena | `ratingError.value = 'Morate biti prijavljeni da biste ocijenili radionicu.'` — inline u modalu, submit se prekida |
| `POST /workshops/{id}/ratings` body `{score, comment: comment ⏐⏐ null}` | — |
| Greška, `detail === 'Could not validate credentials'` | `ratingError` = "Morate biti prijavljeni..." |
| Greška, ostali `detail` | `ratingError` = `err.detail` (direktno iz backend-a) ili "Greška pri slanju ocjene." |
| Uspjeh (201) | `localStorage.setItem('rated_{id}', '1')`, `alreadyRated = true`, modal se zatvara, confetti, zatim `await fetchRatings()` (refetch sve podatke + ponovo izračuna `alreadyRated`) |
| Network greška (catch) | `ratingError` = "Greška pri slanju ocjene." |
| Bilo koji ishod | `ratingSubmitting` se vraća na `false` |

### `formatDate`
Formatira datum u oblik `DD.MM.YYYY.` — koristi se za header, "Datum početka" i "Završetak".

---

## API pozivi (sažetak)

| Endpoint | Metod | Kada se poziva | Auth |
|---|---|---|---|
| `/workshops/{id}` | GET | Pri učitavanju stranice | Ne |
| `/workshops/registration/check/{id}` | GET | Pri učitavanju (ako ima token), i nakon svakog `fetchRatings()` | Da |
| `/workshops/{id}/ratings/average` | GET | Ako je radionica završena | Ne |
| `/workshops/{id}/ratings` | GET | Ako je radionica završena | Ne |
| `/workshops/{id}/ratings` | POST | Slanje nove ocjene | Da |

---







//mahir
