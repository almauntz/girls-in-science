<template>
  <div class="min-h-screen bg-gradient-to-br from-violet-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Zaglavlje -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Prijava za program mentorstva</h1>
        <p class="text-gray-600 text-lg">Pridruži se našoj zajednici i nađi svoju mentoricu!</p>
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
          
          <!-- SEKCIJA 1: Lični podaci -->
          <div class="border-b pb-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">1. Lični podaci</h2>
            
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

            <div class="mt-6">
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

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <div>
                <label class="block text-sm font-semibold text-gray-800 mb-2">
                  Fakultet <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.faculty"
                  type="text"
                  placeholder="Npr. Fakultet informatike"
                  class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
                  :class="{ 'border-red-500': !form.faculty && touched.faculty }"
                />
                <p v-if="!form.faculty && touched.faculty" class="text-red-500 text-sm mt-1">Obavezno polje</p>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-800 mb-2">
                  Godina studija <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="form.year_of_study"
                  class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition"
                  :class="{ 'border-red-500': !form.year_of_study && touched.year_of_study }"
                >
                  <option value="">Odaberite godinu...</option>
                  <option value="1">1. godina</option>
                  <option value="2">2. godina</option>
                  <option value="3">3. godina</option>
                  <option value="4">4. godina</option>
                  <option value="master">Master</option>
                </select>
                <p v-if="!form.year_of_study && touched.year_of_study" class="text-red-500 text-sm mt-1">Obavezno polje</p>
              </div>
            </div>
          </div>

          <!-- SEKCIJA 2: Akademski i profesionalni interesi -->
          <div class="border-b pb-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">2. Akademski i profesionalni interesi</h2>
            
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-3">
                Koje su vaše oblasti interesovanja? <span class="text-red-500">*</span>
              </label>
              <div class="space-y-2">
                <label v-for="option in interestOptions" :key="option" class="flex items-center">
                  <input
                    type="checkbox"
                    :value="option"
                    v-model="form.areas_of_interest"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">{{ option }}</span>
                </label>
              </div>
              <p v-if="form.areas_of_interest.length === 0 && touched.areas_of_interest" class="text-red-500 text-sm mt-1">Odaberite bar jednu oblast</p>
            </div>

            <div class="mt-6">
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Da li imate ideju za poslovanje? <span class="text-gray-500 text-xs">(Opciono)</span>
              </label>
              <div class="space-y-2">
                <label class="flex items-center">
                  <input
                    type="radio"
                    value="Da"
                    v-model="form.has_business_idea"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">Da</span>
                </label>
                <label class="flex items-center">
                  <input
                    type="radio"
                    value="Ne"
                    v-model="form.has_business_idea"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">Ne</span>
                </label>
              </div>
            </div>
          </div>

          <!-- SEKCIJA 3: Očekivanja od mentorskog programa -->
          <div class="border-b pb-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">3. Očekivanja od mentorskog programa</h2>
            
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Šta očekujete od mentoringа? <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="form.expectations"
                placeholder="Opišite šta očekujete od mentorskog programa..."
                rows="4"
                class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition resize-none"
                :class="{ 'border-red-500': (!form.expectations || form.expectations.length < 20) && touched.expectations }"
              ></textarea>
              <p class="text-gray-500 text-xs mt-1">{{ form.expectations.length }} / 500 karaktera</p>
              <p v-if="!form.expectations && touched.expectations" class="text-red-500 text-sm mt-1">Obavezno polje (min. 20 karaktera)</p>
            </div>

            <div class="mt-6">
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Koje vještine bi trebali poboljšati? <span class="text-gray-500 text-xs">(Opciono)</span>
              </label>
              <textarea
                v-model="form.skills_to_improve"
                placeholder="Npr. vođenje projekta, prezentacijske vještine, itd..."
                rows="3"
                class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition resize-none"
              ></textarea>
            </div>

            <div class="mt-6">
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Motivacijska poruka <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="form.motivational_message"
                placeholder="Opišite vašu motivaciju za učešće u programu..."
                rows="4"
                class="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary transition resize-none"
                :class="{ 'border-red-500': (!form.motivational_message || form.motivational_message.length < 20) && touched.motivational_message }"
              ></textarea>
              <p class="text-gray-500 text-xs mt-1">{{ form.motivational_message.length }} / 500 karaktera</p>
              <p v-if="!form.motivational_message && touched.motivational_message" class="text-red-500 text-sm mt-1">Obavezno polje (min. 20 karaktera)</p>
            </div>
          </div>

          <!-- SEKCIJA 4: Dostupnost i obaveze -->
          <div class="border-b pb-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">4. Dostupnost i obaveze</h2>
            
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-3">
                Koji format sesije vam odgovara? <span class="text-red-500">*</span>
              </label>
              <div class="space-y-2">
                <label class="flex items-center">
                  <input
                    type="radio"
                    value="Online"
                    v-model="form.preferred_session_format"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">Online</span>
                </label>
                <label class="flex items-center">
                  <input
                    type="radio"
                    value="Uživo"
                    v-model="form.preferred_session_format"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">Uživo</span>
                </label>
                <label class="flex items-center">
                  <input
                    type="radio"
                    value="Kombinovano"
                    v-model="form.preferred_session_format"
                    class="rounded border-gray-300 mr-2"
                  />
                  <span class="text-gray-700">Kombinovano</span>
                </label>
              </div>
            </div>

            <div class="mt-6">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="form.session_commitment"
                  class="rounded border-gray-300 mr-2"
                />
                <span class="text-sm text-gray-700">
                  Spremna sam da učestvujem u najmanje jednoj sesiji mjesečno
                </span>
              </label>
            </div>
          </div>

          <!-- SEKCIJA 5: Upload CV-ja -->
          <div class="border-b pb-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">5. Učitavanje CV-ja</h2>
            
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">
                Upload CV-ja <span class="text-gray-500 text-xs">(Opciono)</span>
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
            </div>
          </div>

          <!-- SEKCIJA 6: Saglasnosti -->
          <div class="bg-gray-50 p-6 rounded-lg">
            <h2 class="text-lg font-bold text-gray-800 mb-4">6. Saglasnosti</h2>
            
            <div class="space-y-3">
              <label class="flex items-start">
                <input
                  type="checkbox"
                  v-model="form.consent_data"
                  class="rounded border-gray-300 mr-3 mt-1"
                />
                <span class="text-sm text-gray-700">
                  Saglasna sam da se moji lični podaci koriste u svrhu realizacije Girls' Business Mentoring Programa
                </span>
              </label>
              <label class="flex items-start">
                <input
                  type="checkbox"
                  v-model="form.consent_evaluation"
                  class="rounded border-gray-300 mr-3 mt-1"
                />
                <span class="text-sm text-gray-700">
                  Saglasna sam da učestvujem u evaluaciji programa preko ankete
                </span>
              </label>
            </div>

            <p v-if="(!form.consent_data || !form.consent_evaluation) && touched.consent" class="text-red-500 text-sm mt-3">
              Trebate pristati na sve uslove
            </p>
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
        Hvala što se prijaviš na program. Odgovorićemo na tvoju prijavu u roku od 5-7 radnih dana.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const interestOptions = [
  'IT i digitalne tehnologije',
  'Data & AI',
  'Medicina',
  'Biologija',
  'Hemija',
  'Inženjerstvo',
  'Matematika',
  'Fizika',
  'Ostalo'
]

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  faculty: '',
  year_of_study: '',
  areas_of_interest: [],
  has_business_idea: '',
  expectations: '',
  skills_to_improve: '',
  motivational_message: '',
  preferred_session_format: 'Online',
  session_commitment: false,
  consent_data: false,
  consent_evaluation: false,
  cv_file: null
})

const touched = ref({
  first_name: false,
  last_name: false,
  email: false,
  faculty: false,
  year_of_study: false,
  areas_of_interest: false,
  expectations: false,
  motivational_message: false,
  consent: false
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

// Provjera da li je forma validna
const isFormValid = computed(() => {
  return (
    form.value.first_name.trim() &&
    form.value.last_name.trim() &&
    isValidEmail(form.value.email) &&
    form.value.faculty.trim() &&
    form.value.year_of_study &&
    form.value.areas_of_interest.length > 0 &&
    form.value.expectations.trim().length >= 20 &&
    form.value.motivational_message.trim().length >= 20 &&
    form.value.preferred_session_format &&
    form.value.consent_data &&
    form.value.consent_evaluation
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
    formData.append('faculty', form.value.faculty)
    formData.append('year_of_study', form.value.year_of_study)
    formData.append('areas_of_interest', form.value.areas_of_interest.join(', '))
    formData.append('expectations', form.value.expectations)
    formData.append('skills_to_improve', form.value.skills_to_improve)
    formData.append('motivational_message', form.value.motivational_message)
    formData.append('preferred_session_format', form.value.preferred_session_format)
    formData.append('session_commitment', form.value.session_commitment)
    formData.append('has_business_idea', form.value.has_business_idea)
    formData.append('consent_data', form.value.consent_data)
    formData.append('consent_evaluation', form.value.consent_evaluation)
    
    if (form.value.cv_file) {
      formData.append('cv_file', form.value.cv_file)
    }

    // Pošalji na backend
    const response = await fetch('http://127.0.0.1:8000/api/v1/students/register', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Greška pri slanju prijave')
    }

    const data = await response.json()
    successMessage.value = `Hvala, ${data.first_name}! Vaša prijava je primljena. Odgovorićemo vam na email ${data.email} u roku od 5-7 radnih dana.`

    // Resetuj formu nakon 3 sekunde
    setTimeout(() => {
      form.value = {
        first_name: '',
        last_name: '',
        email: '',
        faculty: '',
        year_of_study: '',
        areas_of_interest: [],
        has_business_idea: '',
        expectations: '',
        skills_to_improve: '',
        motivational_message: '',
        preferred_session_format: 'Online',
        session_commitment: false,
        consent_data: false,
        consent_evaluation: false,
        cv_file: null
      }
    }, 3000)
  } catch (error) {
    errorMessage.value = error.message || 'Greška pri slanju prijave'
    console.error('Greška pri slanju:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.primary {
  @apply bg-violet-600;
}
</style>
