<template>
  <div class="py-8">

    <!-- Button za aplikaciju -->
    <div class="mb-8">
      <button
        @click="goToApply"
        class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
      >
        Postani mentor
      </button>
    </div>

    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Mentorice</h1>
      <p class="text-gray-500 mt-2">
        Upoznajte stručnjakinje koje nude mentorstvo studenticama u STEM oblastima.
      </p>
    </div>

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
    <div v-else-if="mentors.length === 0" class="text-center py-20">
      <p class="text-gray-400 text-xl">Trenutno nema dostupnih mentora.</p>
    </div>

    <!-- Grid kartica -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <MentorCard
        v-for="mentor in mentors"
        :key="mentor.id"
        :mentor="mentor"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMentors } from '../../services/mentoring.js'
import MentorCard from '../../components/MentorCard.vue'

const router = useRouter()
const mentors = ref([])
const loading = ref(true)
const error = ref(false)

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