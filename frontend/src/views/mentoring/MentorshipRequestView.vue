<template>
  <div class="max-w-2xl mx-auto p-4">

    <!-- Header -->
    <div class="border rounded-xl p-4 mb-4">
      <button @click="router.back()" class="text-sm text-gray-700 hover:text-black font-semibold">
        ← Profil mentorice
      </button>
    </div>

    <!-- Info o mentorici -->
    <div class="border rounded-xl p-6 mb-4" v-if="mentor">
      <div class="flex items-center gap-4">
        <img
          :src="mentor.profile_img_url || 'https://placehold.co/80x80'"
          class="w-16 h-16 rounded-full object-cover"
        />
        <div>
          <h1 class="text-lg font-bold">{{ mentor.full_name }}</h1>
          <div class="flex items-center gap-2 mt-1 flex-wrap">
            <span class="text-sm text-gray-500">Oblast ekspertize:</span>
            <span
              v-for="(tag, index) in expertiseTags"
              :key="index"
              class="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Forma -->
    <div class="border rounded-xl p-6 mb-4">

      <div class="flex gap-4">
        <!-- Lijeva strana - textarea polja -->
        <div class="flex-1">
          <textarea
            v-model="expectations"
            placeholder="Očekivanja - Šta očekujete od učešća u mentorskom programu?"
            class="w-full border rounded-lg p-3 text-sm resize-none h-24 mb-3 focus:outline-none focus:ring-2 focus:ring-purple-400"
          ></textarea>

          <textarea
            v-model="skills"
            placeholder="Vještine - Koje vještine ili znanja želite unaprijediti?"
            class="w-full border rounded-lg p-3 text-sm resize-none h-24 focus:outline-none focus:ring-2 focus:ring-purple-400"
          ></textarea>
        </div>

        <!-- Desna strana - CV upload -->
        <div class="flex flex-col items-center justify-center w-32">
          <label class="cursor-pointer border rounded-lg w-20 h-20 flex items-center justify-center bg-gray-100 hover:bg-gray-200 transition mb-2">
            <span class="text-2xl">📄</span>
            <input type="file" accept=".pdf,.doc,.docx" class="hidden" @change="handleFileSelect" />
          </label>
          <p class="text-xs text-gray-500 text-center">Priložite CV - samo PDF ili DOC format</p>
          <p v-if="cvFile" class="text-xs text-green-600 mt-1 text-center font-semibold">{{ cvFile.name }}</p>
          <p v-if="fileError" class="text-xs text-red-500 mt-1 text-center">{{ fileError }}</p>
        </div>
      </div>

      <!-- Saglasnost -->
      <div class="flex items-center gap-2 mt-4 mb-6">
        <input type="checkbox" v-model="agreed" id="saglasnost" class="w-4 h-4 accent-purple-600" />
        <label for="saglasnost" class="text-sm text-gray-700">Saglasnost za minimalno 2 sesije</label>
      </div>

      <!-- Dugme + Status -->
      <div class="flex items-center gap-4">
        <button
          @click="submitRequest"
          :disabled="!isFormValid || buttonState === 'loading' || buttonState === 'success' || buttonState === 'pending'"
          :class="{
            'flex-1 py-3 rounded-xl font-semibold transition': true,
            'bg-purple-600 text-white hover:bg-purple-700': buttonState === 'idle' && isFormValid,
            'bg-gray-200 text-gray-400 cursor-not-allowed': buttonState === 'idle' && !isFormValid,
            'bg-gray-400 text-white cursor-not-allowed': buttonState === 'loading',
            'bg-green-600 text-white cursor-not-allowed': buttonState === 'success',
            'bg-red-600 text-white': buttonState === 'error',
            'bg-gray-300 text-gray-500 cursor-not-allowed': buttonState === 'pending',
          }"
        >
          <span v-if="buttonState === 'idle'">Pošalji zahtjev</span>
          <span v-else-if="buttonState === 'loading'">⏳ Slanje...</span>
          <span v-else-if="buttonState === 'success'">✓ Uspješno poslan zahtjev</span>
          <span v-else-if="buttonState === 'error'">✗ Neuspješan zahtjev</span>
          <span v-else-if="buttonState === 'pending'">Status: Na čekanju</span>
        </button>

        <span v-if="buttonState === 'pending'" class="text-sm text-gray-500">
          Status → na čekanju
        </span>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const mentor = ref(null)
const expectations = ref('')
const skills = ref('')
const cvFile = ref(null)
const fileError = ref('')
const agreed = ref(false)
const buttonState = ref('idle')

const expertiseTags = computed(() => {
  if (!mentor.value?.field_of_expertise) return []
  return mentor.value.field_of_expertise.split(',').map(t => t.trim())
})

const isFormValid = computed(() => {
  return expectations.value.trim() !== '' &&
    skills.value.trim() !== '' &&
    cvFile.value !== null &&
    agreed.value
})

function handleFileSelect(event) {
  const file = event.target.files[0]
  fileError.value = ''
  if (!file) return
  if (file.type !== 'application/pdf' && !file.name.endsWith('.doc') && !file.name.endsWith('.docx')) {
    fileError.value = 'Dozvoljen je samo PDF ili DOC format.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    fileError.value = 'Fajl ne smije biti veći od 5MB.'
    return
  }
  cvFile.value = file
}

async function submitRequest() {
  buttonState.value = 'loading'
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('mentor_id', route.params.id)
    formData.append('expectations', expectations.value)
    formData.append('skills_to_improve', skills.value)
    formData.append('cv', cvFile.value)

    const response = await fetch('http://127.0.0.1:8000/mentoring/requests/', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    })

    if (!response.ok) throw new Error('Greška')

    buttonState.value = 'success'
    setTimeout(() => {
      buttonState.value = 'pending'
    }, 2000)

  } catch (e) {
    buttonState.value = 'error'
    setTimeout(() => {
      buttonState.value = 'idle'
    }, 3000)
  }
}

onMounted(async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/mentoring/mentors/${route.params.id}`)
    mentor.value = await response.json()
  } catch (e) {
    console.error('Greška pri učitavanju mentora')
  }
})
</script>