<template>
  <div>

<!-- HERO -->
<div
  class="w-full h-[320px]"
  style="background: linear-gradient(to right, #d0c8f9, #F9DBE7);"
>
  <div class="max-w-6xl mx-auto h-full flex items-center justify-center gap-8">

    <!-- Lijeva strana -->
    <div class="w-[380px]"> 
      <h2
        class="text-[42px] font-semibold leading-none mb-3"
        style="color:#7a3b8f;"
      >
        Postani Mentor
      </h2>

      <p class="text-base leading-relaxed text-gray-800 mb-5">
        Podijeli svoje znanje i iskustvo sa studenticama u STEM oblastima i
        pomozi im u rastu.
      </p>

      <div class="button-wrapper"> 
        <button v-if="!isAdmin" @click="goToApply" class="hero-btn mentor-btn">
          <span class="glass-reflection"></span>
          <span class="btn-text">Postani Mentor</span>
      </button>
      </div>
    </div>

    <!-- Sredina -->
    <div class="w-[240px] flex justify-center">
     <!-- <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 102 83"
        class="w-20 sm:w-28 md:w-36 lg:w-44 h-auto"
      >
        <path fill-rule="evenodd" fill="#7a3b8f" d="M 83.6,36.5 L 79.3,30.3 L 73.4,29.2 L 55.1,39.4 L 54.3,44.9 L 63.5,59.2 L 66.4,56.2 L 59.2,42.2 L 73.5,34.0 L 77.1,34.7 L 78.9,37.5 L 78.0,45.7 L 72.7,56.1 L 65.9,62.4 L 56.7,66.6 L 49.7,62.5 L 46.1,63.1 L 42.3,66.5 L 35.6,64.2 L 28.0,58.5 L 22.1,49.9 L 19.8,37.4 L 21.2,34.9 L 24.7,33.9 L 39.7,42.6 L 32.1,56.3 L 35.7,59.2 L 44.5,44.0 L 42.3,38.3 L 28.2,30.0 L 22.5,29.2 L 16.1,33.4 L 15.1,41.5 L 18.1,52.5 L 24.0,61.3 L 31.7,67.5 L 41.6,71.3 L 45.3,75.8 L 50.0,76.9 L 53.5,75.7 L 56.7,71.4 L 68.4,66.5 L 76.9,58.5 L 82.5,47.2 Z M 48.9,67.0 L 49.6,67.0 L 49.7,67.1 L 50.1,67.1 L 50.5,67.3 L 51.7,68.5 L 51.8,68.7 L 51.8,68.9 L 51.9,69.0 L 51.9,69.5 L 52.0,69.6 L 52.0,69.9 L 51.9,70.0 L 51.9,70.4 L 51.5,71.2 L 51.3,71.4 L 51.3,71.5 L 50.8,72.0 L 50.4,72.2 L 50.2,72.2 L 49.9,72.4 L 49.7,72.4 L 49.6,72.5 L 48.9,72.5 L 47.5,71.8 L 46.9,71.1 L 46.7,70.7 L 46.7,70.5 L 46.6,70.4 L 46.6,70.1 L 46.5,70.0 L 46.5,69.4 L 46.6,69.3 L 46.6,69.0 L 46.7,68.9 L 46.7,68.7 L 46.9,68.3 L 47.5,67.7 L 47.6,67.7 L 47.8,67.5 L 48.1,67.4 L 48.5,67.1 L 48.8,67.1 Z M 63.6,11.0 L 61.6,12.1 L 59.9,13.6 L 59.2,14.6 L 58.1,17.4 L 58.1,20.4 L 59.0,23.0 L 59.8,24.3 L 61.5,25.9 L 63.4,26.9 L 66.3,27.3 L 68.1,27.2 L 70.3,26.6 L 71.5,25.8 L 72.8,24.5 L 73.7,23.3 L 74.6,21.2 L 74.9,18.3 L 74.5,16.6 L 72.9,13.7 L 71.3,12.1 L 69.1,11.0 L 67.5,10.7 Z M 65.8,14.9 L 67.1,15.0 L 68.4,15.5 L 69.1,16.0 L 69.9,16.8 L 70.3,17.6 L 70.3,18.3 L 70.5,18.9 L 70.5,19.6 L 69.9,21.3 L 69.4,21.8 L 68.7,22.2 L 68.3,22.6 L 67.2,23.1 L 65.5,23.1 L 64.6,22.7 L 64.0,22.3 L 62.9,21.2 L 62.4,20.2 L 62.3,19.5 L 62.2,19.4 L 62.3,18.2 L 63.0,16.7 L 63.8,15.9 L 64.1,15.8 L 64.7,15.3 Z M 31.5,10.7 L 29.5,11.0 L 28.5,11.4 L 27.2,12.2 L 25.2,14.2 L 24.0,16.6 L 23.8,19.7 L 24.3,22.4 L 25.3,23.9 L 27.1,25.8 L 28.6,26.7 L 30.0,27.1 L 32.9,27.3 L 34.8,27.0 L 35.9,26.6 L 37.2,25.8 L 38.9,24.1 L 40.0,22.2 L 40.5,20.0 L 40.5,18.1 L 40.1,16.2 L 39.6,15.0 L 38.9,14.0 L 37.3,12.4 L 35.3,11.1 Z M 31.4,15.0 L 33.1,15.0 L 33.7,15.2 L 34.6,15.8 L 35.7,16.9 L 36.1,17.9 L 36.1,18.3 L 36.2,18.4 L 36.2,19.8 L 35.9,20.8 L 35.2,21.7 L 34.0,22.7 L 33.1,23.1 L 31.4,23.1 L 31.3,23.0 L 30.6,22.9 L 29.4,22.0 L 28.9,21.5 L 28.1,19.8 L 28.1,19.0 L 28.0,18.9 L 28.1,18.8 L 28.1,18.3 L 28.9,16.6 L 30.5,15.3 Z" />
      </svg> -->
    </div>

    <!-- Desna strana -->
    <div class="w-[380px] text-right">
      <h2
        class="text-[42px] font-semibold leading-none mb-3"
        style="color:#9a1f61;"
      >
        Studentica Prijava
      </h2>

      <p class="text-base leading-relaxed text-gray-800 mb-5">
        Pronađi idealnu mentoricu koja će te voditi kroz tvoj akademski i
        profesionalni put u STEM-u.
      </p>

      
      <div class="button-wrapper">
        <button
          v-if="!isAdmin"
          @click="goToStudentApply"
          class="hero-btn student-btn">
          <span class="glass-reflection"></span>
          <span class="btn-text">Prijavi se kao Studentica</span>
        </button>
      </div>
    </div>

  </div>
</div>


    <!-- Ostatak stranice -->
    <div class="max-w-7xl mx-auto px-6 py-10">

      <!-- Admin dugme -->
      <div class="flex justify-end mb-6" v-if="isAdmin">
      <router-link
        to="/admin/mentor-applications"
        class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Admin Panel
      </router-link>
    </div>

      <!-- Naslov -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Upoznajte Mentorice</h1>
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
  </div>
</template>

<style scoped>
.hero-btn {
  padding: 13px 20px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;
  letter-spacing: 2px;
  color: #fff;
  border: none;
  border-radius: 100px;
  background: none;
  position: relative;
  overflow: hidden;
  z-index: 0;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.btn-text {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.hero-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 150%;
  height: 100%;
background: conic-gradient(
  from 0deg,
  #e7a1c8,
  #d78fbe,
  #c97fcf,
  #b873dc,
  #a96fe6,
  #b07ae8,
  #c18ae3,
  #d78fbe,
  #e7a1c8
);
  padding-bottom: 150%; 
  transform: translate(-50%, -50%);
  z-index: -1;
  animation: rotate 4s linear infinite;
}

.hero-btn::after{
  content: '';
  position: absolute;
  inset: 3px;
  background: #7049b3;
  border-radius: 97px;
  z-index: -1;
  transition: background 0.5s ease, opacity 0.5s ease; 
}

.glass-reflection {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 50%;
  background: linear-gradient(to bottom, rgba(255,255,255,0.15), transparent);
  transform: translate(-50%, -50%) rotate(25deg);
  animation: shine 2s linear infinite;
  z-index: 1;
  pointer-events: none;
}

.button-wrapper:hover .hero-btn {
     transform: scale(1.03) translateY(-0.5px); 
}

.button-wrapper:hover .hero-btn::after {
  opacity: 0.1;
}

@keyframes rotate {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

</style>

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

const goToStudentApply = () => {
  router.push('/student/apply')
}

onMounted(async () => {
  // Provjeri ulogu iz tokena
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (payload.role === 'mentor') {
        router.push('/mentoring/my-applications')
        return
      }
    } catch {}
  }

  // Normalan tok za member/admin
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