<template>
  <div class="proposals-page">
 
    <!-- ── Naslov stranice ── -->
    <div class="page-header">
      <span class="member-tag">Moji prijedlozi</span>
      <h1>Predloži radionicu</h1>
      <p class="page-sub">Imaš ideju za radionicu? Pošalji prijedlog i pratiti ćemo ga zajedno.</p>
    </div>
 
    <!-- ── Dvije kolone: forma lijevo, lista desno ── -->
    <div class="layout">
 
      <!-- ── LIJEVO: forma za novi prijedlog ── -->
      <div class="form-panel">
        <div class="panel-head">
          <div class="panel-icon icon-purple">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </div>
          <div>
            <h2>Novi prijedlog</h2>
            <p>Popuni naziv i opis radionice</p>
          </div>
        </div>
 
        <div class="form-body">
          <div class="field">
            <label>Naziv radionice <span class="req">*</span></label>
            <input
              v-model="form.title"
              type="text"
              placeholder="npr. Uvod u machine learning"
              :class="{ 'input-error': errors.title }"
              :disabled="submitting"
            />
            <span v-if="errors.title" class="err-msg">{{ errors.title }}</span>
          </div>
 
          <div class="field">
            <label>Opis <span class="req">*</span></label>
            <textarea
              v-model="form.description"
              rows="5"
              placeholder="Opiši o čemu bi radionica bila, šta bi polaznice naučile, zašto smatraš da bi bila korisna…"
              :class="{ 'input-error': errors.description }"
              :disabled="submitting"
            ></textarea>
            <span v-if="errors.description" class="err-msg">{{ errors.description }}</span>
            <span class="char-count" :class="{ 'count-warn': form.description.length > 480 }">
              {{ form.description.length }} / 500
            </span>
          </div>
 
          <button class="btn-submit" @click="submitProposal" :disabled="submitting">
            <span v-if="submitting" class="spin"></span>
            <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            {{ submitting ? 'Slanje…' : 'Pošalji prijedlog' }}
          </button>
        </div>
      </div>
 
      <!-- ── DESNO: lista mojih prijedloga ── -->
      <div class="list-panel">
        <div class="panel-head">
          <div class="panel-icon icon-dark">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
          </div>
          <div>
            <h2>Moji prijedlozi</h2>
            <p>Historija tvojih prijedloga</p>
          </div>
        </div>
 
        <!-- Loading -->
        <div v-if="loading" class="list-state">
          <span class="spin spin-dark"></span>
          <span>Učitavanje…</span>
        </div>
 
        <!-- Prazno -->
        <div v-else-if="proposals.length === 0" class="list-state empty">
          <div class="empty-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <p>Još nisi poslala nijedan prijedlog.</p>
          <span>Popuni formu s lijeve strane!</span>
        </div>
 
        <!-- Lista -->
        <div v-else class="my-proposals-list">
          <div
            v-for="p in proposals"
            :key="p.id"
            class="my-proposal-card"
            :class="`card-${p.status}`"
            @click="openDetail(p)"
          >
            <div class="mpc-top">
              <span class="status-badge" :class="`badge-${p.status}`">
                <span class="badge-dot"></span>
                {{ statusLabel(p.status) }}
              </span>
              <span class="mpc-date">{{ formatDate(p.created_at) }}</span>
            </div>
            <h3 class="mpc-title">{{ p.title }}</h3>
            <p class="mpc-desc">{{ truncate(p.description, 90) }}</p>
 
            <!-- Admin nota (ako postoji i nije pending) -->
            <div v-if="p.admin_note && p.status !== 'pending'" class="mpc-note">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              {{ truncate(p.admin_note, 70) }}
            </div>
          </div>
        </div>
      </div>
 
    </div><!-- /.layout -->
 
    <!-- ── Modal: detalj prijedloga ── -->
    <Teleport to="body">
      <div v-if="detailProposal" class="overlay" @click.self="detailProposal = null">
        <div class="modal">
 
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
                  <span class="badge-dot"></span>
                  {{ statusLabel(detailProposal.status) }}
                </span>
              </p>
            </div>
            <button class="close-btn" @click="detailProposal = null">&#x2715;</button>
          </div>
 
          <div class="modal-body">
            <div class="detail-field">
              <span class="detail-label">Naziv</span>
              <span class="detail-value">{{ detailProposal.title }}</span>
            </div>
            <div class="detail-field">
              <span class="detail-label">Opis</span>
              <span class="detail-value detail-desc">{{ detailProposal.description }}</span>
            </div>
            <div class="detail-field">
              <span class="detail-label">Datum prijedloga</span>
              <span class="detail-value">{{ formatDate(detailProposal.created_at) }}</span>
            </div>
 
            <!-- Status objašnjenje -->
            <div class="status-info" :class="`info-${detailProposal.status}`">
              <div class="si-icon">
                <!-- Pending: sat -->
                <svg v-if="detailProposal.status === 'pending'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                <!-- Accepted: kuka -->
                <svg v-else-if="detailProposal.status === 'accepted'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                <!-- Rejected: X -->
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </div>
              <div>
                <p class="si-title">{{ statusInfoTitle(detailProposal.status) }}</p>
                <p class="si-msg">{{ statusInfoMsg(detailProposal.status) }}</p>
              </div>
            </div>
 
            <!-- Admin nota -->
            <div v-if="detailProposal.admin_note" class="admin-note-box">
              <span class="note-label">Napomena admina</span>
              <p>{{ detailProposal.admin_note }}</p>
            </div>
          </div>
 
          <div class="modal-foot">
            <button class="btn-secondary" @click="detailProposal = null">Zatvori</button>
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