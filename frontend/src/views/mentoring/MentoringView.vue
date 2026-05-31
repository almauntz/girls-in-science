<template>
  <div class="py-8">
    <!-- Button za aplikaciju + Admin Panel dugme -->
    <div class="flex items-center justify-between mb-8">
      <button
        v-if="!isAdmin"
        @click="goToApply"
        class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Postani mentor
      </button>
      <router-link
        v-if="isAdmin"
        to="/admin/mentor-applications"
        class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Admin Panel
      </router-link>
    </div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Mentorice</h1>
      <p class="text-gray-500 mt-2">
        Upoznajte stručnjakinje koje nude mentorstvo studenticama u STEM oblastima.
      </p>
    </div>

    <!-- Filter sekcija -->
    <div class="mb-6">
      <p class="text-sm text-gray-500 uppercase mb-3">Filter po oblasti</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="oblast in oblasti"
          :key="oblast"
          @click="activeFilter = activeFilter === oblast ? null : oblast"
          :class="activeFilter === oblast
            ? 'bg-purple-600 text-white border border-purple-600'
            : 'bg-white text-gray-700 border border-gray-300 hover:border-purple-400'"
          class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors duration-200">
          {{ oblast }}
        </button>
        <button
          v-if="activeFilter"
          @click="activeFilter = null"
          class="text-xs text-gray-400 underline self-center ml-2">
          Ukloni filtere ✗
        </button>
      </div>
    </div>

    <!-- Broj rezultata -->
    <p class="text-sm text-gray-400 mb-4">
      Rezultati: {{ resultCount }}
    </p>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
      <span class="ml-4 text-gray-500">Učitavanje...</span>
    </div>
    <!-- Greška -->
    <div v-else-if="error" class="text-center py-20">
      <p class="text-red-500 text-lg">⚠️ Greška pri učitavanju podataka.</p>
      <p class="text-gray-400 mt-1">Pokušajte ponovo kasnije.</p>
    </div>
    <!-- Prazno stanje -->
    <div v-else-if="filteredMentors.length === 0" class="text-center py-20">
      <p class="text-gray-400 text-xl">
        {{ activeFilter ? `Nema mentorica u oblasti "${activeFilter}".` : 'Trenutno nema dostupnih mentora.' }}
      </p>
    </div>
    <!-- Grid kartica -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <MentorCard
        v-for="mentor in filteredMentors"
        :key="mentor.id"
        :mentor="mentor"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMentors } from '../../services/mentoring.js'
import MentorCard from '../../components/MentorCard.vue'

const router = useRouter()
const mentors = ref([])
const loading = ref(true)
const error = ref(false)

const oblasti = ref([
  'IT',
  'Hemija',
  'Matematika',
  'Biologija',
  'Fizika',
  'Softverski inženjering',
  'Mašinsko učenje',
  'Bioinformatika',
  'Telekomunikacije'
])
const activeFilter = ref(null)

const filteredMentors = computed(() => {
  if (!activeFilter.value) return mentors.value
  return mentors.value.filter(m => m.field_of_expertise === activeFilter.value)
})

const resultCount = computed(() => filteredMentors.value.length)

const isAdmin = computed(() => {
  const token = localStorage.getItem('token')
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role === 'admin'
  } catch {
    return false
  }
})

const goToApply = () => {
  router.push({ name: 'mentor-registration' })
}

onMounted(async () => {
  try {
    const response = await getMentors()
    mentors.value = response.data
  } catch (err) {
    console.error('Greška pri dohvaćanju mentorica:', err)
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>