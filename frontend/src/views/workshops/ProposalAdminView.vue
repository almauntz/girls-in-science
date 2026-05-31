<template>
  <div class="admin-page">
 
    <!-- ── Naslov stranice ── -->
    <div class="page-header">
      <span class="admin-tag">Admin panel</span>
      <h1>Prijedlozi radionica</h1>
      <p class="page-sub">Pregled i obrada prijedloga od studentica</p>
    </div>
 
    <!-- ── Filter dugmad ── -->
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
 
    <!-- ── Loading state ── -->
    <div v-if="loading" class="loading-state">
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
      <div v-if="confirmConfig" class="overlay overlay-top" @click.self="confirmConfig = null">
        <div class="modal modal-narrow confirm-modal">
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
            <button class="btn-secondary" @click="confirmConfig = null" :disabled="busy">Odustani</button>
            <button :class="confirmConfig.btnClass" @click="runAction" :disabled="busy">
              <span v-if="busy" class="spin"></span>
              {{ busy ? 'U toku…' : confirmConfig.btnLabel }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
 
    <!-- ── Toast notifikacije ── -->
    <Transition name="toast">
      <div v-if="toast.show" class="toast" :class="`toast-${toast.type}`">
        <svg v-if="toast.type === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
        {{ toast.message }}
      </div>
    </Transition>
 
  </div>
</template>