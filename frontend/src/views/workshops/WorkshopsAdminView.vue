<template>
  <div class="combined-admin-page">
 
    <!-- ══════════════════════════════════════════════════════════════
         SEKCIJA 1 — UPRAVLJANJE RADIONICAMA
    ══════════════════════════════════════════════════════════════ -->
    <div class="section-divider">
      <div class="section-divider-line"></div>
      <div class="section-divider-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        Upravljanje radionicama
      </div>
      <div class="section-divider-line"></div>
    </div>
 
    <div class="admin-page">
 
      <div class="page-header">
        <span class="admin-tag">Admin panel</span>
        <h1>Upravljanje radionicama</h1>
        <p class="page-sub">Odaberi akciju koju želiš izvršiti</p>
      </div>
 
      <!-- ── Tri kartice (glavni ekran) ── -->
      <div class="actions-row">
 
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
 
<!-- Modal za kreiranje radionice-->
 
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
 
              <!-- Kapacitet -->
              <div class="field field-narrow">
                <label>Kapacitet <span class="req">*</span></label>
                <input v-model.number="form.capacity" type="number" min="1" placeholder="20"
                       :class="{ 'input-error': errors.capacity }"/>
                <span v-if="errors.capacity" class="err-msg">{{ errors.capacity }}</span>
              </div>
 
              <!-- Organizer fields -->
              <div class="field">
                <label>Organizator - Ime i prezime <span class="req">*</span></label>
                <input v-model="form.organizer_name" type="text" placeholder="npr. Ime Prezime"
                       :class="{ 'input-error': errors.organizer_name }"/>
                <span v-if="errors.organizer_name" class="err-msg">{{ errors.organizer_name }}</span>
              </div>
 
              <div class="field-row">
                <div class="field">
                  <label>Organizator - Email <span class="req">*</span></label>
                  <input v-model="form.organizer_email" type="email" placeholder="organizator@primjer.com"
                         :class="{ 'input-error': errors.organizer_email }"/>
                  <span v-if="errors.organizer_email" class="err-msg">{{ errors.organizer_email }}</span>
                </div>
                <div class="field">
                  <label>Organizator - Telefon</label>
                  <input v-model="form.organizer_phone" type="text" placeholder="+387 61 123 456"
                         :class="{ 'input-error': errors.organizer_phone }"/>
                  <span v-if="errors.organizer_phone" class="err-msg">{{ errors.organizer_phone }}</span>
                </div>
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
              <!-- Organizer fields in edit modal -->
              <div class="field">
                <label>Organizator - Ime i prezime</label>
                <input v-model="form.organizer_name" type="text" placeholder="Ostavi prazno za ne mijenjanje"/>
              </div>
              <div class="field-row">
                <div class="field">
                  <label>Organizator - Email</label>
                  <input v-model="form.organizer_email" type="email" placeholder="Ostavi prazno za ne mijenjanje"/>
                </div>
                <div class="field">
                  <label>Organizator - Telefon</label>
                  <input v-model="form.organizer_phone" type="text" placeholder="Ostavi prazno za ne mijenjanje"/>
                </div>
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
              <button class="btn-delete" @click="askConfirm('delete')">Nastavi</button>
            </div>
 
          </div>
        </div>
      </Teleport>
 
      <!-- Potvrdni prozor za sve akcije (create/edit/delete) -->
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
 
      <!-- Kratke notifikacije dole desno nakon akcije -->
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

   <!-- ══════════════════════════════════════════════════════════════
         SEKCIJA 2 — PREGLED PRIJAVA NA RADIONICE
    ══════════════════════════════════════════════════════════════ -->
    <div class="section-divider">
      <div class="section-divider-line"></div>
      <div class="section-divider-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        Pregled prijava na radionice
      </div>
      <div class="section-divider-line"></div>
    </div>
 
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-8">Admin - Pregled Prijava</h1>
 
      <!-- Odabir radionice -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <label class="block text-lg font-semibold mb-4">Odaberi radionicu:</label>
        <select 
          v-model="selectedWorkshopId"
          @change="loadRegistrations"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="" disabled>-- Odaberi radionicu --</option>
          <option 
            v-for="workshop in workshops" 
            :key="workshop.ID_workshop" 
            :value="workshop.ID_workshop"
          >
            {{ workshop.title }} ({{ new Date(workshop.date).toLocaleDateString('sr-RS') }})
          </option>
        </select>
      </div>
 
      <!-- Poruka o učitavanju ili greški -->
      <div v-if="registrationsLoading" class="text-center py-8">
        <p class="text-gray-600">Učitavanje...</p>
      </div>
 
      <div v-if="registrationsError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8">
        {{ registrationsError }}
      </div>
 
      <!-- Tablica sa prijavama -->
      <div v-if="!registrationsLoading && selectedWorkshopId && registrations.length > 0" class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 border-b" style="background: #ede9fe; border-bottom-color: #ddd6fe;">
          <h2 class="text-xl font-semibold" style="color: #7c3aed;">
            Prijavljeni kandidati ({{ registrations.length }})
          </h2>
        </div>
        
        <table class="w-full">
          <thead class="bg-gray-500 border-b">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">Ime</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">Prezime</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">Email</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">Telefon</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">Iskustvo</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-white">GitHub</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(registration, index) in registrations" 
              :key="registration.id"
              :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-100'"
            >
              <td class="px-6 py-3 text-sm text-gray-900">{{ registration.first_name }}</td>
              <td class="px-6 py-3 text-sm text-gray-900">{{ registration.last_name }}</td>
              <td class="px-6 py-3 text-sm text-gray-900">{{ registration.email }}</td>
              <td class="px-6 py-3 text-sm text-gray-900">{{ registration.phone }}</td>
              <td class="px-6 py-3 text-sm text-gray-600">
                <span v-if="registration.previous_experience" class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {{ registration.previous_experience }}
                </span>
                <span v-else class="text-xs text-gray-400">-</span>
              </td>
              <td class="px-6 py-3 text-sm">
                <a 
                  v-if="registration.github_profile"
                  :href="registration.github_profile"
                  target="_blank"
                  class="text-blue-600 hover:text-blue-800 underline"
                >
                  Profil
                </a>
                <span v-else class="text-gray-400">-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
 
      <!-- Poruka kada nema prijava -->
      <div v-if="!registrationsLoading && selectedWorkshopId && registrations.length === 0" class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
        Nema prijavljenih kandidata za odabranu radionicu.
      </div>
    </div> 
 
    <!-- ══════════════════════════════════════════════════════════════
         SEKCIJA 3 — PRIJEDLOZI RADIONICA
    ══════════════════════════════════════════════════════════════ -->
    <div class="section-divider">
      <div class="section-divider-line"></div>
      <div class="section-divider-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="9" y1="12" x2="15" y2="12"/>
          <line x1="9" y1="16" x2="12" y2="16"/>
        </svg>
        Prijedlozi radionica
      </div>
      <div class="section-divider-line"></div>
    </div>
 
    <div class="admin-page">
 
      <div class="page-header">
        <span class="admin-tag">Admin panel</span>
        <h1>Prijedlozi radionica</h1>
        <p class="page-sub">Pregled i obrada prijedloga od studentica</p>
      </div>
 
      <div class="filter-row">
        <button
          v-for="f in filters"
          :key="f.value"
          class="filter-btn"
          :class="{ active: activeFilter === f.value, [`filter-${f.value}`]: true }"
          @click="setFilter(f.value)"
        >
          <span class="filter-dot" :class="`dot-${f.value}`"></span>
          {{ f.label }}
          <span class="filter-count">{{ countFor(f.value) }}</span>
        </button>
      </div>
 
      <div v-if="proposalsLoading" class="loading-state">
        <span class="spin spin-dark"></span>
        <span>Učitavanje prijedloga…</span>
      </div>
 
      <!-- ── Prazna lista ── -->
      <div v-else-if="filteredProposals.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="9" y1="12" x2="15" y2="12"/>
            <line x1="9" y1="16" x2="12" y2="16"/>
          </svg>
        </div>
        <p>Nema prijedloga za odabrani filter.</p>
      </div>
 
      <!-- ── Lista prijedloga ── -->
      <div v-else class="proposals-list">
        <div
          v-for="p in filteredProposals"
          :key="p.id"
          class="proposal-card"
          :class="`card-${p.status}`"
          @click="openDetail(p)"
        >
          <div class="card-left">
            <span class="status-badge" :class="`badge-${p.status}`">
              {{ statusLabel(p.status) }}
            </span>
            <h3 class="proposal-title">{{ p.title }}</h3>
            <p class="proposal-desc">{{ truncate(p.description, 120) }}</p>
            <div class="card-meta">
              <span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                {{ p.proposed_by_email }}
              </span>
              <span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                {{ formatDate(p.created_at) }}
              </span>
            </div>
          </div>
          <div class="card-arrow">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </div>
        </div>
      </div>
 
      <!-- ── Modal: detalj prijedloga ── -->
      <Teleport to="body">
        <div v-if="detailProposal" class="overlay" @click.self="closeDetail">
          <div class="modal modal-detail">
 
            <div class="modal-head" :class="`head-${detailProposal.status}`">
              <div class="mh-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <div>
                <h2>Prijedlog #{{ detailProposal.id }}</h2>
                <p>
                  <span class="status-badge" :class="`badge-${detailProposal.status}`">
                    {{ statusLabel(detailProposal.status) }}
                  </span>
                </p>
              </div>
              <button class="close-btn" @click="closeDetail">&#x2715;</button>
            </div>
 
            <div class="modal-body">
              <!-- Naslov i email -->
              <div class="detail-field">
                <span class="detail-label">Naziv radionice</span>
                <span class="detail-value">{{ detailProposal.title }}</span>
              </div>
              <div class="detail-field">
                <span class="detail-label">Opis</span>
                <span class="detail-value detail-desc">{{ detailProposal.description }}</span>
              </div>
              <div class="field-row">
                <div class="detail-field">
                  <span class="detail-label">Predložila</span>
                  <span class="detail-value">{{ detailProposal.proposed_by_email }}</span>
                </div>
                <div class="detail-field">
                  <span class="detail-label">Datum prijedloga</span>
                  <span class="detail-value">{{ formatDate(detailProposal.created_at) }}</span>
                </div>
              </div>
 
              <!-- Admin nota (ako postoji) -->
              <div v-if="detailProposal.admin_note" class="admin-note-box">
                <span class="note-label">Napomena admina</span>
                <p>{{ detailProposal.admin_note }}</p>
              </div>
 
              <!-- Akcije: samo za pending -->
              <template v-if="detailProposal.status === 'pending'">
                <div class="action-divider">
                  <span>Obrada prijedloga</span>
                </div>
 
                <!-- Reject forma -->
                <div v-if="actionMode === 'reject'" class="action-form action-form-reject">
                  <div class="field">
                    <label>Razlog odbijanja (opcionalno)</label>
                    <textarea v-model="actionNote" rows="3" placeholder="Upiši kratko obrazloženje…"></textarea>
                  </div>
                  <div class="form-actions">
                    <button class="btn-secondary" @click="actionMode = null">Odustani</button>
                    <button class="btn-delete" @click="askConfirmAction('reject')" :disabled="busy">
                      <span v-if="busy" class="spin"></span>
                      Odbij prijedlog
                    </button>
                  </div>
                </div>
 
                <!-- Approve forma -->
                <div v-else-if="actionMode === 'approve'" class="action-form action-form-approve">
                  <div class="field">
                    <label>Napomena za studenticu (opcionalno)</label>
                    <textarea v-model="actionNote" rows="2" placeholder="Npr. Odlična ideja, kreirali smo radionicu!"></textarea>
                  </div>
 
                  <div class="field toggle-row">
                    <label class="toggle-label">
                      <input type="checkbox" v-model="createWorkshop" class="toggle-input"/>
                      <span class="toggle-track">
                        <span class="toggle-thumb"></span>
                      </span>
                      Odmah kreiraj radionicu iz prijedloga
                    </label>
                  </div>
 
                  <!-- Polja za radionicu (opcionalano, samo ako je toggle uključen) -->
                  <template v-if="createWorkshop">
                    <p class="loaded-label">Popuni podatke za novu radionicu</p>
                    <div class="field-row">
                      <div class="field">
                        <label>Lokacija <span class="req">*</span></label>
                        <input v-model="workshopForm.location" type="text" placeholder="npr. Sala A, PMF"
                               :class="{ 'input-error': workshopErrors.location }"/>
                        <span v-if="workshopErrors.location" class="err-msg">{{ workshopErrors.location }}</span>
                      </div>
                      <div class="field">
                        <label>Kapacitet <span class="req">*</span></label>
                        <input v-model.number="workshopForm.capacity" type="number" min="1"
                               :class="{ 'input-error': workshopErrors.capacity }"/>
                        <span v-if="workshopErrors.capacity" class="err-msg">{{ workshopErrors.capacity }}</span>
                      </div>
                    </div>
                    <div class="field-row">
                      <div class="field">
                        <label>Datum početka <span class="req">*</span></label>
                        <input v-model="workshopForm.date" type="date"
                               :class="{ 'input-error': workshopErrors.date }"/>
                        <span v-if="workshopErrors.date" class="err-msg">{{ workshopErrors.date }}</span>
                      </div>
                      <div class="field">
                        <label>Datum kraja <span class="req">*</span></label>
                        <input v-model="workshopForm.end_time" type="date"
                               :class="{ 'input-error': workshopErrors.end_time }"/>
                        <span v-if="workshopErrors.end_time" class="err-msg">{{ workshopErrors.end_time }}</span>
                      </div>
                    </div>
                  </template>
 
                  <div class="form-actions">
                    <button class="btn-secondary" @click="actionMode = null">Odustani</button>
                    <button class="btn-create" @click="askConfirmAction('approve')" :disabled="busy">
                      <span v-if="busy" class="spin"></span>
                      {{ createWorkshop ? 'Odobri i kreiraj radionicu' : 'Odobri prijedlog' }}
                    </button>
                  </div>
                </div>
 
                <!-- Početni gumbi (reject/approve) -->
                <div v-else class="pending-actions">
                  <button class="btn-delete" @click="actionMode = 'reject'">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                    Odbij
                  </button>
                  <button class="btn-create" @click="actionMode = 'approve'">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Odobri
                  </button>
                </div>
              </template>
            </div>
 
          </div>
        </div>
      </Teleport>
      
      <!-- ── Potvrdni prozor ── -->
      <Teleport to="body">
        <div v-if="proposalConfirmConfig" class="overlay overlay-top" @click.self="proposalConfirmConfig = null">
          <div class="modal modal-narrow confirm-modal">
            <div class="confirm-icon" :class="proposalConfirmConfig.iconClass">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
            </div>
            <h3 class="confirm-title">{{ proposalConfirmConfig.title }}</h3>
            <p class="confirm-msg">{{ proposalConfirmConfig.message }}</p>
            <div class="confirm-actions">
              <button class="btn-secondary" @click="proposalConfirmConfig = null" :disabled="busy">Odustani</button>
              <button :class="proposalConfirmConfig.btnClass" @click="runProposalAction" :disabled="busy">
                <span v-if="busy" class="spin"></span>
                {{ busy ? 'U toku…' : proposalConfirmConfig.btnLabel }}
              </button>
            </div>
          </div>
        </div>
      </Teleport>
 
      <!-- ── Toast notifikacije ── -->
      <Transition name="toast">
        <div v-if="proposalToast.show" class="toast" :class="`toast-${proposalToast.type}`">
          <svg v-if="proposalToast.type === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
          {{ proposalToast.message }}
        </div>
      </Transition>
 
    </div>
    <!-- ── Kraj ProposalAdminView ── -->
 
  </div>
</template>