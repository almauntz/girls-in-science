<template>
  <div class="min-h-screen bg-purple-100">
    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Pronađi edukativne radionice</h1>
    </div>

    <div class="py-12 px-4 max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-10">Aktivne radionice</h2>

      <p v-if="error" class="text-center text-gray-500">{{ error }}</p>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="workshop in workshops" :key="workshop.ID_workshop" 
             class="bg-white rounded-xl shadow-md p-6 border-t-4 border-purple-500">
          <h3 class="font-bold text-xl mb-2">{{ workshop.title }}</h3>
          <p class="text-sm text-gray-400">Lokacija: {{ workshop.location }}</p>
          <div class="mt-2 text-sm">
            <span class="text-gray-600">Slobodna mjesta: </span>
            <span :class="workshop.free_spots === 0 ? 'text-red-500 font-bold' : 'text-green-600 font-bold'">
            {{ workshop.free_spots }} / {{ workshop.capacity }}
            </span>
          </div>
          <div class="mt-6 flex justify-between items-center border-t pt-4">
            <router-link :to="`/workshops/${workshop.ID_workshop}`" class="font-bold text-purple-600">Saznaj više →</router-link>
            
            <button @click="handleCancel(workshop.ID_workshop, workshop.title)" 
                    class="text-xs font-bold text-red-400 hover:text-red-600 uppercase">
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