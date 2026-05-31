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

<script setup>
import { ref, reactive, onMounted } from 'vue'
 
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
 
// ── State ──────────────────────────────────────────────────────────────────
 
const proposals      = ref([])
const loading        = ref(false)
const submitting     = ref(false)
const detailProposal = ref(null)
 
const form = reactive({ title: '', description: '' })
const errors = reactive({ title: '', description: '' })
const toast = reactive({ show: false, type: 'success', message: '' })
 
// ── Lifecycle ──────────────────────────────────────────────────────────────
 
onMounted(() => fetchMyProposals())
 
// ── API ────────────────────────────────────────────────────────────────────
 
function authHeaders() {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
}
 
async function fetchMyProposals() {
  loading.value = true
  try {
    const res = await fetch(`${BASE_URL}/workshops/proposals/my`, { headers: authHeaders() })
    if (!res.ok) throw new Error(`Greška ${res.status}`)
    proposals.value = await res.json()
  } catch (e) {
    showToast('error', e.message || 'Greška pri učitavanju prijedloga.')
  } finally {
    loading.value = false
  }
}
 
async function submitProposal() {
  if (!validateForm()) return
  submitting.value = true
  try {
    const body = {
      title:       form.title.trim(),
      description: form.description.trim(),
    }
    const res = await fetch(`${BASE_URL}/workshops/proposals`, {
      method:  'POST',
      headers: authHeaders(),
      body:    JSON.stringify(body),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Greška ${res.status}`)
    }
    const created = await res.json()
    proposals.value.unshift(created)   // dodaj na vrh liste odmah
    Object.assign(form, { title: '', description: '' })
    showToast('success', 'Prijedlog uspješno poslan! Pratiti ćemo status zajedno.')
  } catch (e) {
    showToast('error', e.message || 'Slanje nije uspjelo.')
  } finally {
    submitting.value = false
  }
}
 
// ── Helpers ────────────────────────────────────────────────────────────────
 
function validateForm() {
  Object.assign(errors, { title: '', description: '' })
  let ok = true
  if (!form.title.trim())
    { errors.title = 'Naziv je obavezan.'; ok = false }
  if (!form.description.trim())
    { errors.description = 'Opis je obavezan.'; ok = false }
  else if (form.description.length > 500)
    { errors.description = 'Opis ne smije biti duži od 500 znakova.'; ok = false }
  return ok
}
 
function openDetail(p) {
  detailProposal.value = { ...p }
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
 
function statusInfoTitle(s) {
  return {
    pending:  'Prijedlog je primljen',
    accepted: 'Prijedlog je odobren!',
    rejected: 'Prijedlog nije prihvaćen',
  }[s] ?? ''
}
 
function statusInfoMsg(s) {
  return {
    pending:  'Admin tima još uvijek pregledava tvoj prijedlog. Javit ćemo ti čim bude obrađen.',
    accepted: 'Odlična vijest! Admin je odobrio tvoj prijedlog. Pratite platformu za detalje.',
    rejected: 'Nažalost, ovaj prijedlog nije prihvaćen. Pogledaj napomenu admina ispod za više informacija.',
  }[s] ?? ''
}
 
function showToast(type, message) {
  toast.show = false
  setTimeout(() => {
    Object.assign(toast, { show: true, type, message })
    setTimeout(() => { toast.show = false }, 3800)
  }, 40)
}
</script>

<style scoped>
/* ================================================================
   LAYOUT STRANICE
   ================================================================ */
.proposals-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 3rem 2rem 5rem;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
 
.page-header { text-align: center; margin-bottom: 2.75rem; }
 
.member-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: #ede9fe; color: #7c3aed;
  font-size: 0.68rem; font-weight: 800;
  letter-spacing: .09em; text-transform: uppercase;
  padding: 4px 12px; border-radius: 20px; margin-bottom: 1rem;
  border: 1.5px solid #ddd6fe;
}
.page-header h1 { font-size: 1.75rem; font-weight: 800; color: #1e1b4b; margin: 0 0 0.4rem; }
.page-sub       { color: #9ca3af; font-size: 0.88rem; margin: 0; }
 
/* ── Dvije kolone ── */
.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}
@media (max-width: 680px) {
  .layout { grid-template-columns: 1fr; }
}
 
/* ================================================================
   PANELI (forma i lista)
   ================================================================ */
.form-panel,
.list-panel {
  background: #fff;
  border-radius: 20px;
  border: 1.5px solid #e5e7eb;
  box-shadow: 0 4px 20px rgba(0,0,0,.05);
  overflow: hidden;
}
 
.panel-head {
  display: flex; align-items: center; gap: 0.9rem;
  padding: 1.3rem 1.5rem 1.1rem;
  border-bottom: 1px solid #f3f4f6;
}
.panel-head h2 { font-size: 0.97rem; font-weight: 800; color: #1e1b4b; margin: 0 0 2px; }
.panel-head p  { font-size: 0.77rem; color: #9ca3af; margin: 0; }
 
.panel-icon {
  width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.icon-purple { background: #ede9fe; color: #7c3aed; }
.icon-dark   { background: #f3f4f6; color: #374151; }
 
/* ================================================================
   FORMA ZA PRIJEDLOG
   ================================================================ */
.form-body {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex; flex-direction: column; gap: 1rem;
}
 
.field       { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 0.77rem; font-weight: 700; color: #374151; }
.req         { color: #dc2626; }
 
.field input,
.field textarea {
  background: #fafafa; border: 1.5px solid #e5e7eb;
  border-radius: 10px; padding: 0.48rem 0.7rem;
  font-size: 0.86rem; color: #111827; outline: none;
  transition: border-color .15s, box-shadow .15s;
  font-family: inherit;
}
.field input:focus,
.field textarea:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, .1);
}
.field input:disabled,
.field textarea:disabled { opacity: .6; cursor: not-allowed; }
.field textarea { resize: vertical; min-height: 120px; }
 
.input-error { border-color: #dc2626 !important; }
.err-msg     { font-size: 0.71rem; color: #dc2626; font-weight: 600; }
 
.char-count {
  font-size: 0.71rem; color: #9ca3af; text-align: right;
  font-weight: 600;
}
.count-warn { color: #ef4444; }
 
.btn-submit {
  display: inline-flex; align-items: center; justify-content: center; gap: 7px;
  padding: 0.6rem 1.4rem; border-radius: 12px;
  font-size: 0.88rem; font-weight: 700; cursor: pointer;
  border: none;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  color: #fff; box-shadow: 0 4px 14px rgba(124,58,237,.35);
  transition: opacity .15s, transform .12s;
  align-self: flex-end;
}
.btn-submit:hover   { transform: translateY(-1px); }
.btn-submit:disabled { opacity: .55; cursor: not-allowed; transform: none; }
 
/* ================================================================
   LISTA MOJIH PRIJEDLOGA
   ================================================================ */
.list-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 0.6rem; padding: 3rem 1.5rem;
  color: #9ca3af; font-size: 0.85rem;
}
.list-state.empty span { font-size: 0.78rem; }
 
.empty-icon {
  width: 52px; height: 52px; border-radius: 16px;
  background: #f9fafb; border: 1.5px solid #e5e7eb;
  display: flex; align-items: center; justify-content: center;
  color: #d1d5db;
}
 
.my-proposals-list {
  padding: 0.75rem;
  display: flex; flex-direction: column; gap: 0.6rem;
  max-height: 520px; overflow-y: auto;
}
 
.my-proposal-card {
  background: #fafafa; border: 1.5px solid #e5e7eb;
  border-radius: 14px; padding: 1rem 1.1rem;
  cursor: pointer;
  transition: transform .14s, box-shadow .14s, border-color .14s;
}
.my-proposal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,.08);
}
.card-pending:hover  { border-color: #f59e0b; }
.card-accepted:hover { border-color: #10b981; }
.card-rejected:hover { border-color: #ef4444; }
 
.mpc-top {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 0.5rem;
}
.mpc-date { font-size: 0.72rem; color: #9ca3af; font-weight: 600; }
 
.mpc-title {
  font-size: 0.92rem; font-weight: 800; color: #1e1b4b;
  margin: 0 0 0.3rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.mpc-desc {
  font-size: 0.8rem; color: #6b7280; margin: 0;
  line-height: 1.5;
}
 
.mpc-note {
  display: flex; align-items: flex-start; gap: 5px;
  margin-top: 0.5rem; padding: 0.45rem 0.6rem;
  background: #f0fdf4; border-radius: 8px;
  font-size: 0.76rem; color: #059669; font-weight: 600;
  line-height: 1.4;
}
.card-rejected .mpc-note {
  background: #fef2f2; color: #dc2626;
}
 
/* ================================================================
   STATUS BADGE
   ================================================================ */
.status-badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 2px 10px; border-radius: 20px;
  font-size: 0.7rem; font-weight: 800;
  letter-spacing: .04em; text-transform: uppercase;
}
.badge-dot {
  width: 6px; height: 6px; border-radius: 50; flex-shrink: 0;
}
.badge-pending  { background: #fef3c7; color: #92400e; border: 1.5px solid #fde68a; }
.badge-pending  .badge-dot { background: #f59e0b; border-radius: 50%; }
.badge-accepted { background: #d1fae5; color: #065f46; border: 1.5px solid #6ee7b7; }
.badge-accepted .badge-dot { background: #10b981; border-radius: 50%; }
.badge-rejected { background: #fee2e2; color: #991b1b; border: 1.5px solid #fca5a5; }
.badge-rejected .badge-dot { background: #ef4444; border-radius: 50%; }
 
/* ================================================================
   OVERLAY I MODAL
   ================================================================ */
.overlay {
  position: fixed; inset: 0; z-index: 40;
  background: rgba(15, 10, 40, .52);
  backdrop-filter: blur(5px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem;
  animation: fade-in .15s ease;
}
@keyframes fade-in { from { opacity: 0 } to { opacity: 1 } }
 
.modal {
  background: #fff; border-radius: 20px;
  width: 100%; max-width: 520px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, .22);
  animation: slide-up .2s ease; overflow: hidden;
}
@keyframes slide-up {
  from { opacity: 0; transform: translateY(22px) }
  to   { opacity: 1; transform: translateY(0) }
}
 
.modal-head {
  display: flex; align-items: center; gap: 0.9rem;
  padding: 1.4rem 1.5rem 1.2rem;
  border-bottom: 1px solid #f3f4f6;
}
.modal-head h2 { font-size: 1rem; font-weight: 800; color: #1e1b4b; margin: 0 0 4px; }
.modal-head p  { margin: 0; }
 
.mh-icon {
  width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
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
  max-height: 65vh; overflow-y: auto;
}
 
.modal-foot {
  padding: 1rem 1.5rem 1.4rem;
  display: flex; justify-content: flex-end;
  border-top: 1px solid #f3f4f6;
}
 
/* ================================================================
   DETALJI U MODALU
   ================================================================ */
.detail-field { display: flex; flex-direction: column; gap: 3px; }
.detail-label {
  font-size: 0.71rem; font-weight: 700; color: #9ca3af;
  text-transform: uppercase; letter-spacing: .06em;
}
.detail-value { font-size: 0.9rem; color: #1e1b4b; font-weight: 500; }
.detail-desc  { line-height: 1.6; color: #374151; white-space: pre-wrap; }
 
/* Status info box */
.status-info {
  display: flex; align-items: flex-start; gap: 0.75rem;
  padding: 0.85rem 1rem; border-radius: 12px;
}
.info-pending  { background: #fffbeb; border: 1.5px solid #fde68a; }
.info-accepted { background: #f0fdf4; border: 1.5px solid #bbf7d0; }
.info-rejected { background: #fef2f2; border: 1.5px solid #fecaca; }
 
.si-icon {
  width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.info-pending  .si-icon { background: #fef3c7; color: #d97706; }
.info-accepted .si-icon { background: #d1fae5; color: #059669; }
.info-rejected .si-icon { background: #fee2e2; color: #dc2626; }
 
.si-title { font-size: 0.83rem; font-weight: 800; color: #1e1b4b; margin: 0 0 3px; }
.si-msg   { font-size: 0.79rem; color: #6b7280; margin: 0; line-height: 1.5; }
 
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
   DUGMAD
   ================================================================ */
.btn-secondary {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0.5rem 1.2rem; border-radius: 10px;
  font-size: 0.84rem; font-weight: 700; cursor: pointer;
  background: #f3f4f6; color: #6b7280;
  border: 1.5px solid #e5e7eb;
  transition: background .15s;
}
.btn-secondary:hover { background: #e5e7eb; }
 
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
  border-color: rgba(124,58,237,.2);
  border-top-color: #7c3aed;
}
@keyframes spin { to { transform: rotate(360deg) } }
 
/* ================================================================
   TOAST
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
</style>
 