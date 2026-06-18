<template>
  <div class="min-h-screen bg-gradient-to-br from-violet-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8" style="background: linear-gradient(to right, #d0c8f9, #F9DBE7);">
    <div class="max-w-2xl mx-auto">
      <!-- Zaglavlje -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Prijava za program mentorstva</h1>
        <p class="text-gray-600 text-lg">Budi dio naše zajednice i inspiriši buduće stručnjakinje u STEM-u!</p>
      </div>

      <!-- Forma Kartica -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        
        <!-- Success Poruka -->
        <div 
          v-if="successMessage" 
          class="mb-6 bg-green-50 border border-green-200 text-green-800 px-4 py-4 rounded-lg flex items-start"
        >
          <span class="text-2xl mr-3">✓</span>
          <div>
            <h3 class="font-semibold text-green-900">Prijava uspješno poslana!</h3>
            <p class="text-sm text-green-700 mt-1">{{ successMessage }}</p>
          </div>
        </div>

        <!-- Error Poruka -->
        <div 
          v-if="errorMessage" 
          class="mb-6 bg-red-50 border border-red-200 text-red-800 px-4 py-4 rounded-lg flex items-start"
        >
          <span class="text-2xl mr-3">⚠️</span>
          <div>
            <h3 class="font-semibold text-red-900">Greška pri slanju</h3>
            <p class="text-sm text-red-700 mt-1">{{ errorMessage }}</p>
          </div>
        </div>

        <!-- Forma -->
        <form @submit.prevent="submitForm" v-if="!successMessage" class="space-y-6">
          
          <!-- Ime i Prezime -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Ime <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.first_name"
                type="text"
                placeholder="Vaše ime"
                class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
                :class="{ 'border-red-500': !form.first_name && touched.first_name }"
              />
              <p v-if="!form.first_name && touched.first_name" class="text-red-500 text-sm mt-1">Obavezno polje</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Prezime <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.last_name"
                type="text"
                placeholder="Vaše prezime"
                class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
                :class="{ 'border-red-500': !form.last_name && touched.last_name }"
              />
              <p v-if="!form.last_name && touched.last_name" class="text-red-500 text-sm mt-1">Obavezno polje</p>
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              Email adresa <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="vas@email.com"
              class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
              :class="{ 'border-red-500': (!isValidEmail(form.email) || !form.email) && touched.email }"
            />
            <p v-if="!isValidEmail(form.email) && touched.email" class="text-red-500 text-sm mt-1">Unesite validan email</p>
          </div>

          <!-- Oblast stručnosti -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              Oblast stručnosti <span class="text-red-500">*</span>
            </label>
            <select
              v-model="form.field_of_expertise"
              class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
              :class="{ 'border-red-500': !form.field_of_expertise && touched.field_of_expertise }"
            >
              <option value="">Odaberite oblast...</option>
              <option value="IT">IT / Računarstvo</option>
              <option value="Engineering">Inženjerstvo</option>
              <option value="Science">Prirodne nauke</option>
              <option value="Mathematics">Matematika</option>
              <option value="Physics">Fizika</option>
              <option value="Chemistry">Hemija</option>
              <option value="Biology">Biologija</option>
              <option value="Other">Ostalo</option>
            </select>
            <p v-if="!form.field_of_expertise && touched.field_of_expertise" class="text-red-500 text-sm mt-1">Obavezno polje</p>
          </div>

          <!-- Godine iskustva -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              Godine iskustva <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="form.years_of_experience"
              type="number"
              min="0"
              max="70"
              placeholder="Npr. 5"
              class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
              :class="{ 'border-red-500': (!form.years_of_experience && form.years_of_experience !== 0) && touched.years_of_experience }"
            />
            <p v-if="(!form.years_of_experience && form.years_of_experience !== 0) && touched.years_of_experience" class="text-red-500 text-sm mt-1">Obavezno polje</p>
          </div>

          <!-- LinkedIn Profil -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              LinkedIn profil <span class="text-gray-500 text-xs">(Opciono)</span>
            </label>
            <input
              v-model="form.linkedin_url"
              type="text"
              placeholder="https://linkedin.com/in/korisnica"
              class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
              :class="{ 'border-red-500': form.linkedin_url && !isValidLinkedIn(form.linkedin_url) && touched.linkedin_url }"
            />
            <p v-if="form.linkedin_url && !isValidLinkedIn(form.linkedin_url) && touched.linkedin_url" class="text-red-500 text-sm mt-1">LinkedIn URL nije validan</p>
          </div>

          <!-- Biografija -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              Biografija <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="form.bio"
              placeholder="Opišite Vašu profesionalnu karijeru, iskustvo i motivaciju za mentorstvo..."
              rows="5"
              class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition resize-none"
              :class="{ 'border-red-500': (!form.bio || form.bio.length < 20) && touched.bio }"
            ></textarea>
            <p class="text-gray-500 text-xs mt-1">{{ form.bio.length }} / 1500 karaktera</p>
            <p v-if="!form.bio && touched.bio" class="text-red-500 text-sm mt-1">Obavezno polje (min. 20 karaktera)</p>
          </div>

          <!-- Upload CV-ja -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">
              Upload CV-ja <span class="text-red-500">*</span>
            </label>
            <div
              @drop="handleFileDrop"
              @dragover.prevent
              @dragenter.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              class="border-3 border-dashed rounded-lg p-8 text-center transition cursor-pointer"
              :class="isDragging 
                ? 'border-primary bg-purple-50' 
                : 'border-gray-300 bg-gray-50 hover:border-primary hover:bg-purple-50'
              "
            >
              <input
                ref="fileInput"
                @change="handleFileSelect"
                type="file"
                accept=".pdf,.docx"
                class="hidden"
              />
              
              <div v-if="!form.cv_file" @click="$refs.fileInput.click()" class="cursor-pointer">
                <svg class="mx-auto h-12 w-12 text-gray-400 mb-2" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v28a4 4 0 004 4h24a4 4 0 004-4V20m-8-12v12m0 0l-3-3m3 3l3-3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <p class="text-gray-700 font-medium">Klikni ili prevuci CV datoteku</p>
                <p class="text-gray-500 text-sm mt-1">PDF ili DOCX (Max 5MB)</p>
              </div>

              <div v-else class="text-green-600">
                <svg class="mx-auto h-12 w-12 mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <p class="text-green-700 font-medium">{{ form.cv_file.name }}</p>
                <p class="text-green-600 text-sm mt-1">{{ (form.cv_file.size / 1024 / 1024).toFixed(2) }} MB</p>
                <button type="button" @click="form.cv_file = null" class="text-green-600 text-sm font-medium hover:underline mt-2">
                  Ukloni datoteku
                </button>
              </div>
            </div>
            <p v-if="!form.cv_file && touched.cv_file" class="text-red-500 text-sm mt-1">Obavezno je učitati CV</p>
          </div>

          <!-- Checkbox - Obavezna polja -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <p class="text-xs text-gray-600"><span class="text-red-500">*</span>Obavezna polja</p>
          </div>

          <!-- Submit Dugme -->
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full bg-primary text-white py-3 rounded-lg font-semibold text-lg hover:bg-violet-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></span>
            {{ loading ? 'Slanje u tijeku...' : 'Pošalji prijavu' }}
          </button>
        </form>
      </div>

      <!-- Footer tekst -->
      <p class="text-center text-gray-600 text-sm mt-8">
        Hvala što razmatraš učešće u našem programu mentorstva. Odgovorićemo na tvoju prijavu u roku od 5-7 radnih dana.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { applyAsMentor } from '../../services/mentoring.js'

const router = useRouter()

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  field_of_expertise: '',
  years_of_experience: null,
  linkedin_url: '',
  bio: '',
  cv_file: null
})

const touched = ref({
  first_name: false,
  last_name: false,
  email: false,
  field_of_expertise: false,
  years_of_experience: false,
  linkedin_url: false,
  bio: false,
  cv_file: false
})

const fileInput = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const isDragging = ref(false)

// Validacija email-a
const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Validacija LinkedIn URL-a
const isValidLinkedIn = (url) => {
  if (!url) return true // Opciono polje
  const re = /^https?:\/\/(www\.)?linkedin\.com\/.*$/i
  return re.test(url)
}

// Provjera da li je forma validna
const isFormValid = computed(() => {
  return (
    form.value.first_name.trim() &&
    form.value.last_name.trim() &&
    isValidEmail(form.value.email) &&
    form.value.field_of_expertise &&
    (form.value.years_of_experience !== null && form.value.years_of_experience >= 0) &&
    (!form.value.linkedin_url || isValidLinkedIn(form.value.linkedin_url)) &&
    form.value.bio.trim().length >= 20 &&
    form.value.cv_file
  )
})

// Rukovanje file drop-om
const handleFileDrop = (e) => {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    validateAndSetFile(file)
  }
}

// Rukovanje file selection-om
const handleFileSelect = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    const file = files[0]
    validateAndSetFile(file)
  }
}

// Validacija i postavljanje fajla
const validateAndSetFile = (file) => {
  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  const maxSize = 5 * 1024 * 1024 // 5MB

  if (!allowedTypes.includes(file.type)) {
    errorMessage.value = 'Samo PDF i DOCX datoteke su dozvoljene'
    form.value.cv_file = null
    return
  }

  if (file.size > maxSize) {
    errorMessage.value = 'Datoteka ne smije biti veća od 5MB'
    form.value.cv_file = null
    return
  }

  form.value.cv_file = file
  touched.value.cv_file = true
  errorMessage.value = ''
}

// Slanje forme
const submitForm = async () => {
  // Označi sva polja kao touched
  Object.keys(touched.value).forEach(key => {
    touched.value[key] = true
  })

  // Ako forma nije validna, ne slaj
  if (!isFormValid.value) {
    errorMessage.value = 'Molim popunite sva obavezna polja ispravno'
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // Kreiraj FormData objekat
    const formData = new FormData()
    formData.append('first_name', form.value.first_name)
    formData.append('last_name', form.value.last_name)
    formData.append('email', form.value.email)
    formData.append('field_of_expertise', form.value.field_of_expertise)
    formData.append('years_of_experience', form.value.years_of_experience)
    formData.append('linkedin_url', form.value.linkedin_url || 'https://linkedin.com')
    formData.append('bio', form.value.bio)
    formData.append('cv_file', form.value.cv_file)

    // Pošalji na backend
    const response = await applyAsMentor(formData)

    successMessage.value = `Hvala, ${response.first_name}! Vaša prijava je primljena. Odgovorićemo vam na email ${response.email} u roku od 5-7 radnih dana.`

    // Resetuj formu nakon 3 sekunde
    setTimeout(() => {
      form.value = {
        first_name: '',
        last_name: '',
        email: '',
        field_of_expertise: '',
        years_of_experience: null,
        linkedin_url: '',
        bio: '',
        cv_file: null
      }
    }, 3000)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message || 'Greška pri slanju prijave'
    console.error('Greška pri slanju:', error)
  } finally {
    loading.value = false
  }
}
</script>
