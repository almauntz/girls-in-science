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

</div>
</template> 