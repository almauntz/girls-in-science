<template>
  <div class="min-h-screen bg-purple-100">

    <p v-if="loading" class="text-center text-gray-500 py-20">Učitavanje...</p>

    <p v-else-if="error" class="text-center text-gray-500 py-20">{{ error }}</p>

    <div v-else>
      <div class="text-center py-12 px-4">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">{{ workshop.title }}</h1>
      </div>

      <hr class="border-gray-300" />

      <div class="max-w-5xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-2 gap-12">

        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Opis radionice</h2>
          <p class="text-gray-600 leading-relaxed whitespace-pre-line">{{ workshop.description }}</p>

          <div class="mt-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Organizator</h2>
            <p class="text-gray-800"><span class="font-medium">Ime i prezime:</span> {{ workshop.organizer_name }}</p>
            <p class="text-gray-800"><span class="font-medium">Email:</span> {{ workshop.organizer_email }}</p>
          </div>
        </div>

        <div class="flex flex-col gap-6">
          <h2 class="text-2xl font-bold text-gray-800">Detalji radionice</h2>
          <p class="text-gray-500">Važne informacije na jednom mjestu prije prijave.</p>

          <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
            <div class="flex-1">
              <p class="font-medium text-gray-800">Datum početka</p>
              <p class="text-sm text-gray-400">{{ formatDate(workshop.date) }}</p>
            </div>
            <p class="font-bold text-gray-700">{{ formatTime(workshop.date) }}</p>
          </div>

          <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
            <div class="flex-1">
              <p class="font-medium text-gray-800">Datum završetka</p>
              <p class="text-sm text-gray-400">{{ formatDate(workshop.end_time) }}</p>
            </div>
            <p class="font-bold text-gray-700">{{ formatTime(workshop.end_time) }}</p>
          </div>

          <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
            <div class="flex-1">
              <p class="font-medium text-gray-800">Lokacija</p>
              <p class="text-sm text-gray-400">{{ workshop.location }}</p>
            </div>
          </div>

          <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
            <div class="flex-1">
              <p class="font-medium text-gray-800">Kapacitet</p>
              <p class="text-sm text-gray-400">Broj mjesta</p>
            </div>
            <p class="font-bold text-gray-700">{{ workshop.capacity }} polaznica</p>
          </div>

          <div class="flex items-center gap-4">
            <div class="flex-1">
              <p class="font-medium text-gray-800">Slobodna mjesta</p>
              <p class="text-sm text-gray-400">Još uvijek dostupno</p>
            </div>
            <p
              class="font-bold"
              :class="workshop.free_spots === 0 ? 'text-red-500' : 'text-green-600'"
            >
              {{ workshop.free_spots === 0 ? 'Popunjeno' : workshop.free_spots + ' mjesta' }}
            </p>
          </div>

          <div class="flex gap-4 mt-4">
            <router-link
              to="/workshops"
              class="px-5 py-2 rounded-lg border border-gray-400 text-gray-600 hover:bg-gray-200"
            >
              Nazad
            </router-link>
            
            <button
              :disabled="workshop.free_spots === 0 || workshop.status !== 'upcoming'"
              class="px-5 py-2 rounded-lg bg-blue-600 text-white font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="showForm = true" 
            >
              {{ workshop.free_spots === 0 ? 'Nema mjesta' : 'Prijavi se' }}
            </button>

            <button
              :disabled="workshop.free_spots === 0 || workshop.status !== 'upcoming'"
              class="px-5 py-2 rounded-lg bg-green-600 text-white font-bold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="quickJoin" 
            >
              {{ workshop.free_spots === 0 ? 'Nema mjesta' : 'Pridruži se' }}
            </button>
          </div>
        </div> </div>

        <div v-if="showForm" class="mt-12 border-t border-gray-200 bg-white pt-12">
          <WorkshopRegistrationForm @cancel="showForm = false" @success="handleSuccess" />
        </div>

    </div> </div> </template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import WorkshopRegistrationForm from './WorkshopRegistrationForm.vue'
import { getWorkshopDetails } from '../../services/api.js'
export default {
  components: {
    WorkshopRegistrationForm
  },
  setup() {
    const route = useRoute()
    const workshop = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)

    const formatDate = (date) => {
      if (!date) return ''
      return new Date(date).toLocaleDateString('hr-HR', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      })
    }

    const formatTime = (date) => {
      if (!date) return ''
      return new Date(date).toLocaleTimeString('hr-HR', {
        hour: '2-digit', minute: '2-digit'
      })
    }

    const fetchWorkshop = async () => {
  try {
    loading.value = true
    const workshopId = route.params.id
    
    // Pozivamo pravi backend umjesto izmišljenih podataka
    const response = await fetch(`http://127.0.0.1:8000/workshops/${workshopId}`)
    
    if (!response.ok) throw new Error("Radionica nije pronađena")
    
    const data = await response.json()
    workshop.value = data
    error.value = null
  } catch (err) {
    console.error(err)
    error.value = 'Greška pri učitavanju detalja radionice.'
  } finally {
    loading.value = false
  }
}

    const quickJoin = () => {
      alert('Trebate popuniti formu sa detaljima. Kliknite na Prijavi se.')
    }

    const handleSuccess = () => {
      showForm.value = false
      alert('Uspješno ste se prijavili na radionicu!')
    }

    onMounted(() => {
      fetchWorkshop()
    })

    return {
      workshop,
      loading,
      error,
      quickJoin,
      showForm,
      formatDate,
      formatTime,
      handleSuccess
    }
  }
}
</script>