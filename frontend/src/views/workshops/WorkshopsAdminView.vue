<template>
  <!--
    ================================================================
    WorkshopsAdminView.vue
    ================================================================
    Ovo je admin stranica za upravljanje radionicama.
    Koristi 4 backend endpointa:
      POST   /workshops/           → kreiranje
      GET    /workshops/{id}       → učitavanje za edit
      PATCH  /workshops/{id}       → uređivanje
      DELETE /workshops/{id}       → brisanje
 
    Gdje smjestiti ovaj fajl:
      src/views/workshops/WorkshopsAdminView.vue
 
    Ruta koju dodaješ u src/router/index.js:
      {
        path: '/workshops/admin',
        component: () => import('../views/workshops/WorkshopsAdminView.vue'),
        meta: { requiresAuth: true }
      }
    ================================================================
  -->
  <div class="admin-page">
 
    <!-- ── Naslov stranice ── -->
    <div class="page-header">
      <span class="admin-tag">Admin panel</span>
      <h1>Upravljanje radionicama</h1>
      <p class="page-sub">Odaberi akciju koju želiš izvršiti</p>
    </div>
 
    <!-- ── Tri kartice (glavni ekran) ── -->
    <div class="actions-row">
 
      <!-- Kartica 1: Kreiraj -->
      <button class="action-card card-create" @click="openModal('create')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
        </div>
        <span class="card-label">Kreiraj radionicu</span>
        <span class="card-hint">Dodaj novu radionicu na platformu</span>
      </button>
 
      <!-- Kartica 2: Uredi -->
      <button class="action-card card-edit" @click="openModal('edit')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
        <span class="card-label">Uredi radionicu</span>
        <span class="card-hint">Izmijeni podatke postojeće radionice</span>
      </button>
 
      <!-- Kartica 3: Obriši -->
      <button class="action-card card-delete" @click="openModal('delete')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
            <path d="M10 11v6"/><path d="M14 11v6"/>
            <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
        </div>
        <span class="card-label">Obriši radionicu</span>
        <span class="card-hint">Trajno ukloni radionicu iz sistema</span>
      </button>
 
    </div>

<!-- Otvaranje klikom na kreiraj radionicu-->

    <Teleport to="body">
      <div v-if="activeModal === 'create'" class="overlay" @click.self="closeModal">
        <div class="modal">
 
          <div class="modal-head head-create">
            <div class="mh-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            </div>
            <div>
              <h2>Nova radionica</h2>
              <p>Popuni sva obavezna polja</p>
            </div>
            <button class="close-btn" @click="closeModal">&#x2715;</button>
          </div>
 
          <div class="modal-body">
            <!-- Naziv i lokacija u jednom redu -->
            <div class="field-row">
              <div class="field">
                <label>Naziv <span class="req">*</span></label>
                <input v-model="form.title" type="text" placeholder="npr. Uvod u Python"
                       :class="{ 'input-error': errors.title }"/>
                <span v-if="errors.title" class="err-msg">{{ errors.title }}</span>
              </div>
              <div class="field">
                <label>Lokacija <span class="req">*</span></label>
                <input v-model="form.location" type="text" placeholder="npr. Sala A, PMF"
                       :class="{ 'input-error': errors.location }"/>
                <span v-if="errors.location" class="err-msg">{{ errors.location }}</span>
              </div>
            </div>
 
            <!-- Opis -->
            <div class="field">
              <label>Opis <span class="req">*</span></label>
              <textarea v-model="form.description" rows="3" placeholder="Kratki opis radionice…"
                        :class="{ 'input-error': errors.description }"></textarea>
              <span v-if="errors.description" class="err-msg">{{ errors.description }}</span>
            </div>
 
            <!--
              Datum početka i kraja — type="date" (bez vremena).
              Kada se šalje backendu, konvertujemo u ISO format
              u funkciji dateToISO() npr. "2025-06-15" → "2025-06-15T00:00:00.000Z"
            -->
            <div class="field-row">
              <div class="field">
                <label>Datum početka <span class="req">*</span></label>
                <input v-model="form.date" type="date"
                       :class="{ 'input-error': errors.date }"/>
                <span v-if="errors.date" class="err-msg">{{ errors.date }}</span>
              </div>
              <div class="field">
                <label>Datum kraja <span class="req">*</span></label>
                <input v-model="form.end_time" type="date"
                       :class="{ 'input-error': errors.end_time }"/>
                <span v-if="errors.end_time" class="err-msg">{{ errors.end_time }}</span>
              </div>
            </div>
 
            <!-- Kapacitet — uži input -->
            <div class="field field-narrow">
              <label>Kapacitet <span class="req">*</span></label>
              <input v-model.number="form.capacity" type="number" min="1" placeholder="20"
                     :class="{ 'input-error': errors.capacity }"/>
              <span v-if="errors.capacity" class="err-msg">{{ errors.capacity }}</span>
            </div>
          </div>
 
          <div class="modal-foot">
            <button class="btn-secondary" @click="closeModal">Odustani</button>
            <!-- Validira formu, pa otvara potvrdni prozor -->
            <button class="btn-create" @click="askConfirm('create')">Kreiraj radionicu</button>
          </div>
 
        </div>
      </div>
    </Teleport>

<!-- Modal za uređivanje radionice -->

    <Teleport to="body">
      <div v-if="activeModal === 'edit'" class="overlay" @click.self="closeModal">
        <div class="modal">
 
          <div class="modal-head head-edit">
            <div class="mh-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </div>
            <div>
              <h2>Uredi radionicu</h2>
              <p>{{ editStep === 1 ? 'Korak 1 — unesi ID radionice' : `Korak 2 — izmijeni podatke (#${editId})` }}</p>
            </div>
            <button class="close-btn" @click="closeModal">&#x2715;</button>
          </div>
 
          <!-- Korak 1: samo polje za ID -->
          <div v-if="editStep === 1" class="modal-body">
            <div class="field">
              <label>ID radionice <span class="req">*</span></label>
              <input v-model.number="editId" type="number" min="1" placeholder="npr. 5"
                     :class="{ 'input-error': errors.editId }"/>
              <span v-if="errors.editId" class="err-msg">{{ errors.editId }}</span>
            </div>
            <p class="hint-text">ID možeš pronaći na listi radionica.</p>
          </div>
 
          <!-- Korak 2: forma popunjena podacima s API-ja -->
          <div v-else class="modal-body">
            <p class="loaded-label">Ostavi polje prazno ako ga ne želiš mijenjati</p>
 
            <div class="field-row">
              <div class="field">
                <label>Naziv</label>
                <input v-model="form.title" type="text" placeholder="Ostavi prazno za ne mijenjanje"/>
              </div>
              <div class="field">
                <label>Lokacija</label>
                <input v-model="form.location" type="text" placeholder="Ostavi prazno za ne mijenjanje"/>
              </div>
            </div>
 
            <div class="field">
              <label>Opis</label>
              <textarea v-model="form.description" rows="3"
                        placeholder="Ostavi prazno za ne mijenjanje"></textarea>
            </div>
 
            <!-- Datum bez vremena, isto kao kod kreiranja -->
            <div class="field-row">
              <div class="field">
                <label>Datum početka</label>
                <input v-model="form.date" type="date"/>
              </div>
              <div class="field">
                <label>Datum kraja</label>
                <input v-model="form.end_time" type="date"/>
              </div>
            </div>
 
            <div class="field field-narrow">
              <label>Kapacitet</label>
              <input v-model.number="form.capacity" type="number" min="1" placeholder="—"/>
            </div>
          </div>
 
          <div class="modal-foot">
            <button class="btn-secondary" @click="closeModal">Odustani</button>
            <!-- Korak 1: učitaj podatke s API-ja -->
            <button v-if="editStep === 1" class="btn-edit" @click="loadWorkshop" :disabled="busy">
              <span v-if="busy" class="spin"></span>
              {{ busy ? 'Učitavanje…' : 'Dalje →' }}
            </button>
            <!-- Korak 2: otvori potvrdni prozor -->
            <button v-else class="btn-edit" @click="askConfirm('edit')">
              Sačuvaj promjene
            </button>
          </div>
 
        </div>
      </div>
    </Teleport>

    <!-- Modal za brijsanje radionice -->

    <Teleport to="body">
      <div v-if="activeModal === 'delete'" class="overlay" @click.self="closeModal">
        <div class="modal modal-narrow">
 
          <div class="modal-head head-delete">
            <div class="mh-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
              </svg>
            </div>
            <div>
              <h2>Obriši radionicu</h2>
              <p>Upiši ID i potvrdi brisanje</p>
            </div>
            <button class="close-btn" @click="closeModal">&#x2715;</button>
          </div>
 
          <div class="modal-body">
            <div class="field">
              <label>ID radionice <span class="req">*</span></label>
              <input v-model.number="deleteId" type="number" min="1" placeholder="npr. 5"
                     :class="{ 'input-error': errors.deleteId }"/>
              <span v-if="errors.deleteId" class="err-msg">{{ errors.deleteId }}</span>
            </div>
            <!-- Vizuelno upozorenje da je brisanje trajno -->
            <div class="danger-notice">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              Brisanje je trajno i ne može se poništiti.
            </div>
          </div>
 
          <div class="modal-foot">
            <button class="btn-secondary" @click="closeModal">Odustani</button>
            <!-- Provjeri ID pa otvori potvrdu -->
            <button class="btn-delete" @click="askConfirm('delete')">Nastavi</button>
          </div>
 
        </div>
      </div>
    </Teleport>
 
    <!-- ================================================================
         POTVRDNI PROZOR (dijeli se za sve tri akcije)
         Prikazuje se iznad aktivnog modala (z-index: 50 vs 40).
         confirmConfig objekt određuje tekst i boju ovisno o akciji.
         Klik na potvrdu poziva odgovarajuću API funkciju.
    ================================================================ -->
    <Teleport to="body">
      <div v-if="confirmConfig" class="overlay overlay-top" @click.self="confirmConfig = null">
        <div class="modal modal-narrow confirm-modal">
 
          <!-- Ikona mijenja boju ovisno o tipu akcije -->
          <div class="confirm-icon" :class="confirmConfig.iconClass">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
 
          <h3 class="confirm-title">{{ confirmConfig.title }}</h3>
          <p class="confirm-msg">{{ confirmConfig.message }}</p>
 
          <div class="confirm-actions">
            <button class="btn-secondary" @click="confirmConfig = null" :disabled="busy">
              Odustani
            </button>
            <!-- Dugme za potvrdu — boja se mijenja (create/edit/delete) -->
            <button :class="confirmConfig.btnClass" @click="runAction" :disabled="busy">
              <span v-if="busy" class="spin"></span>
              {{ busy ? 'U toku…' : confirmConfig.btnLabel }}
            </button>
          </div>
 
        </div>
      </div>
    </Teleport>
 
    <!-- ================================================================
         TOAST NOTIFIKACIJE
         Prikazuju se dolje desno nakon svake akcije.
         Nestaju automatski nakon 3.8 sekundi.
         toast.type = 'success' → zelena | 'error' → crvena
    ================================================================ -->
    <Transition name="toast">
      <div v-if="toast.show" class="toast" :class="`toast-${toast.type}`">
        <svg v-if="toast.type === 'success'" width="14" height="14" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="3">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-width="3">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
        {{ toast.message }}
      </div>
    </Transition>
 
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
 
// ================================================================
// KONFIGURACIJA
// Promijeni BASE_URL ako backend ne radi na defaultnom portu.
// VITE_API_URL možeš postaviti u .env fajl u root projekta:
//   VITE_API_URL=http://localhost:8000
// ================================================================
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
 
// ================================================================
// STATE — reaktivne varijable koje kontrolišu UI
// ================================================================
const activeModal  = ref(null)   // koji modal je otvoren: 'create' | 'edit' | 'delete' | null
const confirmConfig = ref(null)  // konfiguracija potvrdnog prozora (ili null ako je zatvoren)
const busy         = ref(false)  // true dok čekamo odgovor s API-ja (onemogućava dugmad)
const editStep     = ref(1)      // korak edit modala: 1 = unos ID-a, 2 = forma
const editId       = ref(null)   // ID radionice za uređivanje
const deleteId     = ref(null)   // ID radionice za brisanje
 
// Podaci koje admin upisuje u formu (kreiranje i uređivanje)
const form = reactive({
  title: '',
  description: '',
  location: '',
  date: '',       // format: "YYYY-MM-DD" (iz type="date" inputa)
  end_time: '',   // format: "YYYY-MM-DD" (iz type="date" inputa)
  capacity: null
})
 
// Poruke grešaka validacije — prikazuju se ispod polja
const errors = reactive({
  title: '', description: '', location: '',
  date: '', end_time: '', capacity: '',
  editId: '',   // greška za polje ID-a u edit modalu
  deleteId: ''  // greška za polje ID-a u delete modalu
})
 
// Stanje toast notifikacije
const toast = reactive({ show: false, type: 'success', message: '' })
 
// ================================================================
// POMOĆNE FUNKCIJE
// ================================================================
 
// Čita Bearer token iz localStorage i vraća headere za API pozive.
// Token se sprema u localStorage pri prijavi (LoginView.vue).
function authHeaders() {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
}
 
// Pretvara string datuma "YYYY-MM-DD" (iz date inputa)
// u ISO datetime string koji FastAPI backend očekuje.
// npr. "2025-06-15" → "2025-06-15T00:00:00.000Z"
function dateToISO(dateStr) {
  if (!dateStr) return null
  return new Date(dateStr + 'T00:00:00').toISOString()
}
 
// Otvara modal i resetuje svo stanje iz prethodne akcije
function openModal(type) {
  resetAll()
  activeModal.value = type
}
 
// Zatvara sve modalne prozore i čisti stanje
function closeModal() {
  activeModal.value = null
  confirmConfig.value = null
  busy.value = false
  resetAll()
}
 
// Resetuje formu, greške i pomoćne varijable na početne vrijednosti
function resetAll() {
  Object.assign(form, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: null
  })
  Object.assign(errors, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: '',
    editId: '', deleteId: ''
  })
  editId.value   = null
  deleteId.value = null
  editStep.value = 1
}
 
// ================================================================
// VALIDACIJA — provjera forme prije slanja
// ================================================================
 
// Validira formu za kreiranje. Vraća true ako je sve ok.
// Greške se postavljaju direktno u errors objekt i prikazuju u UI-u.
function validateCreate() {
  Object.assign(errors, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: ''
  })
  let ok = true
 
  if (!form.title.trim())
    { errors.title = 'Naziv je obavezan.'; ok = false }
  if (!form.description.trim())
    { errors.description = 'Opis je obavezan.'; ok = false }
  if (!form.location.trim())
    { errors.location = 'Lokacija je obavezna.'; ok = false }
  if (!form.date)
    { errors.date = 'Datum početka je obavezan.'; ok = false }
  if (!form.end_time)
    { errors.end_time = 'Datum kraja je obavezan.'; ok = false }
  if (!form.capacity || form.capacity < 1)
    { errors.capacity = 'Kapacitet mora biti ≥ 1.'; ok = false }
  if (form.date && form.end_time && form.date > form.end_time)
    { errors.end_time = 'Datum kraja mora biti nakon početka.'; ok = false }
 
  return ok
}
 
// ================================================================
// OTVARANJE POTVRDNOG PROZORA
// Svaka akcija ima svoju konfiguraciju (tekst, boja, šta pozvati).
// Potvrdni prozor se prikazuje iznad aktivnog modala.
// ================================================================
function askConfirm(action) {
  // Validacija prije otvaranja potvrde
  if (action === 'create' && !validateCreate()) return
  if (action === 'delete') {
    errors.deleteId = ''
    if (!deleteId.value || deleteId.value < 1) {
      errors.deleteId = 'Upiši ispravan ID.'
      return
    }
  }
 
  // Konfiguracija potvrdnog prozora ovisno o akciji
  const configs = {
    create: {
      title:     'Potvrdi kreiranje',
      message:   `Kreiraš novu radionicu „${form.title}". Jesi li sigurna?`,
      btnLabel:  'Da, kreiraj',
      btnClass:  'btn-create',
      iconClass: 'icon-create',
      action:    doCreate
    },
    edit: {
      title:     'Potvrdi izmjene',
      message:   `Spremaš izmjene za radionicu #${editId.value}. Nastavi?`,
      btnLabel:  'Da, sačuvaj',
      btnClass:  'btn-edit',
      iconClass: 'icon-edit',
      action:    doEdit
    },
    delete: {
      title:     'Potvrdi brisanje',
      message:   `Trajno ćeš obrisati radionicu #${deleteId.value}. Ova akcija se ne može poništiti!`,
      btnLabel:  'Da, obriši trajno',
      btnClass:  'btn-delete',
      iconClass: 'icon-delete',
      action:    doDelete
    }
  }
 
  confirmConfig.value = configs[action]
}
 
// Poziva se klikom na "Potvrdi" — pokreće odgovarajući API poziv
async function runAction() {
  if (confirmConfig.value?.action) {
    await confirmConfig.value.action()
  }
}
 
// ================================================================
// API POZIVI
// ================================================================
 
// POST /workshops/ — kreira novu radionicu
// Šalje sve podatke iz forme, datume konvertuje u ISO format
async function doCreate() {
  busy.value = true
  try {
    const body = {
      title:       form.title.trim(),
      description: form.description.trim(),
      location:    form.location.trim(),
      date:        dateToISO(form.date),
      end_time:    dateToISO(form.end_time),
      capacity:    form.capacity
    }
    const res = await fetch(`${BASE_URL}/workshops/`, {
      method:  'POST',
      headers: authHeaders(),
      body:    JSON.stringify(body)
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    showToast('success', 'Radionica uspješno kreirana!')
    closeModal()
  } catch (e) {
    showToast('error', e.message || 'Kreiranje nije uspjelo.')
    confirmConfig.value = null // zatvori potvrdu, vrati korisnika na formu
  } finally {
    busy.value = false
  }
}
 
// GET /workshops/{id} — dohvata podatke radionice za popunjavanje edit forme
// Poziva se klikom na "Dalje →" u koraku 1 edit modala
async function loadWorkshop() {
  errors.editId = ''
  if (!editId.value || editId.value < 1) {
    errors.editId = 'Upiši ispravan ID.'
    return
  }
  busy.value = true
  try {
    const res = await fetch(`${BASE_URL}/workshops/${editId.value}`, {
      headers: authHeaders()
    })
    if (!res.ok) {
      errors.editId = `Radionica #${editId.value} nije pronađena.`
      return
    }
    const w = await res.json() // WorkshopDetailRead schema
 
    // Popuni formu s podacima koji su došli s API-ja
    // .slice(0, 10) uzima samo "YYYY-MM-DD" dio ISO stringa
    Object.assign(form, {
      title:       w.title       ?? '',
      description: w.description ?? '',
      location:    '',  // WorkshopDetailRead ne vraća location, admin unese ručno
      date:        w.date     ? w.date.slice(0, 10)     : '',
      end_time:    w.end_time ? w.end_time.slice(0, 10) : '',
      capacity:    w.capacity ?? null
    })
    editStep.value = 2 // prijeđi na drugi korak
  } catch {
    errors.editId = 'Greška pri učitavanju. Provjeri server.'
  } finally {
    busy.value = false
  }
}
 
// PATCH /workshops/{id} — ažurira samo polja koja su popunjena
// Prazna polja se ne šalju — backend ih neće dirati (partial update)
async function doEdit() {
  busy.value = true
  try {
    // Prikupljamo samo popunjena polja
    const body = {}
    if (form.title.trim())       body.title       = form.title.trim()
    if (form.description.trim()) body.description = form.description.trim()
    if (form.location.trim())    body.location    = form.location.trim()
    if (form.date)               body.date        = dateToISO(form.date)
    if (form.end_time)           body.end_time    = dateToISO(form.end_time)
    if (form.capacity)           body.capacity    = form.capacity
 
    const res = await fetch(`${BASE_URL}/workshops/${editId.value}`, {
      method:  'PATCH',
      headers: authHeaders(),
      body:    JSON.stringify(body)
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    showToast('success', `Radionica #${editId.value} uspješno ažurirana!`)
    closeModal()
  } catch (e) {
    showToast('error', e.message || 'Ažuriranje nije uspjelo.')
    confirmConfig.value = null
  } finally {
    busy.value = false
  }
}
 
// DELETE /workshops/{id} — trajno briše radionicu
// Backend vraća 204 No Content (prazan odgovor), nema JSON-a
async function doDelete() {
  busy.value = true
  try {
    const res = await fetch(`${BASE_URL}/workshops/${deleteId.value}`, {
      method:  'DELETE',
      headers: authHeaders()
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    showToast('success', `Radionica #${deleteId.value} uspješno obrisana.`)
    closeModal()
  } catch (e) {
    showToast('error', e.message || 'Brisanje nije uspjelo.')
    confirmConfig.value = null
  } finally {
    busy.value = false
  }
}
 
// ================================================================
// TOAST — kratka notifikacija dolje desno
// Automatski nestaje nakon 3.8 sekundi
// ================================================================
function showToast(type, message) {
  toast.show = false
  setTimeout(() => {
    Object.assign(toast, { show: true, type, message })
    setTimeout(() => { toast.show = false }, 3800)
  }, 40)
}
</script>