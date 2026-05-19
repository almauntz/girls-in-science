<template>
  <div class="min-h-screen bg-purple-100">
    <p v-if="loading" class="text-center text-gray-500 py-20 font-medium">Učitavanje...</p>
    <p v-else-if="error" class="text-center text-red-500 py-20 font-medium">{{ error }}</p>

    <div v-else>
      <div class="text-center py-12 px-4">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">{{ workshop.title }}</h1>
      </div>

      <hr class="border-gray-300" />

      <div class="max-w-5xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-2 gap-12">
        <!-- Opis radionice -->
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Opis radionice</h2>
          <p class="text-gray-600 leading-relaxed">
            {{ workshop.description }}
          </p>

          <!-- Organizator -->
          <div class="mt-6">
            <h3 class="text-xl font-bold text-gray-800 mb-2">Organizator</h3>
            <p class="text-sm text-gray-600"><strong>Ime i prezime:</strong> {{ workshop.organizer_name }}</p>
            <p class="text-sm text-gray-600"><strong>Email:</strong> {{ workshop.organizer_email }}</p>
          </div>
        </div>

        <!-- Detalji radionice -->
        <div class="flex flex-col gap-6">
          <h2 class="text-2xl font-bold text-gray-800">Detalji radionice</h2>
          <p class="text-sm text-gray-500">Važne informacije na jednom mjestu prije prijave.</p>

          <div class="space-y-4">
            <div>
              <p class="font-semibold text-gray-800">Datum početka</p>
              <p class="text-sm text-gray-600">{{ formatDate(workshop.date) }}</p>
            </div>

            <div>
              <p class="font-semibold text-gray-800">Datum završetka</p>
              <p class="text-sm text-gray-600">{{ formatDate(workshop.end_time) }}</p>
            </div>

            <div>
              <p class="font-semibold text-gray-800">Kapacitet</p>
              <p class="text-sm text-gray-600">{{ workshop.capacity }} polaznika</p>
            </div>

            <div>
              <p class="font-semibold text-gray-800">Slobodna mjesta</p>
              <p class="text-sm" :class="workshop.free_spots === 0 ? 'text-red-500' : 'text-green-600 font-bold'">
                {{ workshop.free_spots }}
              </p>
            </div>

            <div class="flex gap-4 pt-4">
              <router-link to="/workshops" class="px-5 py-2 border-2 border-gray-300 rounded-lg font-bold">Nazad</router-link>
              <button 
                @click="showForm = true"
                :disabled="workshop.free_spots === 0 || workshop.status !== 'upcoming'"
                class="px-5 py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 disabled:opacity-50"
              >
                Prijavi se
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="showForm" class="mt-8 pb-20">
        <WorkshopRegistrationForm @cancel="showForm = false" @success="handleSuccess" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import WorkshopRegistrationForm from './WorkshopRegistrationForm.vue'

export default {
  components: { WorkshopRegistrationForm },
  setup() {
    const route = useRoute()
    const workshop = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)

    const fetchWorkshop = async () => {
      try {
        loading.value = true
        const response = await fetch(`http://127.0.0.1:8000/workshops/${route.params.id}`)
        if (!response.ok) throw new Error("Radionica nije pronađena")
        workshop.value = await response.json()
      } catch (err) { error.value = 'Greška pri učitavanju.' }
      finally { loading.value = false }
    }

    const handleSuccess = () => {
      showForm.value = false
      fetchWorkshop()
    }

    // funkcija za promjenu prikaza datuma
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const d = new Date(dateString)
      const day = String(d.getDate()).padStart(2, '0')
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const year = d.getFullYear()
      return `${day}.${month}.${year}`   
    }

    onMounted(fetchWorkshop)
    return { workshop, loading, error, showForm, handleSuccess, formatDate }
  }
}
</script>
