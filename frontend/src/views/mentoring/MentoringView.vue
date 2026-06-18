<template>
  <div class="py-8">
    <!-- Dugmad gore -->
    <div class="flex items-center justify-between mb-8">
      <button
        v-if="!isAdmin"
        @click="goToApply"
        class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Postani mentor
      </button>
      <router-link
        to="/student/apply"
        class="bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Prijava Studentica
      </router-link>
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

    <!-- Filter panel -->
    <div class="bg-white border border-gray-200 rounded-xl p-5 mb-6 space-y-4">

      <!-- Filter po oblasti -->
      <div>
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Oblast</p>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="oblast in oblasti"
            :key="oblast"
            @click="activeOblast = activeOblast === oblast ? null : oblast"
            :class="activeOblast === oblast
              ? 'bg-purple-600 text-white border-purple-600'
              : 'bg-white text-gray-700 border-gray-300 hover:border-purple-400'"
            class="px-4 py-1.5 rounded-full text-sm font-medium border transition-colors duration-200"
          >
            {{ prevediOblast(oblast) }}
          </button>
        </div>
      </div>

      <!-- Filter po formatu sesije -->
      <div>
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Format sesije</p>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="format in formati"
            :key="format.value"
            @click="activeFormat = activeFormat === format.value ? null : format.value"
            :class="activeFormat === format.value
              ? 'bg-purple-600 text-white border-purple-600'
              : 'bg-white text-gray-700 border-gray-300 hover:border-purple-400'"
            class="px-4 py-1.5 rounded-full text-sm font-medium border transition-colors duration-200"
          >
            {{ format.label }}
          </button>
        </div>
      </div>

      <!-- Ukloni filtere -->
      <div v-if="activeOblast || activeFormat">
        <button
          @click="activeOblast = null; activeFormat = null"
          class="text-xs text-gray-400 hover:text-gray-600 underline"
        >
          Ukloni sve filtere ✗
        </button>
      </div>
    </div>

    <!-- Broj rezultata -->
    <p class="text-sm text-gray-400 mb-4">Rezultati: {{ resultCount }}</p>

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
      <p class="text-gray-400 text-xl">Nema mentorica koje odgovaraju odabranim filterima.</p>
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

const activeOblast = ref(null)
const activeFormat = ref(null)

// Mapa prijevoda oblast (engleski → bosanski)
const prijevodOblasti = {
  'IT': 'IT',
  'Biology': 'Biologija',
  'Biologija': 'Biologija',
  'Chemistry': 'Hemija',
  'Hemija': 'Hemija',
  'Mathematics': 'Matematika',
  'Matematika': 'Matematika',
  'Physics': 'Fizika',
  'Fizika': 'Fizika',
  'Software Engineering': 'Softverski inženjering',
  'Softverski inženjering': 'Softverski inženjering',
  'Machine Learning': 'Mašinsko učenje',
  'Mašinsko učenje': 'Mašinsko učenje',
  'Bioinformatics': 'Bioinformatika',
  'Bioinformatika': 'Bioinformatika',
  'Telecommunications': 'Telekomunikacije',
  'Telekomunikacije': 'Telekomunikacije',
}

function prevediOblast(oblast) {
  return prijevodOblasti[oblast] || oblast
}

// Oblasti dinamički iz stvarnih podataka mentorica
const oblasti = computed(() => {
  const unique = [...new Set(mentors.value.map(m => m.field_of_expertise).filter(Boolean))]
  return unique.sort()
})

// Formati sesije
const formati = [
  { value: 'Online', label: '💻 Online' },
  { value: 'Offline', label: '🤝 Uživo' },
  { value: 'Hybrid', label: '🔄 Hybrid' },
]

const filteredMentors = computed(() => {
  return mentors.value.filter(m => {
    const oblastMatch = !activeOblast.value || m.field_of_expertise === activeOblast.value
    const formatMatch = !activeFormat.value ||
      (m.preferred_session_format || '').toLowerCase().includes(activeFormat.value.toLowerCase())
    return oblastMatch && formatMatch
  })
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