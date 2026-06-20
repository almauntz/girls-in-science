<template>
  <div>

    <!-- HERO -->
    <div class="w-full h-[320px]" style="background: linear-gradient(to right, #d0c8f9, #F9DBE7);">
      <div class="max-w-6xl mx-auto h-full flex items-center justify-center gap-8">

        <div class="w-[380px]">
          <h2 class="text-[42px] font-semibold leading-none mb-3" style="color:#7a3b8f;">
            Postani Mentor
          </h2>
          <p class="text-base leading-relaxed text-gray-800 mb-5">
            Podijeli svoje znanje i iskustvo sa studenticama u STEM oblastima i pomozi im u rastu.
          </p>
          <div class="button-wrapper">
            <button v-if="!isAdmin" @click="goToApply" class="hero-btn mentor-btn">
              <span class="glass-reflection"></span>
              <span class="btn-text">Postani Mentor</span>
            </button>
          </div>
        </div>

        <div class="w-[240px] flex justify-center"></div>

        <div class="w-[380px] text-right">
          <h2 class="text-[42px] font-semibold leading-none mb-3" style="color:#9a1f61;">
            Studentica Prijava
          </h2>
          <p class="text-base leading-relaxed text-gray-800 mb-5">
            Pronađi idealnu mentoricu koja će te voditi kroz tvoj akademski i profesionalni put u STEM-u.
          </p>
          <div class="button-wrapper">
            <button v-if="!isAdmin" @click="goToStudentApply" class="hero-btn student-btn">
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

      <!-- Filter panel -->
      <div class="bg-white border border-gray-200 rounded-xl p-5 mb-6 space-y-4">

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

        <div v-if="activeOblast || activeFormat">
          <button
            @click="activeOblast = null; activeFormat = null"
            class="text-xs text-gray-400 hover:text-gray-600 underline"
          >
            Ukloni sve filtere ✗
          </button>
        </div>
      </div>

      <p class="text-sm text-gray-400 mb-4">Rezultati: {{ resultCount }}</p>

      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
        <span class="ml-4 text-gray-500">Učitavanje...</span>
      </div>

      <div v-else-if="error" class="text-center py-20">
        <p class="text-red-500 text-lg">⚠️ Greška pri učitavanju podataka.</p>
        <p class="text-gray-400 mt-1">Pokušajte ponovo kasnije.</p>
      </div>

      <div v-else-if="filteredMentors.length === 0" class="text-center py-20">
        <p class="text-gray-400 text-xl">Nema mentorica koje odgovaraju odabranim filterima.</p>
      </div>

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
  background: conic-gradient(from 0deg, #e7a1c8, #d78fbe, #c97fcf, #b873dc, #a96fe6, #b07ae8, #c18ae3, #d78fbe, #e7a1c8);
  padding-bottom: 150%;
  transform: translate(-50%, -50%);
  z-index: -1;
  animation: rotate 4s linear infinite;
}
.hero-btn::after {
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
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
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

const activeOblast = ref(null)
const activeFormat = ref(null)

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

const oblasti = computed(() => {
  const unique = [...new Set(mentors.value.map(m => m.field_of_expertise).filter(Boolean))]
  return unique.sort()
})

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

const goToApply = () => router.push({ name: 'mentor-registration' })
const goToStudentApply = () => router.push('/student/apply')

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