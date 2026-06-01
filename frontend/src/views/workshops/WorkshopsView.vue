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
    </div>

    <div class="py-12 px-4 max-w-4xl mx-auto">

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

      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
        Aktivne radionice
      </h2>

      <p class="text-center text-gray-500 mb-10">
        Klikom na Saznaj više pogledajte detaljne informacije o radionici
      </p>

      <p v-if="error" class="text-center text-gray-500">
        {{ error }}
      </p>

      <div v-else>
        <div v-if="viewType === 'list'" class="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div
            v-for="workshop in workshops"
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

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'
import CalendarView from './Calendar.vue'

const BASE_URL = 'http://127.0.0.1:8000'
import CalendarView from './Calendar.vue' // DODATO: Import komponente
import Notifications from './Notifications.vue' // DODATO: Import tvoje komponente za notifikacije

const workshops = ref([])
const error = ref(null)
const viewType = ref('list')
const registrations = ref({})

/* ---------------- AUTH HELPER ---------------- */
function getAuthHeaders() {
  const token = localStorage.getItem('token')

  if (!token) {
    Swal.fire('Greška', 'Morate biti prijavljeni.', 'warning')
    throw new Error('NO_TOKEN')
  }

  return {
    Authorization: `Bearer ${token}`
  }
}

/* ---------------- FORMAT DATE ---------------- */
function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'Z')
  return `${String(d.getDate()).padStart(2, '0')}.${String(
    d.getMonth() + 1
  ).padStart(2, '0')}.${d.getFullYear()}`
}

/* ---------------- CAPACITY ---------------- */
const getRegisteredCount = (w) => w.registered_count ?? 0

const getFreeSpots = (w) => {
  if (w.free_spots !== undefined) return w.free_spots
  return Math.max(0, (w.capacity ?? 0) - getRegisteredCount(w))
}

const getCapacityClass = (w) =>
  getFreeSpots(w) > 0 ? 'text-green-600' : 'text-red-500'

/* ---------------- FETCH WORKSHOPS ---------------- */
const fetchWorkshops = async () => {
  try {
    error.value = null

    const res = await fetch(`${BASE_URL}/workshops/active`)
    const data = await res.json()

    workshops.value = Array.isArray(data) ? data : []

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
    const res = await fetch(
      `${BASE_URL}/workshops/registration/check/${workshopId}`,
      {
        method: 'GET',
        headers: {
          ...getAuthHeaders()
        }
      }
    )

    const data = await res.json()

    registrations.value = {
      ...registrations.value,
      [workshopId]: data.registered
    }
  } catch (err) {
    if (err.message === 'NO_TOKEN') return

    registrations.value = {
      ...registrations.value,
      [workshopId]: false
    }
  }
}

const checkAllRegistrations = async () => {
  await Promise.all(
    workshops.value.map(w => checkRegistration(w.ID_workshop))
  )
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
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
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
    const res = await fetch(
      `${BASE_URL}/workshops/waiting-list/join/${workshopId}`,
      {
        method: 'POST',
        headers: {
          ...getAuthHeaders()
        }
      }
    )

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.detail || 'Neuspješno dodavanje na listu čekanja.')
    }

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
    const response = await fetch(
      `${BASE_URL}/workshops/cancellation/${id}`,
      {
        method: 'DELETE',
        headers: {
          ...getAuthHeaders()
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Neuspješno otkazivanje.')
    }

    const currentUser = JSON.parse(localStorage.getItem('user') || '{}')

    if (
      data.promotion &&
      currentUser?.id &&
      data.promotion.user_id === currentUser.id
    ) {
      await Swal.fire(
        '🎉 Automatska prijava!',
        `Ti si upravo prijavljen na "${title}" jer si bio prvi na listi čekanja.`,
        'success'
      )
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
      headers: {
        ...getAuthHeaders()
      }
    })

    const data = await res.json()
    const promotion = data?.promotion

    if (!promotion?.is_promoted) return

    const alreadyNotified = localStorage.getItem(
      `promotion_notified_${promotion.workshop_id}`
    )

    if (alreadyNotified) return

    await Swal.fire(
      '🎉 Automatska prijava!',
      `Prebačen si na radionicu: ${promotion.workshop_title}`,
      'success'
    )

    // zapamti po workshop_id (ne globalno)
    localStorage.setItem(
      `promotion_notified_${promotion.workshop_id}`,
      'true'
    )

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