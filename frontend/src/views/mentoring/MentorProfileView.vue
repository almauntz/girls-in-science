<template>
  <div class="max-w-2xl mx-auto p-4">

    <!-- Dugme Nazad -->
    <button @click="router.back()" class="mb-4 text-sm text-blue-600 hover:underline">
      ← Nazad
    </button>

    <div v-if="loading" class="text-center py-10">Učitavanje...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

    <div v-else-if="mentor">

      <!-- Header -->
      <div class="border rounded-xl p-6 mb-4">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-4">
            <img
              :src="mentor.profile_img_url || 'https://placehold.co/80x80'"
              class="w-20 h-20 rounded-full object-cover"
            />
            <div>
              <h1 class="text-xl font-bold">{{ mentor.full_name }}</h1>
              <!-- Tagovi za oblast ekspertize -->
              <div class="flex items-center gap-2 mt-1 flex-wrap">
                <span class="text-sm text-gray-500">Oblast ekspertize:</span>
                <span
                  v-for="(tag, index) in expertiseTags"
                  :key="index"
                  class="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <!-- LinkedIn -->
          <a v-if="mentor.linkedin_url" :href="mentor.linkedin_url" target="_blank"
            class="bg-blue-600 text-white rounded px-3 py-2 text-sm font-bold hover:bg-blue-700 transition">
            in
          </a>
        </div>

        <!-- Popunjenost i format -->
        <div class="flex gap-4 mt-4">
          <div class="border rounded-lg px-4 py-2 text-sm flex items-center gap-2">
            <!-- Zeleni krug ako ima mjesta, crveni ako je puno -->
            <span
              :class="isFull ? 'bg-red-500' : 'bg-green-500'"
              class="w-3 h-3 rounded-full inline-block"
            ></span>
            <span class="text-gray-500">Popunjeno </span>
            <span
              :class="isFull ? 'text-red-600 font-semibold' : 'text-green-600 font-semibold'"
            >
              {{ mentor.current_applications_count }}/{{ mentor.max_mentees }}
            </span>
          </div>
          <div class="border rounded-lg px-4 py-2 text-sm">
            <span class="text-gray-500">Format sesije: </span>
            <span class="font-semibold">{{ mentor.preferred_session_format || 'Online' }}</span>
          </div>
        </div>
      </div>

      <!-- Biografija -->
      <div class="border rounded-xl p-6 mb-4">
        <h2 class="font-bold text-lg mb-2">Biografija</h2>
        <p class="text-gray-700">{{ mentor.bio || 'Nema biografije.' }}</p>
      </div>

      <!-- Timeline iskustva -->
      <div class="border rounded-xl p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="font-bold text-lg">Iskustvo</h2>
          <div class="flex items-center gap-2">
            <span class="bg-gray-800 text-white text-sm px-3 py-1 rounded-full">
              {{ mentor.years_of_experience || '—' }} + godina
            </span>
          </div>
        </div>
        <!-- Timeline -->
        <div class="flex gap-4">
          <div class="flex flex-col items-center">
            <div class="w-3 h-3 rounded-full bg-blue-500 mt-1"></div>
            <div class="w-0.5 flex-1 bg-gray-200 mt-1"></div>
          </div>
          <div class="pb-4">
            <p class="font-semibold">{{ mentor.position || 'Pozicija nije navedena' }}</p>
            <p class="text-sm text-gray-500">{{ mentor.institution || '' }}</p>
          </div>
        </div>
      </div>

      <!-- Glavno dugme -->
      <button
        :disabled="!mentor.is_available"
        :class="mentor.is_available
          ? 'w-full bg-purple-600 text-white py-3 rounded-xl font-semibold hover:bg-purple-700 transition'
          : 'w-full bg-gray-300 text-gray-500 py-3 rounded-xl font-semibold cursor-not-allowed'"
      >
        {{ mentor.is_available ? 'Zatraži mentorstvo' : 'Nedostupno' }}
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const mentor = ref(null)
const loading = ref(true)
const error = ref(null)

// Dijeli field_of_expertise po zarezu u više tagova
const expertiseTags = computed(() => {
  if (!mentor.value?.field_of_expertise) return []
  return mentor.value.field_of_expertise.split(',').map(t => t.trim())
})

// Je li mentor potpuno popunjen
const isFull = computed(() => {
  if (!mentor.value) return false
  return mentor.value.current_applications_count >= mentor.value.max_mentees
})

onMounted(async () => {
  // FEJK PODACI - obriši ovo kad backend bude imao prave podatke
  mentor.value = {
    id: 1,
    full_name: "Amina Hodžić",
    field_of_expertise: "IT i digitalne tehnologije, Data, AI i digitalna transformacija",
    bio: "Imam 6 godina iskustva u softverskom razvoju. Radila sam na projektima u oblasti web razvoja i mašinskog učenja.",
    linkedin_url: "https://linkedin.com",
    preferred_session_format: "Online",
    max_mentees: 3,
    current_applications_count: 3,
    is_available: true,
    profile_img_url: null,
    position: "Software Engineer",
    institution: "Microsoft",
    years_of_experience: "6"
  }
  loading.value = false
})
</script>