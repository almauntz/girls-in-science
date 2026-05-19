<template>
  <div class="min-h-screen bg-purple-100">
    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Pronađi edukativne radionice</h1>
      <p class="text-gray-600">Izaberi radionicu i prijavi se u par klikova.</p>
    </div>

    <div class="py-12 px-4 max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Aktivne radionice</h2>
      <p class="text-center text-gray-500 mb-10">Klikom na Saznaj više pogledajte detaljne informacije o radionici</p>

      <p v-if="error" class="text-center text-gray-500">{{ error }}</p>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="workshop in workshops" :key="workshop.ID_workshop"
             class="bg-white rounded-xl p-5 border border-gray-100 flex flex-col gap-2">

          <h3 class="font-medium text-base text-gray-800">{{ workshop.title }}</h3>

          <p class="text-sm text-gray-400">Datum: {{ formatDate(workshop.date) }}</p>

          <p class="text-sm text-gray-400">Lokacija: {{ workshop.location }}</p>

          <hr class="border-gray-100 mt-2">

          <div class="flex justify-between items-center">
            <router-link :to="`/workshops/${workshop.ID_workshop}`"
                         class="text-sm font-medium text-purple-600">
              Saznaj više →
            </router-link>
            <button @click="handleCancel(workshop.ID_workshop, workshop.title)"
                    class="text-xs font-medium text-gray-400 hover:text-red-500 uppercase tracking-wide">
              Odustani
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

const workshops = ref([])
const error = ref(null)

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}.${month}.${year}`; // rezultat: 12.09.2026
}


const fetchWorkshops = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/workshops/active')
    const data = await response.json()
    if (Array.isArray(data)) workshops.value = data
    else error.value = "Trenutno nema aktivnih radionica."
  } catch (err) { error.value = "Nije moguće kontaktirati server." }
}

const handleCancel = async (id, title) => {
  const result = await Swal.fire({
    title: 'Otkazivanje?',
    text: `Želite li odustati od radionice: ${title}?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Da, otkaži',
    confirmButtonColor: '#d33'
  })

  if (result.isConfirmed) {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://127.0.0.1:8000/workshops/registration/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      Swal.fire('Otkazano', 'Prijava je poništena.', 'success')
      fetchWorkshops()
    } else {
      Swal.fire('Ups!', 'Izgleda da niste ni prijavljeni na ovu radionicu.', 'error')
    }
  }
}

onMounted(fetchWorkshops)
</script>