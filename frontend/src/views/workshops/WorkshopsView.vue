<template>
  <div class="min-h-screen bg-purple-100">
    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        Pronađi edukativne radionice
      </h1>
      <p class="text-gray-600">
        Izaberi radionicu i prijavi se u par klikova.
      </p>
    </div>

    <div class="py-12 px-4 max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">
        Aktivne radionice
      </h2>

      <p class="text-center text-gray-500 mb-10">
        Klikom na Saznaj više pogledajte detaljne informacije o radionici
      </p>

      <p v-if="error" class="text-center text-gray-500">
        {{ error }}
      </p>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
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

          <!-- CAPACITY -->
          <p class="text-sm font-medium" :class="getCapacityClass(workshop)">
            <span v-if="getFreeSpots(workshop) > 0">
              Slobodnih mjesta: {{ getFreeSpots(workshop) }}
            </span>
            <span v-else>
              Kapacitet popunjen
            </span>
          </p>

          <!-- REGISTRATION CHECK -->
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

            <!-- AKO JE VEĆ PRIJAVLJEN -->
            <button
              v-if="registrations[workshop.ID_workshop]"
              @click="handleCancel(workshop.ID_workshop, workshop.title)"
              class="text-xs font-medium text-gray-400 hover:text-red-500 uppercase tracking-wide"
            >
              Odustani
            </button>

            <!-- AKO NIJE PRIJAVLJEN I IMA MJESTA -->
            <button
              v-else-if="getFreeSpots(workshop) > 0"
              @click="handleRegister(workshop.ID_workshop)"
              class="text-xs font-medium text-green-600 hover:text-green-800 uppercase tracking-wide"
            >
              Prijavi se
            </button>

            <!-- AKO JE PUNO → WAITING LIST -->
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'

const BASE_URL = 'http://127.0.0.1:8000'

const workshops = ref([])
const error = ref(null)

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

/* refresh */
const refreshWorkshops = async () => {
  await fetchWorkshops()
  await checkAllRegistrations()
}

/* key: workshopId -> true/false */
const registrations = ref({})

/* ---------------- DATE ---------------- */
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
      error.value = "Trenutno nema aktivnih radionica."
    }
  } catch {
    error.value = "Nije moguće kontaktirati server."
  }
}

/* ---------------- CHECK REGISTRATION ---------------- */
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

    if (!res.ok) throw new Error()

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
  const list = [...workshops.value]
  await Promise.all(list.map(w => checkRegistration(w.ID_workshop)))
}

/* ---------------- REGISTER ---------------- */
const handleRegister = async (workshopId) => {
  try {
    const user = JSON.parse(localStorage.getItem('user'))

    // 🔴 zaštita
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
        previous_experience: "",
        github_profile: ""
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

    if (!res.ok) throw new Error(data.detail)

    await Swal.fire(
      'Uspjeh',
      'Dodani ste na listu čekanja.',
      'success'
    )

    await refreshWorkshops()
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', err.message || 'Nešto nije u redu.', 'error')
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

    if (response.ok) {
      await Swal.fire('Otkazano', 'Prijava je poništena.', 'success')
      await refreshWorkshops()
    } else {
      const err = await response.json()
      Swal.fire('Greška', err.detail || 'Neuspješno otkazivanje.', 'error')
    }
  } catch (err) {
    if (err.message === 'NO_TOKEN') return
    Swal.fire('Greška', 'Server nije dostupan.', 'error')
  }
}

/* ---------------- INIT ---------------- */
onMounted(async () => {
  await refreshWorkshops()
})
</script>