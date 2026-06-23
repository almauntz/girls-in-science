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
                <p>{{ editStep === 1 ? 'Odaberi radionicu za uređivanje' : `Izmijeni podatke (#${editId})` }}</p>
              </div>
              <button class="close-btn" @click="closeModal">&#x2715;</button>
            </div>
 
            <!-- Korak 1: padajući meni sa radionicama -->
            <div v-if="editStep === 1" class="modal-body">
              <div class="field">
                <label>Radionica <span class="req">*</span></label>
                <select v-model.number="editId" class="workshop-select" :class="{ 'input-error': errors.editId }">
                  <option value="" disabled>— Odaberi radionicu —</option>
                  <option
                    v-for="w in workshops"
                    :key="w.ID_workshop"
                    :value="w.ID_workshop"
                  >
                    {{ w.title }} · {{ new Date(w.date).toLocaleDateString('bs-BA') }}
                  </option>
                </select>
                <span v-if="errors.editId" class="err-msg">{{ errors.editId }}</span>
              </div>
            </div> 

            <!-- Korak 2: forma popunjena podacima s API-ja -->
            <div v-else class="modal-body">
              <p class="loaded-label">Ostavi netaknuto polje ako ga ne želiš mijenjati</p>
 
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
                <p>Odaberi radionicu i potvrdi brisanje</p>
              </div>
              <button class="close-btn" @click="closeModal">&#x2715;</button>
            </div>
 
            <div class="modal-body">
              <div class="field">
                <label>Radionica <span class="req">*</span></label>
                <select v-model.number="deleteId" class="workshop-select" :class="{ 'input-error': errors.deleteId }">
                  <option value="" disabled>— Odaberi radionicu —</option>
                  <option
                    v-for="w in workshops"
                    :key="w.ID_workshop"
                    :value="w.ID_workshop"
                  >
                    {{ w.title }} · {{ new Date(w.date).toLocaleDateString('bs-BA') }}
                  </option>
                </select>
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
      <!-- Odabir radionice -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <label class="block text-lg font-semibold mb-4">Odaberi radionicu:</label>
        <select
          v-model="selectedWorkshopId"
          @change="loadRegistrations"
          class="workshop-select"
        >
          <option value="" disabled>— Odaberi radionicu —</option>
          <option
            v-for="workshop in workshops"
            :key="workshop.ID_workshop"
            :value="workshop.ID_workshop"
          >
            {{ workshop.title }} · {{ new Date(workshop.date).toLocaleDateString('bs-BA') }}
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
                    <div class="field">
    <label>Organizator - Ime i prezime <span class="req">*</span></label>
    <input v-model="workshopForm.organizer_name" type="text" placeholder="npr. Ime Prezime"
           :class="{ 'input-error': workshopErrors.organizer_name }"/>
    <span v-if="workshopErrors.organizer_name" class="err-msg">{{ workshopErrors.organizer_name }}</span>
  </div>
  <div class="field-row">
    <div class="field">
      <label>Organizator - Email <span class="req">*</span></label>
      <input v-model="workshopForm.organizer_email" type="email" placeholder="organizator@primjer.com"
             :class="{ 'input-error': workshopErrors.organizer_email }"/>
      <span v-if="workshopErrors.organizer_email" class="err-msg">{{ workshopErrors.organizer_email }}</span>
    </div>
    <div class="field">
      <label>Organizator - Telefon</label>
      <input v-model="workshopForm.organizer_phone" type="text" placeholder="+387 61 123 456"/>
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

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
 
const BASE_URL = import.meta.env.VITE_API_URL
 
// ================================================================
// UPRAVLJANJE RADIONICAMA
// ================================================================
 
const activeModal  = ref(null)
const confirmConfig = ref(null)
const busy         = ref(false)
const editStep     = ref(1)
const editId       = ref('')
const deleteId     = ref('')
 
const form = reactive({
  title: '',
  description: '',
  location: '',
  date: '',
  end_time: '',
  capacity: null,
  organizer_name: '',
  organizer_email: '',
  organizer_phone: ''
})
 
const errors = reactive({
  title: '', description: '', location: '',
  date: '', end_time: '', capacity: '',
  organizer_name: '', organizer_email: '', organizer_phone: '',
  editId: '',
  deleteId: ''
})
 
const toast = reactive({ show: false, type: 'success', message: '' })
 
function authHeaders() {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
}
 
function dateToISO(dateStr) {
  if (!dateStr) return null
  return new Date(dateStr + 'T00:00:00').toISOString()
}
 
function openModal(type) {
  resetAll()
  activeModal.value = type
}
 
function closeModal() {
  activeModal.value = null
  confirmConfig.value = null
  busy.value = false
  resetAll()
}
 
function resetAll() {
  Object.assign(form, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: null,
    organizer_name: '', organizer_email: '', organizer_phone: ''
  })
  Object.assign(errors, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: '',
    organizer_name: '', organizer_email: '', organizer_phone: '',
    editId: '', deleteId: ''
  })
  editId.value   = ''
  deleteId.value = ''
  editStep.value = 1
}
 
function validateCreate() {
  Object.assign(errors, {
    title: '', description: '', location: '',
    date: '', end_time: '', capacity: '',
    organizer_name: '', organizer_email: '', organizer_phone: ''
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
 
  if (!form.organizer_name.trim())
    { errors.organizer_name = 'Ime organizatora je obavezno.'; ok = false }
  if (!form.organizer_email.trim())
    { errors.organizer_email = 'Email organizatora je obavezan.'; ok = false }
 
  return ok
}
 
function askConfirm(action) {
  if (action === 'create' && !validateCreate()) return
  if (action === 'delete') {
    errors.deleteId = ''
  if (!deleteId.value) {
    errors.deleteId = 'Odaberi radionicu.'
    return
  }
}

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
 
async function runAction() {
  if (confirmConfig.value?.action) {
    await confirmConfig.value.action()
  }
}
 
async function doCreate() {
  busy.value = true
  try {
    const body = {
      title:       form.title.trim(),
      description: form.description.trim(),
      location:    form.location.trim(),
      date:        dateToISO(form.date),
      end_time:    dateToISO(form.end_time),
        capacity:    form.capacity,
        organizer_name: form.organizer_name.trim(),
        organizer_email: form.organizer_email.trim(),
        organizer_phone: form.organizer_phone.trim()
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
    confirmConfig.value = null
  } finally {
    busy.value = false
  }
}
 
async function loadWorkshop() {
  errors.editId = ''
  if (!editId.value) {
  errors.editId = 'Odaberi radionicu.'
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
    const w = await res.json()
 
    Object.assign(form, {
      title:       w.title       ?? '',
      description: w.description ?? '',
      location:    '',
      date:        w.date     ? w.date.slice(0, 10)     : '',
      end_time:    w.end_time ? w.end_time.slice(0, 10) : '',
      capacity:    w.capacity ?? null,
      organizer_name: w.organizer_name ?? '',
      organizer_email: w.organizer_email ?? '',
      organizer_phone: w.organizer_phone ?? ''
    })
    editStep.value = 2
  } catch {
    errors.editId = 'Greška pri učitavanju. Provjeri server.'
  } finally {
    busy.value = false
  }
}
 
async function doEdit() {
  busy.value = true
  try {
    const body = {}
    if (form.title.trim())       body.title       = form.title.trim()
    if (form.description.trim()) body.description = form.description.trim()
    if (form.location.trim())    body.location    = form.location.trim()
    if (form.date)               body.date        = dateToISO(form.date)
    if (form.end_time)           body.end_time    = dateToISO(form.end_time)
    if (form.capacity)           body.capacity    = form.capacity
      if (form.organizer_name && form.organizer_name.trim()) body.organizer_name = form.organizer_name.trim()
      if (form.organizer_email && form.organizer_email.trim()) body.organizer_email = form.organizer_email.trim()
      if (form.organizer_phone && form.organizer_phone.trim()) body.organizer_phone = form.organizer_phone.trim()
 
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
 
function showToast(type, message) {
  toast.show = false
  setTimeout(() => {
    Object.assign(toast, { show: true, type, message })
    setTimeout(() => { toast.show = false }, 3800)
  }, 40)
}

onMounted(async () => {
  const res = await fetch(`${BASE_URL}/workshops/active`)
  workshops.value = await res.json()
})
 
// ================================================================
// PREGLED PRIJAVLJENIH
// ================================================================
 
const workshops          = ref([])
const registrations      = ref([])
const selectedWorkshopId = ref('')
const registrationsLoading = ref(false)
const registrationsError   = ref(null)
 
function getAuthHeaders() {
  const token = localStorage.getItem('token')
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}
 
async function loadWorkshops() {
  try {
    registrationsLoading.value = true
    registrationsError.value = null
    const response = await fetch(`${BASE_URL}/workshops/active`)
    workshops.value = await response.json()
  } catch (err) {
    registrationsError.value = 'Greška pri učitavanju radionica: ' + err.message
    console.error(err)
  } finally {
    registrationsLoading.value = false
  }
}
 
async function loadRegistrations() {
  if (!selectedWorkshopId.value) {
    registrations.value = []
    return
  }
 
  try {
    registrationsLoading.value = true
    registrationsError.value = null
    const response = await fetch(
      `${BASE_URL}/workshops/${selectedWorkshopId.value}/registrations`,
      { headers: getAuthHeaders() }
    )
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Greška pri učitavanju prijava')
    }
    registrations.value = await response.json()
  } catch (err) {
    registrationsError.value = 'Greška pri učitavanju prijava: ' + err.message
    console.error(err)
    registrations.value = []
  } finally {
    registrationsLoading.value = false
  }
}
 
// ================================================================
// PRIJEDLOZI
// ================================================================
 
const proposals          = ref([])
const proposalsLoading   = ref(false)
const activeFilter       = ref('all')
const detailProposal     = ref(null)
const actionMode         = ref(null)
const actionNote         = ref('')
const createWorkshop     = ref(false)
const proposalConfirmConfig = ref(null)
const proposalBusy       = ref(false)
 
const workshopForm   = reactive({ location: '', date: '', end_time: '', capacity: null, organizer_name: '', organizer_email: '', organizer_phone: '' })
const workshopErrors = reactive({ location: '', date: '', end_time: '', capacity: '', organizer_name: '', organizer_email: '' })
const proposalToast  = reactive({ show: false, type: 'success', message: '' })
 
const filters = [
  { value: 'all',      label: 'Svi' },
  { value: 'pending',  label: 'Na čekanju' },
  { value: 'accepted', label: 'Odobreni' },
  { value: 'rejected', label: 'Odbijeni' },
]
 
const filteredProposals = computed(() => {
  if (activeFilter.value === 'all') return proposals.value
  return proposals.value.filter(p => p.status === activeFilter.value)
})
 
async function fetchProposals() {
  proposalsLoading.value = true
  try {
    const res = await fetch(`${BASE_URL}/workshops/admin`, { headers: authHeaders() })
    if (!res.ok) throw new Error(`Greška ${res.status}`)
    proposals.value = await res.json()
  } catch (e) {
    showProposalToast('error', e.message || 'Greška pri učitavanju prijedloga.')
  } finally {
    proposalsLoading.value = false
  }
}
 
async function doApprove() {
  proposalBusy.value = true
  busy.value = true
  try {
    const body = {
      admin_note:      actionNote.value.trim() || null,
      create_workshop: createWorkshop.value,
    }
    if (createWorkshop.value) {
      body.location  = workshopForm.location.trim()
      body.date      = dateToISO(workshopForm.date)
      body.end_time  = dateToISO(workshopForm.end_time)
      body.capacity  = workshopForm.capacity
       body.organizer_name  = workshopForm.organizer_name.trim()
      body.organizer_email = workshopForm.organizer_email.trim()
      body.organizer_phone = workshopForm.organizer_phone.trim() || null
    }
    const res = await fetch(
      `${BASE_URL}/workshops/proposals/${detailProposal.value.id}/approve`,
      { method: 'PATCH', headers: authHeaders(), body: JSON.stringify(body) }
    )
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    const updated = await res.json()
    const idx = proposals.value.findIndex(p => p.id === updated.id)
    if (idx !== -1) proposals.value[idx] = updated
    showProposalToast('success', createWorkshop.value ? 'Prijedlog odobren i radionica kreirana!' : 'Prijedlog uspješno odobren!')
    closeDetail()
  } catch (e) {
    showProposalToast('error', e.message || 'Odobravanje nije uspjelo.')
    proposalConfirmConfig.value = null
  } finally {
    proposalBusy.value = false
    busy.value = false
  }
}
 
async function doReject() {
  proposalBusy.value = true
  busy.value = true
  try {
    const body = { admin_note: actionNote.value.trim() || null }
    const res = await fetch(
      `${BASE_URL}/workshops/proposals/${detailProposal.value.id}/reject`,
      { method: 'PATCH', headers: authHeaders(), body: JSON.stringify(body) }
    )
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    const updated = await res.json()
    const idx = proposals.value.findIndex(p => p.id === updated.id)
    if (idx !== -1) proposals.value[idx] = updated
    showProposalToast('success', 'Prijedlog odbijen.')
    closeDetail()
  } catch (e) {
    showProposalToast('error', e.message || 'Odbijanje nije uspjelo.')
    proposalConfirmConfig.value = null
  } finally {
    proposalBusy.value = false
    busy.value = false
  }
}
 
function setFilter(val) {
  activeFilter.value = val
}
 
function countFor(filterVal) {
  if (filterVal === 'all') return proposals.value.length
  return proposals.value.filter(p => p.status === filterVal).length
}
 
function truncate(str, n) {
  return str && str.length > n ? str.slice(0, n) + '…' : str
}
 
function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('bs-BA', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
 
function statusLabel(s) {
  return { pending: 'Na čekanju', accepted: 'Odobreno', rejected: 'Odbijeno' }[s] ?? s
}
 
function openDetail(p) {
  detailProposal.value = { ...p }
  actionMode.value = null
  actionNote.value = ''
  createWorkshop.value = false
  Object.assign(workshopForm, { location: '', date: '', end_time: '', capacity: null, organizer_name: '', organizer_email: '', organizer_phone: '' })
Object.assign(workshopErrors, { location: '', date: '', end_time: '', capacity: '', organizer_name: '', organizer_email: '' })
}
 
function closeDetail() {
  detailProposal.value = null
  proposalConfirmConfig.value  = null
  actionMode.value     = null
  actionNote.value     = ''
  createWorkshop.value = false
  proposalBusy.value = false
  busy.value = false
}
 
function validateWorkshopForm() {
  Object.assign(workshopErrors, { location: '', date: '', end_time: '', capacity: '' })
  let ok = true
  if (!workshopForm.location.trim())    { workshopErrors.location = 'Obavezno.'; ok = false }
  if (!workshopForm.date)               { workshopErrors.date = 'Obavezno.'; ok = false }
  if (!workshopForm.end_time)           { workshopErrors.end_time = 'Obavezno.'; ok = false }
  if (!workshopForm.capacity || workshopForm.capacity < 1) { workshopErrors.capacity = 'Mora biti ≥ 1.'; ok = false }
  if (workshopForm.date && workshopForm.end_time && workshopForm.date > workshopForm.end_time)
    { workshopErrors.end_time = 'Kraj mora biti nakon početka.'; ok = false }
  if (!workshopForm.organizer_name.trim())  { workshopErrors.organizer_name = 'Obavezno.'; ok = false }
  if (!workshopForm.organizer_email.trim()) { workshopErrors.organizer_email = 'Obavezno.'; ok = false }
  return ok
}
 
function askConfirmAction(type) {
  if (type === 'approve' && createWorkshop.value && !validateWorkshopForm()) return
  const cfgs = {
    approve: {
      title:     'Potvrdi odobravanje',
      message:   createWorkshop.value
        ? `Odobrit ćeš prijedlog „${detailProposal.value.title}" i kreirati radionicu.`
        : `Odobrit ćeš prijedlog „${detailProposal.value.title}".`,
      btnLabel:  'Da, odobri',
      btnClass:  'btn-create',
      iconClass: 'icon-create',
      action:    doApprove,
    },
    reject: {
      title:     'Potvrdi odbijanje',
      message:   `Odbit ćeš prijedlog „${detailProposal.value.title}". Autorici će biti vidljiv status.`,
      btnLabel:  'Da, odbij',
      btnClass:  'btn-delete',
      iconClass: 'icon-delete',
      action:    doReject,
    },
  }
  proposalConfirmConfig.value = cfgs[type]
}
 
async function runProposalAction() {
  if (proposalConfirmConfig.value?.action) await proposalConfirmConfig.value.action()
}
 
function showProposalToast(type, message) {
  proposalToast.show = false
  setTimeout(() => {
    Object.assign(proposalToast, { show: true, type, message })
    setTimeout(() => { proposalToast.show = false }, 3800)
  }, 40)
}
  
onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    // redirect to login if needed — handled by router guard
    return
  }
  loadWorkshops()
  fetchProposals()
})
</script>

<style scoped>
/* ================================================================
   Naslovi koji dijele tri sekcije
   ================================================================ */
.combined-admin-page {
  font-family: 'Segoe UI', system-ui, sans-serif;
}
 
.section-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2.5rem 2rem 0;
  max-width: 860px;
  margin: 0 auto;
}
 
.section-divider-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, #ede9fe, #ddd6fe);
  border-radius: 2px;
}
 
.section-divider-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #ede9fe;
  color: #7c3aed;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 6px 16px;
  border-radius: 20px;
  border: 1.5px solid #ddd6fe;
  white-space: nowrap;
}
 
/* ================================================================
   LAYOUT STRANICE
   ================================================================ */
.admin-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem 2rem 5rem;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
 
/* Naslov stranice */
.page-header { text-align: center; margin-bottom: 3rem; }
 
.admin-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: #ede9fe; color: #7c3aed;
  font-size: 0.68rem; font-weight: 800;
  letter-spacing: .09em; text-transform: uppercase;
  padding: 4px 12px; border-radius: 20px; margin-bottom: 1rem;
  border: 1.5px solid #ddd6fe;
}
 
.page-header h1 {
  font-size: 1.75rem; font-weight: 800;
  color: #1e1b4b; margin: 0 0 0.4rem;
}
 
.page-sub { color: #9ca3af; font-size: 0.88rem; margin: 0; }
 
/* ================================================================
   TRI KARTICE (glavni ekran)
   ================================================================ */
.actions-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}
 
.action-card {
  display: flex; flex-direction: column; align-items: center;
  gap: 0.8rem; padding: 2.25rem 1.25rem;
  border-radius: 18px; border: 2px solid transparent;
  cursor: pointer; text-align: center; background: #fff;
  transition: transform .18s, box-shadow .18s, border-color .18s;
}
.action-card:hover { transform: translateY(-5px); }
 
.card-icon {
  width: 66px; height: 66px; border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: transform .18s;
}
.action-card:hover .card-icon { transform: scale(1.08); }
 
.card-label { font-size: 1rem; font-weight: 800; color: #1e1b4b; }
.card-hint  { font-size: 0.77rem; color: #9ca3af; line-height: 1.45; }
 
/* Kartica Kreiraj — lila */
.card-create { box-shadow: 0 2px 16px rgba(124,58,237,.1); }
.card-create:hover { border-color: #7c3aed; box-shadow: 0 8px 28px rgba(124,58,237,.18); }
.card-create .card-icon { background: #ede9fe; color: #7c3aed; }
 
/* Kartica Uredi — žuta */
.card-edit { box-shadow: 0 2px 16px rgba(217,119,6,.08); }
.card-edit:hover { border-color: #d97706; box-shadow: 0 8px 28px rgba(217,119,6,.18); }
.card-edit .card-icon { background: #fef3c7; color: #d97706; }
 
/* Kartica Obriši — crvena */
.card-delete { box-shadow: 0 2px 16px rgba(220,38,38,.07); }
.card-delete:hover { border-color: #dc2626; box-shadow: 0 8px 28px rgba(220,38,38,.15); }
.card-delete .card-icon { background: #fee2e2; color: #dc2626; }
 
/* ================================================================
   OVERLAY I MODALI
   ================================================================ */
.overlay {
  position: fixed; inset: 0; z-index: 40;
  background: rgba(15, 10, 40, .52);
  backdrop-filter: blur(5px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem;
  animation: fade-in .15s ease;
}
.overlay-top { z-index: 50; }
 
@keyframes fade-in { from { opacity: 0 } to { opacity: 1 } }
 
.modal {
  background: #fff; border-radius: 20px;
  width: 100%; max-width: 560px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, .22);
  animation: slide-up .2s ease; overflow: hidden;
}
.modal-narrow  { max-width: 440px; }
.modal-detail  { max-width: 600px; }
 
@keyframes slide-up {
  from { opacity: 0; transform: translateY(22px) }
  to   { opacity: 1; transform: translateY(0) }
}
 
.modal-head {
  display: flex; align-items: center; gap: 0.9rem;
  padding: 1.4rem 1.5rem 1.2rem;
  border-bottom: 1px solid #f3f4f6;
}
.modal-head h2 { font-size: 1rem; font-weight: 800; color: #1e1b4b; margin: 0 0 2px; }
.modal-head p  { font-size: 0.77rem; color: #9ca3af; margin: 0; }
 
.mh-icon {
  width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.head-create   .mh-icon { background: #ede9fe; color: #7c3aed; }
.head-edit     .mh-icon { background: #fef3c7; color: #d97706; }
.head-delete   .mh-icon { background: #fee2e2; color: #dc2626; }
.head-pending  .mh-icon { background: #fef3c7; color: #d97706; }
.head-accepted .mh-icon { background: #d1fae5; color: #059669; }
.head-rejected .mh-icon { background: #fee2e2; color: #dc2626; }
 
.close-btn {
  margin-left: auto; background: #f9fafb; border: 1.5px solid #f3f4f6;
  width: 30px; height: 30px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #9ca3af; font-size: 0.9rem;
  transition: background .15s;
}
.close-btn:hover { background: #f3f4f6; color: #374151; }
 
.modal-body {
  padding: 1.25rem 1.5rem;
  display: flex; flex-direction: column; gap: 1rem;
  max-height: 70vh; overflow-y: auto;
}
 
.modal-foot {
  padding: 1rem 1.5rem 1.4rem;
  display: flex; justify-content: flex-end; gap: 0.75rem;
  border-top: 1px solid #f3f4f6;
}
 
/* ================================================================
   FORMA — polja za unos podataka
   ================================================================ */
.field-row   { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field       { display: flex; flex-direction: column; gap: 4px; }
.field-narrow { max-width: 150px; }
 
.field label { font-size: 0.77rem; font-weight: 700; color: #374151; }
.req { color: #dc2626; }
 
.field input,
.fiels select,
.field textarea {
  background: #fafafa; border: 1.5px solid #e5e7eb;
  border-radius: 10px; padding: 0.48rem 0.7rem;
  font-size: 0.86rem; color: #111827; outline: none;
  transition: border-color .15s, box-shadow .15s;
  font-family: inherit;
}
.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, .1);
}
.field textarea { resize: vertical; min-height: 76px; }

.field select {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239ca3af' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  padding-right: 2rem;
  cursor: pointer;
} 
.input-error { border-color: #dc2626 !important; }
.err-msg { font-size: 0.71rem; color: #dc2626; font-weight: 600; }
 
.hint-text { font-size: 0.77rem; color: #9ca3af; margin: 0; }
 
.loaded-label {
  font-size: 0.77rem; color: #7c3aed; font-weight: 700;
  background: #ede9fe; padding: 6px 10px; border-radius: 8px; margin: 0;
}
 
/* ================================================================
   UPOZORENJE ZA BRISANJE
   ================================================================ */
.danger-notice {
  display: flex; align-items: center; gap: 8px;
  background: #fef2f2; border: 1.5px solid #fecaca;
  border-radius: 10px; padding: 0.65rem 0.9rem;
  font-size: 0.8rem; font-weight: 600; color: #991b1b;
}
 
/* ================================================================
   POTVRDNI PROZOR
   ================================================================ */
.confirm-modal {
  padding: 2rem; text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
}
 
.confirm-icon {
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.icon-create { background: #ede9fe; color: #7c3aed; }
.icon-edit   { background: #fef3c7; color: #d97706; }
.icon-delete { background: #fee2e2; color: #dc2626; }
 
.confirm-title { font-size: 1.05rem; font-weight: 800; color: #1e1b4b; margin: 0; }
.confirm-msg   { font-size: 0.85rem; color: #6b7280; line-height: 1.6; margin: 0; }
.confirm-actions { display: flex; gap: 0.75rem; margin-top: 0.5rem; }
 
/* ================================================================
   DUGMAD
   ================================================================ */
.btn-secondary,
.btn-create,
.btn-edit,
.btn-delete {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0.5rem 1.2rem; border-radius: 10px;
  font-size: 0.84rem; font-weight: 700; cursor: pointer;
  border: none; transition: opacity .15s, transform .12s;
}
.btn-create:hover, .btn-edit:hover, .btn-delete:hover { transform: translateY(-1px); }
.btn-create:disabled, .btn-edit:disabled,
.btn-delete:disabled, .btn-secondary:disabled {
  opacity: .55; cursor: not-allowed; transform: none;
}
 
.btn-secondary { background: #f3f4f6; color: #6b7280; border: 1.5px solid #e5e7eb; }
.btn-secondary:hover { background: #e5e7eb; }
 
.btn-create {
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  color: #fff; box-shadow: 0 3px 10px rgba(124,58,237,.3);
}
.btn-edit {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #fff; box-shadow: 0 3px 10px rgba(245,158,11,.3);
}
.btn-delete {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #fff; box-shadow: 0 3px 10px rgba(239,68,68,.3);
}
 
/* ================================================================
   SPINNER
   ================================================================ */
.spin {
  display: inline-block; width: 13px; height: 13px;
  border: 2px solid rgba(255, 255, 255, .4);
  border-top-color: #fff; border-radius: 50%;
  animation: spin .65s linear infinite;
}
.spin-dark {
  border: 2px solid rgba(124,58,237,.2);
  border-top-color: #7c3aed;
}
@keyframes spin { to { transform: rotate(360deg) } }
 
/* ================================================================
   TOAST NOTIFIKACIJE
   ================================================================ */
.toast {
  position: fixed; bottom: 1.75rem; right: 1.75rem; z-index: 9999;
  display: flex; align-items: center; gap: 8px;
  padding: 0.7rem 1.2rem; border-radius: 12px;
  font-size: 0.85rem; font-weight: 600;
  box-shadow: 0 8px 24px rgba(0, 0, 0, .14);
}
.toast-success { background: #ecfdf5; color: #065f46; border: 1.5px solid #6ee7b7; }
.toast-error   { background: #fef2f2; color: #991b1b; border: 1.5px solid #fca5a5; }
 
.toast-enter-active, .toast-leave-active { transition: all .28s ease; }
.toast-enter-from { opacity: 0; transform: translateY(8px); }
.toast-leave-to   { opacity: 0; transform: translateY(-8px); }
 
/* ================================================================
   FILTER DUGMAD (Proposals sekcija)
   ================================================================ */
.filter-row {
  display: flex; gap: 0.6rem; flex-wrap: wrap;
  margin-bottom: 1.75rem;
}
.filter-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0.42rem 1rem; border-radius: 20px;
  font-size: 0.8rem; font-weight: 700; cursor: pointer;
  background: #fff; border: 1.5px solid #e5e7eb; color: #6b7280;
  transition: all .15s;
}
.filter-btn:hover { border-color: #d1d5db; color: #374151; }
.filter-btn.active { background: #1e1b4b; border-color: #1e1b4b; color: #fff; }
 
.filter-dot {
  width: 7px; height: 7px; border-radius: 50%;
}
.dot-all      { background: #9ca3af; }
.dot-pending  { background: #f59e0b; }
.dot-accepted { background: #10b981; }
.dot-rejected { background: #ef4444; }
 
.filter-count {
  background: rgba(0,0,0,.07); border-radius: 20px;
  padding: 1px 7px; font-size: 0.72rem; font-weight: 800;
}
.filter-btn.active .filter-count { background: rgba(255,255,255,.2); }
 
/* ================================================================
   LOADING / EMPTY STATE (Proposals sekcija)
   ================================================================ */
.loading-state, .empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 0.75rem; padding: 4rem 0;
  color: #9ca3af; font-size: 0.88rem;
}
.empty-icon {
  width: 60px; height: 60px; border-radius: 18px;
  background: #f9fafb; border: 1.5px solid #e5e7eb;
  display: flex; align-items: center; justify-content: center;
  color: #d1d5db;
}
 
/* ================================================================
   LISTA PRIJEDLOGA
   ================================================================ */
.proposals-list { display: flex; flex-direction: column; gap: 0.75rem; }
 
.proposal-card {
  background: #fff; border-radius: 16px;
  border: 1.5px solid #e5e7eb;
  padding: 1.25rem 1.4rem;
  display: flex; align-items: center; gap: 1rem;
  cursor: pointer;
  transition: transform .15s, box-shadow .15s, border-color .15s;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.proposal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,.09);
}
.card-pending:hover  { border-color: #f59e0b; }
.card-accepted:hover { border-color: #10b981; }
.card-rejected:hover { border-color: #ef4444; }
 
.card-left   { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 0.4rem; }
.card-arrow  { color: #d1d5db; flex-shrink: 0; }
 
.proposal-title {
  font-size: 0.97rem; font-weight: 800; color: #1e1b4b;
  margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.proposal-desc { font-size: 0.82rem; color: #6b7280; margin: 0; line-height: 1.5; }
 
.card-meta {
  display: flex; gap: 1.1rem; flex-wrap: wrap;
  font-size: 0.75rem; color: #9ca3af; margin-top: 2px;
}
.card-meta span { display: flex; align-items: center; gap: 4px; }
 
/* ================================================================
   STATUS BADGE
   ================================================================ */
.status-badge {
  display: inline-block;
  padding: 2px 10px; border-radius: 20px;
  font-size: 0.7rem; font-weight: 800; letter-spacing: .04em;
  text-transform: uppercase;
}
.badge-pending  { background: #fef3c7; color: #92400e; border: 1.5px solid #fde68a; }
.badge-accepted { background: #d1fae5; color: #065f46; border: 1.5px solid #6ee7b7; }
.badge-rejected { background: #fee2e2; color: #991b1b; border: 1.5px solid #fca5a5; }
 
/* ================================================================
   Polje detalja
   ================================================================ */
.detail-field { display: flex; flex-direction: column; gap: 3px; }
.detail-label {
  font-size: 0.71rem; font-weight: 700; color: #9ca3af;
  text-transform: uppercase; letter-spacing: .06em;
}
.detail-value { font-size: 0.9rem; color: #1e1b4b; font-weight: 500; }
.detail-desc  { line-height: 1.6; color: #374151; white-space: pre-wrap; }
 
.admin-note-box {
  background: #f0fdf4; border: 1.5px solid #bbf7d0;
  border-radius: 10px; padding: 0.75rem 1rem;
}
.note-label {
  display: block; font-size: 0.7rem; font-weight: 800;
  color: #059669; text-transform: uppercase;
  letter-spacing: .06em; margin-bottom: 4px;
}
.admin-note-box p { font-size: 0.85rem; color: #374151; margin: 0; }
 
/* ================================================================
   AKCIJE U DETALJNOM MODALU
   ================================================================ */
.action-divider {
  display: flex; align-items: center; gap: 0.75rem;
  font-size: 0.72rem; font-weight: 800; color: #9ca3af;
  text-transform: uppercase; letter-spacing: .07em;
  margin: 0.25rem 0;
}
.action-divider::before, .action-divider::after {
  content: ''; flex: 1; height: 1px; background: #f3f4f6;
}
 
.pending-actions {
  display: flex; gap: 0.75rem; justify-content: flex-end;
}
 
.action-form {
  display: flex; flex-direction: column; gap: 0.85rem;
  padding: 1rem; border-radius: 12px;
}
.action-form-approve { background: #f0fdf4; border: 1.5px solid #bbf7d0; }
.action-form-reject  { background: #fef2f2; border: 1.5px solid #fecaca; }
 
.form-actions { display: flex; gap: 0.6rem; justify-content: flex-end; }
 
/* Toggle switch */
.toggle-row { flex-direction: row; align-items: center; }
.toggle-label {
  display: flex; align-items: center; gap: 0.65rem;
  font-size: 0.84rem; font-weight: 600; color: #374151;
  cursor: pointer; user-select: none;
}
.toggle-input { display: none; }
.toggle-track {
  position: relative; width: 38px; height: 21px;
  background: #e5e7eb; border-radius: 20px;
  transition: background .2s; flex-shrink: 0;
}
.toggle-input:checked + .toggle-track { background: #7c3aed; }
.toggle-thumb {
  position: absolute; top: 3px; left: 3px;
  width: 15px; height: 15px; border-radius: 50%;
  background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,.2);
  transition: left .2s;
}
.toggle-input:checked ~ .toggle-track .toggle-thumb { left: 20px; }
/* ================================================================
   WORKSHOP SELECT
   ================================================================ */
.workshop-select {
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
  background: #fafafa;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.55rem 2.5rem 0.55rem 0.85rem;
  font-size: 0.86rem;
  color: #111827;
  outline: none;
  cursor: pointer;
  font-family: inherit;
  transition: border-color .15s, box-shadow .15s;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%237c3aed' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.workshop-select:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, .1);
}

.workshop-select option:disabled {
  color: #9ca3af;
}

</style>
 