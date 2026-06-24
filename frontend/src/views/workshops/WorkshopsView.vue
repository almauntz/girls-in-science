<template>
  <div class="min-h-screen" style="background: #f4f1fb; font-family: 'Segoe UI', system-ui, sans-serif;">
    <Notifications />
    <div
      class="relative overflow-visible px-6 pt-10 pb-8"
      style="background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 50%, #9333ea 100%);"
    >
      <div class="absolute top-0 right-0 w-64 h-64 rounded-full opacity-10" style="background: #fff; transform: translate(30%, -30%);"></div>
      <div class="absolute bottom-0 left-1/2 w-48 h-48 rounded-full opacity-10" style="background: #fff; transform: translate(-50%, 50%);"></div>
      
      <div class="relative max-w-2xl mx-auto">
        <h1 class="text-3xl font-extrabold text-white mb-1">Pronađi edukativne radionice</h1>
        <p class="text-purple-200 text-sm mb-6">Izaberi radionicu i prijavi se u par klikova.</p>

      <!-- Search bar -->
<div ref="searchBarRef" class="relative bg-white rounded-2xl px-4 py-3 shadow-lg mb-4" style="gap: 10px;">
  <div class="flex items-center" style="gap: 10px;">
    <svg class="w-4 h-4 flex-shrink-0" style="color:#a78bfa;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <input
      v-model="searchQuery"
      @input="handleSearch"
      @blur="hideDropdown"
      type="text"
      placeholder="Pretraži radionice po nazivu ili lokaciji..."
      class="flex-1 bg-transparent text-sm focus:outline-none text-gray-800 placeholder-gray-400"
    />
    <div class="w-px h-5 bg-gray-200 flex-shrink-0"></div>
    <button
      @click="dateOpen = !dateOpen"
      class="flex items-center gap-1.5 text-sm font-medium transition-colors flex-shrink-0"
      style="color: #7c3aed;"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>
      </svg>
      Datum
      <svg class="w-3 h-3 transition-transform duration-200" :class="dateOpen ? 'rotate-180' : ''" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
        <path d="m6 9 6 6 6-6"/>
      </svg>
    </button>
  </div>

  <div
    v-if="searchResults.length > 0 && searchQuery.trim()"
    class="absolute left-0 right-0 bg-white rounded-2xl shadow-xl border border-purple-100 overflow-y-auto"
    style="top: calc(100% + 8px); z-index: 9999; max-height: 320px;"
  >
    <div
      v-for="workshop in searchResults"
      :key="workshop.ID_workshop"
      @mousedown.prevent="goToWorkshop(workshop)"
      class="px-4 py-3 hover:bg-purple-50 cursor-pointer border-b border-gray-50 last:border-0"
    >
      <p class="text-sm font-semibold text-gray-800">{{ workshop.title }}</p>
      <p class="text-xs text-gray-400">{{ formatDate(workshop.date) }} · {{ workshop.location }}</p>
    </div>
  </div>
</div>

        <!-- Date panel -->
        <div
          v-if="dateOpen"
          class="bg-white rounded-2xl px-4 py-3 mb-4 flex items-center gap-3 flex-wrap shadow-md"
        >
          <span class="text-xs text-gray-400">Od</span>
          <input v-model="filterDateFrom" type="date" class="text-sm px-3 py-1.5 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-400 bg-white" />
          <span class="text-xs text-gray-400">Do <span class="italic">(opciono)</span></span>
          <input v-model="filterDateTo" type="date" class="text-sm px-3 py-1.5 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-400 bg-white" />
          <button @click="applyFilters" class="ml-auto px-4 py-1.5 text-white text-sm font-semibold rounded-lg transition-colors" style="background:#7c3aed;">
            Primijeni
          </button>
        </div>

        <div v-if="filtersActive" class="flex gap-2 flex-wrap mt-3">
          <span v-if="filterDateFrom || filterDateTo" class="inline-flex items-center gap-1.5 text-xs px-3 py-1 rounded-full bg-white/20 text-white border border-white/30">
            {{ filterDateFrom || '...' }} → {{ filterDateTo || '...' }}
            <button @click="clearDates" class="hover:text-red-300 font-bold">×</button>
          </span>
          <button @click="resetFilters" class="text-xs text-purple-200 hover:text-white transition-colors">
            Resetuj sve ✕
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 pb-32">

      <div class="flex justify-end mb-5">
        <div class="inline-flex rounded-xl border border-purple-100 bg-white p-1 shadow-sm">
          <button
            @click="viewType = 'list'"
            :class="viewType === 'list' ? 'text-white' : 'hover:bg-purple-50'"
            :style="viewType === 'list' ? 'background:#7c3aed; color:#fff;' : 'color:#7c3aed;'"
            class="px-4 py-2 rounded-lg text-sm font-semibold transition-all"
          >
            ☰ Lista
          </button>
          <button
            @click="viewType = 'calendar'"
            :style="viewType === 'calendar' ? 'background:#7c3aed; color:#fff;' : 'color:#7c3aed;'"
            class="px-4 py-2 rounded-lg text-sm font-semibold transition-all hover:bg-purple-50"
          >
            📅 Kalendar
          </button>
        </div>
      </div>

      <p v-if="error" class="text-center text-gray-400 text-sm py-8">{{ error }}</p>

      <div v-else>
        <!-- CALENDAR VIEW -->
        <div v-if="viewType === 'calendar'">
          <CalendarView :workshops="workshops" :registrations="registrations" />
        </div>

<!-- LIST VIEW -->
<div v-else class="flex flex-col gap-10">

  <!-- Aktivne radionice -->
  <div>
    <div class="flex items-center gap-3 mb-5">
      <div class="w-1 h-7 rounded-full" style="background:#7c3aed;"></div>
      <h2 class="text-xl font-extrabold text-gray-800">Aktivne radionice</h2>
      <span class="text-xs font-bold px-3 py-1 rounded-full text-purple-700" style="background:#ede9fe;">
        {{ activeWorkshops.length }} dostupnih
      </span>
    </div>

    <div v-if="activeWorkshops.length === 0" class="text-gray-400 text-sm text-center py-10 bg-white rounded-2xl">
      Nema aktivnih radionica.
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div
        v-for="workshop in activeWorkshops"
        :key="workshop.ID_workshop"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-200 overflow-hidden flex flex-col"
      >
        <!-- Colored top accent -->
        <div class="h-1.5 w-full" :style="getFreeSpots(workshop) > 0 ? 'background: linear-gradient(90deg,#7c3aed,#a855f7)' : 'background: linear-gradient(90deg,#f59e0b,#fbbf24)'"></div>

        <div class="p-5 flex flex-col gap-3 flex-1">
          <!-- Status + prijava tag -->
          <div class="flex items-center gap-2 flex-wrap">
            <span
              class="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full"
              :style="getFreeSpots(workshop) > 0 ? 'background:#dcfce7; color:#16a34a;' : 'background:#fef3c7; color:#b45309;'"
            >
              <span class="w-1.5 h-1.5 rounded-full inline-block" :style="getFreeSpots(workshop) > 0 ? 'background:#16a34a;' : 'background:#b45309;'"></span>
              {{ getFreeSpots(workshop) > 0 ? 'Slobodna mjesta' : 'Popunjeno' }}
            </span>
            <span v-if="registrations[workshop.ID_workshop] === true" class="text-xs font-semibold px-2.5 py-1 rounded-full" style="background:#ede9fe; color:#7c3aed;">
              ✓ Prijavljen
            </span>
            <span v-if="waitingList[workshop.ID_workshop]" class="text-xs font-semibold px-2.5 py-1 rounded-full" style="background:#fef3c7; color:#b45309;">
              ⏳ Lista čekanja
            </span>
          </div>

          <!-- Naziv -->
          <h3 class="font-extrabold text-base text-gray-800 leading-snug">{{ workshop.title }}</h3>

          <!-- Info -->
          <div class="flex flex-col gap-1.5 text-xs text-gray-400">
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
              {{ formatDate(workshop.date) }}
            </span>
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              {{ workshop.location }}
            </span>
          </div>

          <!-- Progress bar -->
          <div v-if="workshop.capacity" class="mt-1">
            <div class="flex justify-between text-xs text-gray-400 mb-1">
              <span>Popunjenost</span>
              <span class="font-semibold" :style="getFreeSpots(workshop) > 0 ? 'color:#7c3aed' : 'color:#b45309'">
                {{ workshop.capacity - getFreeSpots(workshop) }}/{{ workshop.capacity }}
              </span>
            </div>
            <div class="w-full h-1.5 rounded-full bg-gray-100 overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-500"
                :style="`width: ${Math.round(((workshop.capacity - getFreeSpots(workshop)) / workshop.capacity) * 100)}%; background: ${getFreeSpots(workshop) > 0 ? '#7c3aed' : '#f59e0b'}`"
              ></div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-between items-center pt-3 mt-auto border-t border-gray-50">
            <router-link :to="`/workshops/${workshop.ID_workshop}`" class="text-sm font-bold transition-colors" style="color:#7c3aed;">
              Saznaj više →
            </router-link>
            <button
              v-if="registrations[workshop.ID_workshop]"
              @click="handleCancel(workshop.ID_workshop, workshop.title)"
              class="text-xs font-semibold text-gray-400 hover:text-red-500 uppercase tracking-wide transition-colors"
            >Odustani</button>
            <button
              v-else-if="waitingList[workshop.ID_workshop]"
              @click="handleLeaveWaitingList(workshop.ID_workshop)"
              class="text-xs font-semibold text-red-400 hover:text-red-600 uppercase tracking-wide transition-colors"
            >Napusti listu</button>
            <button
              v-else-if="getFreeSpots(workshop) === 0"
              @click="handleJoinWaitingList(workshop.ID_workshop)"
              class="text-xs font-semibold uppercase tracking-wide transition-colors"
              style="color:#d97706;"
            >Lista čekanja</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Završene radionice -->
  <div>
    <div class="flex items-center gap-3 mb-5">
      <div class="w-1 h-7 rounded-full bg-gray-300"></div>
      <h2 class="text-xl font-extrabold text-gray-800">Završene radionice</h2>
      <span class="text-xs font-bold px-3 py-1 rounded-full text-gray-500" style="background:#f3f4f6;">
        {{ completedWorkshops.length }} završenih
      </span>
    </div>

    <div v-if="completedWorkshops.length === 0" class="text-gray-400 text-sm text-center py-10 bg-white rounded-2xl">
      Nema završenih radionica.
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div
        v-for="workshop in completedWorkshops"
        :key="workshop.ID_workshop"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col opacity-80"
      >
        <div class="h-1.5 w-full bg-gray-200"></div>

        <div class="p-5 flex flex-col gap-3 flex-1">
          <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full w-fit" style="background:#f3f4f6; color:#6b7280;">
            <span class="w-1.5 h-1.5 rounded-full bg-gray-400 inline-block"></span>
            Završena
          </span>

          <h3 class="font-extrabold text-base text-gray-600 leading-snug">{{ workshop.title }}</h3>

          <div class="flex flex-col gap-1.5 text-xs text-gray-400">
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
              {{ formatDate(workshop.date) }}
            </span>
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              {{ workshop.location }}
            </span>
          </div>

          <div class="flex justify-between items-center pt-3 mt-auto border-t border-gray-50">
            <router-link :to="`/workshops/${workshop.ID_workshop}`" class="text-sm font-bold transition-colors" style="color:#9333ea;">
              Pogledaj ocjene →
            </router-link>
            <button
              @click="openRatingModal(workshop.ID_workshop, workshop.title)"
              class="text-xs font-bold uppercase tracking-wide px-3 py-1.5 rounded-lg transition-colors"
              style="background:#ede9fe; color:#7c3aed;"
            >
              ★ Ocijeni
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>
    </div>

  </div>
      <!-- Prijedlog dugme -->
     <router-link
  to="/workshops/my-proposals"
  class="fixed bottom-8 right-8 flex items-center gap-3 text-white text-sm font-bold px-6 py-4 rounded-full shadow-2xl transition-all hover:-translate-y-1 hover:shadow-purple-400/50 hover:shadow-2xl"
  style="background: linear-gradient(135deg, #7c3aed, #a855f7); box-shadow: 0 8px 30px rgba(124, 58, 237, 0.45);"
>
  <span class="text-xl">💡</span>
  <span class="flex flex-col leading-tight">
    <span class="text-xs font-medium opacity-80">
      Imaš ideju za radionicu?
    </span>
    <span class="text-base font-extrabold tracking-wide">
      Dodaj svoj prijedlog!
    </span>
  </span>
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" stroke-width="2.5" class="opacity-80">
    <line x1="5" y1="12" x2="19" y2="12"/>
    <polyline points="12 5 19 12 12 19"/>
  </svg>
</router-link>

    <!-- Rating -->
    <div v-if="showRatingModal" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" @click="showRatingModal = false"></div>
      <div class="relative z-10 bg-white rounded-2xl p-8 w-[480px] shadow-2xl">
        <button @click="showRatingModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl">×</button>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Ocjenite radionicu</h3>
        <p class="text-sm text-gray-500 mb-6">{{ selectedWorkshopTitle }}</p>
        <div class="flex gap-3 mb-6 justify-center">
          <button
            v-for="n in 5"
            :key="n"
            @click="ratingForm.score = n"
            class="text-4xl transition-transform hover:scale-110"
            :class="n <= ratingForm.score ? 'text-yellow-400' : 'text-gray-300'"
          >★</button>
        </div>
        <textarea
          v-model="ratingForm.comment"
          placeholder="Komentar (opciono)..."
          maxlength="500"
          rows="3"
          class="w-full border border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:border-purple-400 resize-none mb-4"
        ></textarea>
        <button
          @click="submitRating"
          :disabled="!ratingForm.score || ratingSubmitting"
          class="w-full py-3 text-white rounded-lg font-bold disabled:opacity-50 transition-colors"
          style="background:#7c3aed;"
        >
          {{ ratingSubmitting ? 'Šaljem...' : 'Pošalji ocjenu' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted,reactive } from 'vue'
import axios from "axios";
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'
import CalendarView from './Calendar.vue'
import Notifications from './Notifications.vue'
import confetti from 'canvas-confetti'
import Location from './Location.vue'

const BASE_URL = import.meta.env.VITE_API_URL
const router = useRouter()

const workshops = ref([])
const error = ref(null)
const viewType = ref('list')
const registrations = ref({})
const waitingList = reactive({})

const activeWorkshops = computed(() => workshops.value.filter(w => w.status === 'upcoming'))
const completedWorkshops = computed(() => workshops.value.filter(w => w.status === 'completed'))


const searchQuery = ref('')
const searchResults = ref([])
const dropdownTop = ref(0)
const dropdownLeft = ref(0)
const dropdownWidth = ref(0)
const searchBarRef = ref(null)
let searchTimeout = null

const updateDropdownPosition = () => {
  if (searchBarRef.value) {
    const rect = searchBarRef.value.getBoundingClientRect()
    dropdownTop.value = rect.bottom + 8
    dropdownLeft.value = rect.left
    dropdownWidth.value = rect.width
  }
}

const handleSearch = () => {
  clearTimeout(searchTimeout)
  updateDropdownPosition()
  if (searchQuery.value.trim() === '') { searchResults.value = []; return }
  searchTimeout = setTimeout(async () => {
    await fetchSearchResults(searchQuery.value.trim())
  }, 400)
}

const fetchSearchResults = async (title) => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/search?title=${encodeURIComponent(title)}`)
    const data = await res.json()
    searchResults.value = Array.isArray(data) ? data : []
  } catch { searchResults.value = [] }
}

const hideDropdown = () => {
  setTimeout(() => {
    searchResults.value = []
    searchQuery.value = ''   // ← dodaj ovo

  }, 200)
}

const goToWorkshop = (workshop) => {
  searchQuery.value = ''
  searchResults.value = []
  router.push(`/workshops/${workshop.ID_workshop}`)
}

/* ---------------- FILTERI ---------------- */

const filterDateFrom = ref('')
const filterDateTo = ref('')
const dateOpen = ref(false)

const clearDates = async () => { filterDateFrom.value = ''; filterDateTo.value = ''; dateOpen.value = false; await applyFilters() }
const filtersActive = computed(() => filterDateFrom.value !== '' || filterDateTo.value !== '')

const applyFilters = async () => {
  try {
    error.value = null
    const params = new URLSearchParams()
    if (filterDateFrom.value) params.append('date_from', filterDateFrom.value)
    if (filterDateTo.value) params.append('date_to', filterDateTo.value)
    const url = params.toString() ? `${BASE_URL}/workshops/search?${params.toString()}` : `${BASE_URL}/workshops/active`
    const res = await fetch(url)
    const data = await res.json()
    workshops.value = Array.isArray(data) ? data : []
    if (workshops.value.length === 0) error.value = 'Nema radionica koje odgovaraju filterima.'
    await checkAllRegistrations()
  } catch { error.value = 'Greška pri filtriranju.' }
}

const resetFilters = async () => {
  filterDateFrom.value = ''; filterDateTo.value = ''; dateOpen.value = false
  await refreshWorkshops()
}

/* --- Rating --- */
const showRatingModal = ref(false)
const selectedWorkshopId = ref(null)
const selectedWorkshopTitle = ref('')
const ratingForm = ref({ score: 0, comment: '' })
const ratingSubmitting = ref(false)

const openRatingModal = (workshopId, title) => {
  selectedWorkshopId.value = workshopId
  selectedWorkshopTitle.value = title
  ratingForm.value = { score: 0, comment: '' }
  showRatingModal.value = true
}

const submitRating = async () => {
  if (!ratingForm.value.score) return

  const token = localStorage.getItem('token')
  if (!token) {
    Swal.fire('Greška', 'Morate biti prijavljeni da biste ocijenili radionicu.', 'error')
    return
  }

  ratingSubmitting.value = true
  try {
    const res = await fetch(`${BASE_URL}/workshops/${selectedWorkshopId.value}/ratings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ score: ratingForm.value.score, comment: ratingForm.value.comment || null })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Greška.')
    
    showRatingModal.value = false

    confetti({
      particleCount: 120,
      spread: 80,
      origin: { y: 0.6 }
    })

    await Swal.fire('Hvala!', 'Vaša ocjena je uspješno poslana.', 'success')
  } catch (err) {
    const poruka = err.message === 'Could not validate credentials'
      ? 'Morate biti prijavljeni da biste ocijenili radionicu.'
      : err.message || 'Neuspješno slanje ocjene.'
    Swal.fire('Greška', poruka, 'error')
  } finally { 
    ratingSubmitting.value = false 
  }
}
/* --- Auth helper ---- */
function getAuthHeaders() {
  const token = localStorage.getItem('token')
 /* if (!token) { Swal.fire('Greška', 'Morate biti prijavljeni.', 'warning'); throw new Error('NO_TOKEN') } */
  return { Authorization: `Bearer ${token}` }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'Z')
  return `${String(d.getDate()).padStart(2, '0')}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`
}

const getFreeSpots = (w) => {
  if (w.free_spots !== undefined) return w.free_spots
  return Math.max(0, (w.capacity ?? 0) - (w.registered_count ?? 0))
}

const fetchWorkshops = async () => {
  try {
    error.value = null
    try { await fetch(`${BASE_URL}/workshops/auto-complete`, { method: 'POST' }) } catch { console.warn('auto-complete nije uspio') }
    const res = await fetch(`${BASE_URL}/workshops/active`)
    const data = await res.json()
    workshops.value = Array.isArray(data) ? data : []
    if (!Array.isArray(data)) error.value = 'Trenutno nema aktivnih radionica.'
  } catch { error.value = 'Nije moguće kontaktirati server.' }
}

const checkRegistration = async (workshopId) => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/registration/check/${workshopId}`, { headers: { ...getAuthHeaders() } })
    const data = await res.json()
    registrations.value = { ...registrations.value, [workshopId]: data.registered }
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    registrations.value = { ...registrations.value, [workshopId]: false }
  }
}

const checkAllRegistrations = async () => { 
  const token = localStorage.getItem('token')
  if (!token) return
  await Promise.all(workshops.value.map(w => checkRegistration(w.ID_workshop))) }

const handleJoinWaitingList = async (workshopId) => {
  try {
    const res = await fetch(
      `${BASE_URL}/workshops/waiting-list/join/${workshopId}`,
      {
        method: 'POST',
        headers: { ...getAuthHeaders() }
      }
    )

    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Neuspješno dodavanje na listu čekanja.')

    waitingList[workshopId] = true

    await Swal.fire('Uspjeh', 'Dodani ste na listu čekanja.', 'success')

    await refreshWorkshops()
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Server greška.', 'error')
  }
}

const handleCancel = async (id, title) => {
  const result = await Swal.fire({
    title: 'Otkazivanje?', text: `Želite li odustati od radionice: ${title}?`, icon: 'question',
    showCancelButton: true, confirmButtonText: 'Da, otkaži', cancelButtonText: 'Ne', confirmButtonColor: '#d33'
  })
  if (!result.isConfirmed) return
  try {
    const response = await fetch(`${BASE_URL}/workshops/cancellation/${id}`, { method: 'DELETE', headers: { ...getAuthHeaders() } })
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'Neuspješno otkazivanje.')
    const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
    if (data.promotion && currentUser?.id && data.promotion.user_id === currentUser.id) {
      await Swal.fire('🎉 Automatska prijava!', `Ti si upravo prijavljen na "${title}" jer si bio prvi na listi čekanja.`, 'success')
    } else {
      await Swal.fire('Otkazano', 'Prijava je poništena.', 'success')
    }
    await refreshWorkshops()
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Server nije dostupan.', 'error')
  }
}

const handleLeaveWaitingList = async (id) => {
  const result = await Swal.fire({
    title: 'Lista čekanja?',
    text: `Želite li napustiti listu čekanja za ovu radionicu?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Da, napusti',
    cancelButtonText: 'Ne',
    confirmButtonColor: '#d33'
  })

  if (!result.isConfirmed) return

  try {
    const response = await fetch(
      `${BASE_URL}/workshops/waiting-list/${id}`,
      {
        method: 'DELETE',
        headers: { ...getAuthHeaders() }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Neuspješno uklanjanje sa liste čekanja.')
    }

    delete waitingList[id]

    await Swal.fire(
      'Uklonjeno',
      'Uspješno ste uklonjeni sa liste čekanja.',
      'success'
    )

    await refreshWorkshops()

  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Server nije dostupan.', 'error')
  }
}



const fetchWaitingList = async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  const res = await fetch(`${BASE_URL}/workshops/waiting-list/me`, {
    headers: getAuthHeaders()
  })

  const data = await res.json()

  // reset
  Object.keys(waitingList).forEach(k => delete waitingList[k])

  data.forEach(item => {
    waitingList[item.workshop_id] = true
  })
}

const checkMyPromotion = async () => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/my-promotion`, {
      headers: { ...getAuthHeaders() }
    })

    const data = await res.json()
    const promotion = data?.promotion

    if (!promotion?.is_promoted) return

    await Swal.fire(
      '🎉 Automatska prijava!',
      `Prebačen si na radionicu: ${promotion.workshop_title}`,
      'success'
    )

    //refresh UI nakon promocije
    await refreshWorkshops()
    await fetchWaitingList()

  } catch (err) {
    if (err.message !== 'NO_TOKEN') {
      Swal.fire('Greška', err.message || 'Server greška.', 'error')
    }
  }
}

const refreshWorkshops = async () => { await fetchWorkshops(); await checkAllRegistrations() }

onMounted(async () => {
  await refreshWorkshops()
  await checkMyPromotion()
  await fetchWaitingList()
})
</script>
