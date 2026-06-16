<template>
  <div class="min-h-screen bg-purple-100">
    <Notifications />

    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        Pronađi edukativne radionice
      </h1>
      <p class="text-gray-600">
        Izaberi radionicu i prijavi se u par klikova.
      </p>
      <!-- Search bar -->
<div class="max-w-2xl mx-auto px-4 mb-6">
  <div ref="searchBarRef" class="relative bg-white rounded-2xl px-4 py-3 shadow-lg">
    <div class="flex items-center gap-3">
      <svg class="w-4 h-4 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      </svg>
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @blur="hideDropdown"
        type="text"
        placeholder="Pretraži radionice po nazivu..."
        class="flex-1 bg-transparent text-sm focus:outline-none text-gray-800 placeholder-gray-400"
      />
      <button @click="dateOpen = !dateOpen" class="flex items-center gap-1.5 text-sm font-medium text-purple-600">
        📅 Datum
      </button>
    </div>

    <div v-if="searchResults.length > 0 && searchQuery.trim()"
      class="absolute left-0 right-0 bg-white rounded-2xl shadow-xl border border-purple-100 overflow-y-auto"
      style="top: calc(100% + 8px); z-index: 9999; max-height: 320px;">
      <div v-for="workshop in searchResults" :key="workshop.ID_workshop"
        @mousedown.prevent="goToWorkshop(workshop)"
        class="px-4 py-3 hover:bg-purple-50 cursor-pointer border-b border-gray-50 last:border-0">
        <p class="text-sm font-semibold text-gray-800">{{ workshop.title }}</p>
        <p class="text-xs text-gray-400">{{ formatDate(workshop.date) }} · {{ workshop.location }}</p>
      </div>
    </div>
  </div>

  <!-- Date panel -->
  <div v-if="dateOpen" class="bg-white rounded-2xl px-4 py-3 mt-2 flex items-center gap-3 flex-wrap shadow-md">
    <span class="text-xs text-gray-400">Od</span>
    <input v-model="filterDateFrom" type="date" class="text-sm px-3 py-1.5 rounded-lg border border-purple-200 focus:outline-none bg-white" />
    <span class="text-xs text-gray-400">Do</span>
    <input v-model="filterDateTo" type="date" class="text-sm px-3 py-1.5 rounded-lg border border-purple-200 focus:outline-none bg-white" />
    <button @click="applyFilters" class="ml-auto px-4 py-1.5 text-white text-sm font-semibold rounded-lg" style="background:#7c3aed;">
      Primijeni
    </button>
  </div>

  <!-- Location chips -->
  <div class="flex gap-2 flex-wrap mt-3">
    <button v-for="loc in locationChips" :key="loc" @click="selectLocation(loc)"
      :class="filterLocation === loc ? 'bg-purple-600 text-white' : 'bg-white text-purple-600 border border-purple-200'"
      class="px-4 py-1.5 rounded-full text-sm font-semibold transition-all">
      {{ loc }}
    </button>
  </div>
</div>
    </div>

    <div class="py-12 px-4 max-w-7xl mx-auto">

      <div class="flex justify-end mb-6">
        <div class="inline-flex rounded-lg border border-purple-200 bg-white p-1 shadow-sm">
          <button
            @click="viewType = 'list'"
            :class="viewType === 'list' ? 'bg-purple-600 text-white' : 'text-purple-600 hover:bg-purple-50'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            ☰ Lista
          </button>

          <button
            @click="viewType = 'calendar'"
            :class="viewType === 'calendar' ? 'bg-purple-600 text-white' : 'text-purple-600 hover:bg-purple-50'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            📅 Kalendar
          </button>
        </div>
      </div>

      <p v-if="error" class="text-center text-gray-500">
        {{ error }}
      </p>

      <div v-else>
        <div v-if="viewType === 'list'" class="grid grid-cols-1 md:grid-cols-2 gap-8">

          <!-- LIJEVO: Aktivne radionice -->
          <div>
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
              Aktivne radionice
            </h2>
            <p class="text-center text-gray-500 mb-10">
              Klikom na Saznaj više pogledajte detaljne informacije o radionici
            </p>
            <div v-if="activeWorkshops.length === 0" class="text-gray-400 text-sm text-center py-10 bg-white rounded-xl">
              Nema aktivnih radionica.
            </div>
            <div class="flex flex-col gap-4">
              <div
                v-for="workshop in activeWorkshops"
                :key="workshop.ID_workshop"
                class="bg-white rounded-xl p-5 border border-gray-100 flex flex-col gap-2"
              >
                <h3 class="font-medium text-base text-gray-800">
                  {{ workshop.title }}
                </h3>
                <p class="text-sm text-gray-400">
                  Datum: {{ formatDate(workshop.date) }}
                </p>
                <p class="text-sm text-gray-400">
                  Lokacija: {{ workshop.location }}
                </p>
                <p class="text-sm font-medium" :class="getCapacityClass(workshop)">
                  <span v-if="getFreeSpots(workshop) > 0">
                    Slobodnih mjesta: {{ getFreeSpots(workshop) }}
                  </span>
                  <span v-else>
                    Kapacitet popunjen
                  </span>
                </p>
                <p
                  v-if="registrations[workshop.ID_workshop] === true"
                  class="text-green-600 text-xs font-semibold"
                >
                  Već si prijavljen na ovu radionicu
                </p>
                <hr class="border-gray-100 mt-2" />
                <div class="flex justify-between items-center">
                  <router-link
                    :to="`/workshops/${workshop.ID_workshop}`"
                    class="text-sm font-medium text-purple-600"
                  >
                    Saznaj više →
                  </router-link>
                  <!-- Odustani ako je prijavljen -->
                  <button
                    v-if="registrations[workshop.ID_workshop]"
                    @click="handleCancel(workshop.ID_workshop, workshop.title)"
                    class="text-xs font-medium text-gray-400 hover:text-red-500 uppercase tracking-wide"
                  >
                    Odustani
                  </button>
                  <!-- Prijava ako ima mjesta -->
                  <span v-else-if="getFreeSpots(workshop) > 0"></span>
                  <!-- Waiting list -->
                  <button
                    v-else
                    @click="handleJoinWaitingList(workshop.ID_workshop)"
                    class="text-xs font-medium text-orange-500 hover:text-orange-700 uppercase tracking-wide"
                  >
                    Dodaj se na listu čekanja
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- DESNO: Završene radionice -->
          <div>
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
              Završene radionice
            </h2>
            <p class="text-center text-gray-500 mb-10">
              Pogledajte ocjene završenih radionica
            </p>
            <div v-if="completedWorkshops.length === 0" class="text-gray-400 text-sm text-center py-10 bg-white rounded-xl">
              Nema završenih radionica.
            </div>
            <div class="flex flex-col gap-4">
              <div
                v-for="workshop in completedWorkshops"
                :key="workshop.ID_workshop"
                class="bg-white rounded-xl p-5 border border-gray-100 flex flex-col gap-2 opacity-80"
              >
                <div class="flex items-center justify-between">
                  <h3 class="font-medium text-base text-gray-700">{{ workshop.title }}</h3>
                  <span class="text-xs bg-gray-100 text-gray-500 px-2 py-1 rounded-full">Završena</span>
                </div>
                <p class="text-sm text-gray-400">Datum: {{ formatDate(workshop.date) }}</p>
                <p class="text-sm text-gray-400">Lokacija: {{ workshop.location }}</p>
                <hr class="border-gray-100 mt-2" />
                <div class="flex justify-between items-center">
                  <router-link :to="`/workshops/${workshop.ID_workshop}`" class="text-sm font-medium text-purple-500">
                    Pogledaj ocjene →
                  </router-link>
                  <button
                    @click="openRatingModal(workshop.ID_workshop, workshop.title)"
                    class="text-xs font-medium text-purple-600 hover:text-purple-800 uppercase tracking-wide"
                  >
                    Ostavi ocjenu
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>

        <div v-else>
          <CalendarView :workshops="workshops" :registrations="registrations" />
        </div>
      </div>
    </div>

    <!-- Floating button -->
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

    <!-- Modal za ocjenu -->
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
          class="w-full py-3 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 disabled:opacity-50 transition-colors"
        >
          {{ ratingSubmitting ? 'Šaljem...' : 'Pošalji ocjenu' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

const BASE_URL = 'http://127.0.0.1:8000'
import CalendarView from './Calendar.vue'
import Notifications from './Notifications.vue'

const router = useRouter()
const workshops = ref([])
const error = ref(null)
const viewType = ref('list')
const registrations = ref({})

const activeWorkshops = computed(() => workshops.value.filter(w => w.status === 'upcoming'))
const completedWorkshops = computed(() => workshops.value.filter(w => w.status === 'completed'))

/* ---------------- SEARCH & FILTERI ---------------- */
const searchQuery = ref('')
const searchResults = ref([])
const searchBarRef = ref(null)
const filterLocation = ref('Sve')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const dateOpen = ref(false)
const locationChips = ref(['Sve'])
let searchTimeout = null

const filtersActive = computed(() =>
  (filterLocation.value && filterLocation.value !== 'Sve') ||
  filterDateFrom.value !== '' ||
  filterDateTo.value !== ''
)

const handleSearch = () => {
  clearTimeout(searchTimeout)
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
  setTimeout(() => { searchResults.value = [] }, 200)
}

const goToWorkshop = (workshop) => {
  searchQuery.value = ''
  searchResults.value = []
  router.push(`/workshops/${workshop.ID_workshop}`)
}

const selectLocation = async (loc) => { filterLocation.value = loc; await applyFilters() }

const clearDates = async () => {
  filterDateFrom.value = ''; filterDateTo.value = ''; dateOpen.value = false; await applyFilters()
}

const applyFilters = async () => {
  try {
    error.value = null
    const params = new URLSearchParams()
    if (filterLocation.value && filterLocation.value !== 'Sve') params.append('location', filterLocation.value)
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
  filterLocation.value = 'Sve'; filterDateFrom.value = ''; filterDateTo.value = ''; dateOpen.value = false
  await refreshWorkshops()
}

/* ---------------- RATING ---------------- */
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
  ratingSubmitting.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`${BASE_URL}/workshops/${selectedWorkshopId.value}/ratings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        score: ratingForm.value.score,
        comment: ratingForm.value.comment || null
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Greška.')
    showRatingModal.value = false
    await Swal.fire('Hvala!', 'Vaša ocjena je uspješno poslana.', 'success')
  } catch (err) {
    Swal.fire('Greška', err.message || 'Neuspješno slanje ocjene.', 'error')
  } finally {
    ratingSubmitting.value = false
  }
}

/* ---------------- AUTH HELPER ---------------- */
function getAuthHeaders() {
  const token = localStorage.getItem('token')
  if (!token) {
    Swal.fire('Greška', 'Morate biti prijavljeni.', 'warning')
    throw new Error('NO_TOKEN')
  }
  return { Authorization: `Bearer ${token}` }
}

/* ---------------- FORMAT DATE ---------------- */
function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'Z')
  return `${String(d.getDate()).padStart(2, '0')}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`
}

/* ---------------- CAPACITY ---------------- */
const getRegisteredCount = (w) => w.registered_count ?? 0

const getFreeSpots = (w) => {
  if (w.free_spots !== undefined) return w.free_spots
  return Math.max(0, (w.capacity ?? 0) - getRegisteredCount(w))
}

const getCapacityClass = (w) => getFreeSpots(w) > 0 ? 'text-green-600' : 'text-red-500'

/* ---------------- FETCH WORKSHOPS ---------------- */
const fetchWorkshops = async () => {
  try {
    error.value = null
    try {
      await fetch(`${BASE_URL}/workshops/auto-complete`, { method: 'POST' })
    } catch {
      console.warn('auto-complete nije uspio')
    }
    const res = await fetch(`${BASE_URL}/workshops/active`)
    const data = await res.json()
    workshops.value = Array.isArray(data) ? data : []
    const locations = [...new Set(workshops.value.map(w => w.location).filter(Boolean))]
    locationChips.value = ['Sve', ...locations]
    if (!Array.isArray(data)) {
      error.value = 'Trenutno nema aktivnih radionica.'
    }
  } catch {
    error.value = 'Nije moguće kontaktirati server.'
  }
}

/* ---------------- REGISTRATION CHECK ---------------- */
const checkRegistration = async (workshopId) => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/registration/check/${workshopId}`, {
      method: 'GET',
      headers: { ...getAuthHeaders() }
    })
    const data = await res.json()
    registrations.value = { ...registrations.value, [workshopId]: data.registered }
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    registrations.value = { ...registrations.value, [workshopId]: false }
  }
}

const checkAllRegistrations = async () => {
  await Promise.all(workshops.value.map(w => checkRegistration(w.ID_workshop)))
}

/* ---------------- REGISTER ---------------- */
const handleRegister = async (workshopId) => {
  try {
    const user = JSON.parse(localStorage.getItem('user'))
    if (!user) {
      Swal.fire('Greška', 'Niste prijavljeni.', 'warning')
      return
    }
    const res = await fetch(`${BASE_URL}/workshops/registration`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
      body: JSON.stringify({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        phone: user.phone,
        workshop_id: workshopId,
        previous_experience: '',
        github_profile: ''
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    await Swal.fire('Uspjeh', 'Uspješno ste prijavljeni.', 'success')
    await refreshWorkshops()
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Neuspješna prijava.', 'error')
  }
}

/* ---------------- WAITING LIST ---------------- */
const handleJoinWaitingList = async (workshopId) => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/waiting-list/join/${workshopId}`, {
      method: 'POST',
      headers: { ...getAuthHeaders() }
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Neuspješno dodavanje na listu čekanja.')
    await Swal.fire('Uspjeh', 'Dodani ste na listu čekanja.', 'success')
    await refreshWorkshops()
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Server greška.', 'error')
  }
}

/* ---------------- CANCEL ---------------- */
const handleCancel = async (id, title) => {
  const result = await Swal.fire({
    title: 'Otkazivanje?',
    text: `Želite li odustati od radionice: ${title}?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Da, otkaži',
    cancelButtonText: 'Ne',
    confirmButtonColor: '#d33'
  })
  if (!result.isConfirmed) return
  try {
    const response = await fetch(`${BASE_URL}/workshops/cancellation/${id}`, {
      method: 'DELETE',
      headers: { ...getAuthHeaders() }
    })
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

/* ---------------- PROMOTION CHECK ---------------- */
const checkMyPromotion = async () => {
  try {
    const res = await fetch(`${BASE_URL}/workshops/my-promotion`, {
      method: 'GET',
      headers: { ...getAuthHeaders() }
    })
    const data = await res.json()
    const promotion = data?.promotion
    if (!promotion?.is_promoted) return
    const alreadyNotified = localStorage.getItem(`promotion_notified_${promotion.workshop_id}`)
    if (alreadyNotified) return
    await Swal.fire('🎉 Automatska prijava!', `Prebačen si na radionicu: ${promotion.workshop_title}`, 'success')
    localStorage.setItem(`promotion_notified_${promotion.workshop_id}`, 'true')
  } catch (err) {
    Swal.fire('Greška', err.message || 'Server greška.', 'error')
  }
}

/* ---------------- REFRESH ---------------- */
const refreshWorkshops = async () => {
  await fetchWorkshops()
  await checkAllRegistrations()
}

/* ---------------- INIT ---------------- */
onMounted(async () => {
  await refreshWorkshops()
  await checkMyPromotion()
})
</script>