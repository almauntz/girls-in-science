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

              <button
                v-if="registrations[workshop.ID_workshop]"
                @click="handleCancel(workshop.ID_workshop, workshop.title)"
                class="text-xs font-medium text-gray-400 hover:text-red-500 uppercase tracking-wide"
              >
                Odustani
              </button>
            </div>
          </div>
        </div>

        <div v-else>
          <CalendarView :workshops="workshops" :registrations="registrations" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'
import CalendarView from './Calendar.vue' // DODATO: Import komponente

const workshops = ref([])
const error = ref(null)
const viewType = ref('list') // DODATO: Stanje prikaza

/*MAHIR refresh*/
const refreshWorkshops = async () => {
  await fetchWorkshops()
  await checkAllRegistrations()
}

const registrations = ref({})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${String(d.getDate()).padStart(2, '0')}.${String(
    d.getMonth() + 1
  ).padStart(2, '0')}.${d.getFullYear()}`
}

const getRegisteredCount = (w) => w.registered_count ?? 0

const getFreeSpots = (w) => {
  if (w.free_spots !== undefined) return w.free_spots
  return (w.capacity ?? 0) - getRegisteredCount(w)
}

const getCapacityClass = (w) =>
  getFreeSpots(w) > 0 ? 'text-green-600' : 'text-red-500'

const fetchWorkshops = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/workshops/active')
    const data = await res.json()

    workshops.value = Array.isArray(data) ? data : []
    if (!Array.isArray(data)) error.value = "Trenutno nema aktivnih radionica."
  } catch {
    error.value = "Nije moguće kontaktirati server."
  }
}

const checkRegistration = async (workshopId) => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(
      `http://127.0.0.1:8000/workshops/registration/check/${workshopId}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    const data = await res.json()
    registrations.value[workshopId] = data.registered
  } catch (err) {
    registrations.value[workshopId] = false
  }
}

const checkAllRegistrations = async () => {
  await Promise.all(
    workshops.value.map(w => checkRegistration(w.ID_workshop))
  )
}

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
    const token = localStorage.getItem('token')
    const response = await fetch(
      `http://127.0.0.1:8000/workshops/cancellation/${id}`,
      {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`
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
  } catch {
    Swal.fire('Greška', 'Server nije dostupan.', 'error')
  }
}

onMounted(async () => {
   await refreshWorkshops()
})
</script>