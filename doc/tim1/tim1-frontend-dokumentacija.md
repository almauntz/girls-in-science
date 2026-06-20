//amel


//elma
# Frontend dokumentacija — Prijava na radionice, Kalendar, Notifikacije

Dokumentacija obuhvata komponente: `RegistrationForm.vue`, `Calendar.vue`, `Notifications.vue`, te dio `WorkshopDetail.vue` vezan za otvaranje forme za prijavu.

---

## 1. RegistrationForm.vue

### Svrha
Forma za prijavu korisnika na radionicu. Prikazuje se kao modal preko `WorkshopDetail.vue` stranice.

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

### Validacija prije slanja (frontend-only, ne ide do backend-a)

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
- ⚠️ Napomena: backend vraća i `message` i `free_spots_left` u body-ju, ali frontend ih **ne koristi** — prikazuje samo fiksni tekst.

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
Samo zatvara modal/formu (`showForm.value = false` u parent komponenti). **Ne poziva nikakav backend endpoint** — nije vezano za odjavu sa radionice, već za odustajanje od popunjavanja forme.

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

⚠️ Ovo **nije** isto dugme "Odustani" iz `RegistrationForm.vue` (ono samo zatvara formu i ostaje nepromijenjeno). Ovo je novo dugme koje se prikazuje **kad je korisnik već prijavljen** i poziva backend da ga odjavi.

#### Izmjena u `<template>`

**Prije:**
```html
<button
  @click="handleRegistrationClick"
  :disabled="wasRegistered"
  class="flex-1 py-2.5 text-white rounded-xl font-bold text-sm transition"
  :style="wasRegistered
    ? 'background:#d1d5db; cursor:not-allowed;'
    : 'background: linear-gradient(135deg, #7c3aed, #a855f7);'"
  :class="!wasRegistered ? 'hover:opacity-90' : ''">
  {{ wasRegistered ? '✓ Prijavljeni' : '🎟 Prijavi se' }}
</button>
```

**Poslije:**
```html
<button
  @click="wasRegistered ? handleCancellation() : handleRegistrationClick()"
  class="flex-1 py-2.5 text-white rounded-xl font-bold text-sm transition hover:opacity-90"
  :style="wasRegistered
    ? 'background:#ef4444;'
    : 'background: linear-gradient(135deg, #7c3aed, #a855f7);'"
>
  {{ wasRegistered ? '✕ Odustani' : '🎟 Prijavi se' }}
</button>
```

| Stanje | Tekst dugmeta | Boja | Klik poziva |
|---|---|---|---|
| `wasRegistered === false` | "🎟 Prijavi se" | ljubičasta | `handleRegistrationClick()` |
| `wasRegistered === true` | "✕ Odustani" | crvena | `handleCancellation()` |

#### Nova funkcija u `<script>` (unutar `setup()`)

```js
const handleCancellation = () => {
  Swal.fire({
    title: 'Da li ste sigurni?',
    text: 'Ako odustanete, izgubićete svoje mjesto na ovoj radionici.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Da, odustani',
    cancelButtonText: 'Ne, ostani prijavljen'
  }).then(async (result) => {
    if (!result.isConfirmed) return

    const token = localStorage.getItem('token')

    try {
      const res = await fetch(`${BASE_URL}/workshops/cancellation/${route.params.id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Greška pri odjavi.')
      }

      const data = await res.json()

      await Swal.fire({
        title: 'Odjavljeni ste',
        text: data.message || 'Uspješno ste odustali od radionice.',
        icon: 'success',
        confirmButtonColor: '#9333ea'
      })

      wasRegistered.value = false
      fetchWorkshop()
    } catch (e) {
      Swal.fire('Greška', e.message || 'Došlo je do greške.', 'error')
    }
  })
}
```

#### Dodati u `return { ... }` na kraju `setup()`

```js
return {
  workshop, loading, error, showForm, showRatingModal,
  ratings, ratingsAverage, alreadyRated, wasRegistered,
  ratingForm, ratingSubmitting, ratingError, isLoggedIn,
  handleSuccess, formatDate, handleRegistrationClick, submitRating,
  handleCancellation   // ← novo
}
```

#### Tok korisničke akcije (UX flow)

1. Korisnik je prijavljen na radionicu → vidi dugme **"✕ Odustani"**
2. Klik → SweetAlert2 popup: *"Da li ste sigurni?"* sa opcijama "Da, odustani" / "Ne, ostani prijavljen"
3. Ako klikne "Ne" → popup se zatvara, ništa se ne mijenja
4. Ako klikne "Da" → poziva se `DELETE /workshops/cancellation/{workshop_id}`
5. **Uspjeh** → popup "Odjavljeni ste", dugme se vraća na "🎟 Prijavi se", podaci o radionici se refetch-uju (ažurira `free_spots`)
6. **Greška** → popup "Greška" sa porukom iz backend-a (`err.detail`)

#### Mogući backend odgovori

⚠️ **Napomena:** Backend ruta `DELETE /workshops/cancellation/{workshop_id}` je trenutno **duplirana** u `workshops.py` (dvije funkcije na istoj ruti). Frontend kod gore radi ispravno u oba slučaja, jer koristi samo `data.message`, ali bi duplikat na backend-u trebalo riješiti.

| Status | Slučaj | Body | Šta korisnik vidi |
|---|---|---|---|
| `200 OK` | Uspješna odjava (verzija sa promocijom) | `{"message": "Uspješno ste odustali od radionice.", "promoted_user_id": null ili broj}` | "Odjavljeni ste" / "Uspješno ste odustali od radionice." |
| `200 OK` | Uspješna odjava (verzija bez promocije) | `{"message": "Uspješno ste odustali od radionice."}` | "Odjavljeni ste" / "Uspješno ste odustali od radionice." |
| `404 Not Found` | Korisnik nema prijavu za tu radionicu | `{"detail": "Nije pronađena vaša prijava za ovu radionicu."}` | "Greška" / "Nije pronađena vaša prijava za ovu radionicu." |

#### TODO / otvoreno pitanje

- [ ] Riješiti duplikat `cancel_registration()` funkcije u backend-u (`workshops.py`) — odlučiti koja verzija ostaje
- [ ] Testirati flow nakon implementacije (prijava → odjava → provjera da li se `Registration` zapis stvarno briše)
- [ ] Provjeriti da li treba i obavijestiti promovisanog korisnika sa waiting liste (ako se koristi verzija sa `promoted_user_id`) — trenutno frontend to ne prikazuje nikome

---

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

## Sažetak — koje su komponente urađene, šta nedostaje

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
