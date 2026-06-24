<template>
  <div class="max-w-4xl mx-auto py-8 px-4">

    <h1 class="text-3xl font-bold text-gray-800 mb-2">Prijava za mentorski program</h1>
    <p class="text-gray-500 mb-8">
      Popunite formu kako biste pronašli mentoricu koja odgovara vašim interesovanjima.
    </p>

    <form @submit.prevent="submitForm" class="grid grid-cols-1 md:grid-cols-2 gap-6">

      <!-- Sekcija 1: Lični podaci -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h2 class="font-semibold text-lg mb-4">1. Lični podaci</h2>

        <div>
          <label class="text-sm text-gray-600 mb-1 block">Ime i prezime *</label>
          <input v-model="form.full_name" type="text" required
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400" />
        </div>

        <div class="mt-3">
          <label class="text-sm text-gray-600 mb-1 block">Email adresa *</label>
          <input v-model="form.email" type="email" required
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400" />
        </div>

        <div class="grid grid-cols-2 gap-3 mt-3">
          <div>
            <label class="text-sm text-gray-600 mb-1 block">Univerzitet na kojem studirate *</label>
            <input v-model="form.university" type="text" required
              class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400" />
          </div>
          <div>
            <label class="text-sm text-gray-600 mb-1 block">Fakultet *</label>
            <input v-model="form.faculty" type="text" required
              class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400" />
          </div>
        </div>

        <div class="mt-3">
          <label class="text-sm text-gray-600 mb-1 block">Godina studija *</label>
          <select v-model="form.year_of_study" required
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400">
            <option value="">Odaberi godinu studija *</option>
            <option>1. godina</option>
            <option>2. godina</option>
            <option>3. godina</option>
            <option>4. godina</option>
            <option>Master</option>
          </select>
        </div>

        <div class="mt-3">
          <label class="text-sm text-gray-600 mb-1 block">Grad/Država *</label>
          <input v-model="form.city_country" type="text" required
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400" />
        </div>
      </div>

      <!-- Sekcija 2: Akademski i profesionalni interesi -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h2 class="font-semibold text-lg mb-4">2. Akademski i profesionalni interesi</h2>

        <div>
          <label class="text-sm text-gray-600 mb-1 block">Koja su vaša glavna interesovanja? *</label>
          <select v-model="form.areas_of_interest" required
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400">
            <option value="">Odaberi glavna interesovanja *</option>
            <option>Poduzetništvo / startupi</option>
            <option>Finansije i investicije</option>
            <option>IT i digitalne tehnologije</option>
            <option>Data, AI i digitalna transformacija</option>
            <option>Marketing i brendiranje</option>
            <option>Projektni menadžment</option>
            <option>Leadership i upravljanje</option>
            <option>Karijerni razvoj</option>
            <option>Akademska karijera i istraživanje</option>
          </select>
        </div>

        <div class="mt-4">
          <label class="text-sm text-gray-600 mb-2 block">
            Da li trenutno imate poslovnu ideju ili start-up kompaniju? *
          </label>
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm">
              <input type="radio" value="Da" v-model="form.has_business_idea" class="accent-purple-600" /> Da
            </label>
            <label class="flex items-center gap-2 text-sm">
              <input type="radio" value="Ne" v-model="form.has_business_idea" class="accent-purple-600" /> Ne
            </label>
            <label class="flex items-center gap-2 text-sm">
              <input type="radio" value="Other" v-model="form.has_business_idea" class="accent-purple-600" /> Other
            </label>
          </div>
        </div>
      </div>

      <!-- Sekcija 3: Očekivanja -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h2 class="font-semibold text-lg mb-4">3. Očekivanja od mentorskog programa</h2>

        <div>
          <label class="text-sm text-gray-600 mb-1 block">
            Šta očekujete od učešća u mentorskom programu? *
          </label>
          <textarea v-model="form.expectations" required rows="3"
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
            placeholder="Tvoj odgovor ovdje..."></textarea>
        </div>

        <div class="mt-4">
          <label class="text-sm text-gray-600 mb-1 block">
            Koje vještine ili znanja želite posebno unaprijediti kroz mentoring? *
          </label>
          <textarea v-model="form.skills_to_improve" required rows="3"
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
            placeholder="Tvoj odgovor ovdje..."></textarea>
        </div>
      </div>

      <!-- Sekcija 4: Dostupnost -->
      <div class="bg-white rounded-xl border border-gray-200 p-6">
        <h2 class="font-semibold text-lg mb-4">4. Dostupnost i obaveze</h2>

        <label class="text-sm text-gray-600 mb-2 block">Preferirani format mentorskih sesija *</label>
        <div class="flex flex-col gap-2">
          <label class="flex items-center gap-2 text-sm">
            <input type="radio" value="Online" v-model="form.preferred_session_format" class="accent-purple-600" /> Online
          </label>
          <label class="flex items-center gap-2 text-sm">
            <input type="radio" value="Uživo" v-model="form.preferred_session_format" class="accent-purple-600" /> Uživo
          </label>
          <label class="flex items-center gap-2 text-sm">
            <input type="radio" value="Kombinovano" v-model="form.preferred_session_format" class="accent-purple-600" /> Kombinovano
          </label>
        </div>

        <div class="mt-4">
          <label class="flex items-start gap-2 text-sm text-gray-700">
            <input type="checkbox" v-model="form.session_commitment" class="mt-1 accent-purple-600" />
            Spremna sam da učestvujem u minimalno dvije (2) mentorske sesije u okviru Girls' Business Mentoring Programa *
          </label>
        </div>
      </div>

      <!-- Sekcija 5: Saglasnosti -->
      <div class="bg-white rounded-xl border border-gray-200 p-6 col-span-1 md:col-span-2">
        <h2 class="font-semibold text-lg mb-4">5. Saglasnosti</h2>

        <div class="flex flex-col gap-3">
          <label class="flex items-start gap-2 text-sm text-gray-700">
            <input type="checkbox" v-model="form.consent_data" required class="mt-1 accent-purple-600" />
            Saglasna sam da se moji lični podaci koriste isključivo u svrhu realizacije Girls' Business Mentoring Programa *
          </label>
          <label class="flex items-start gap-2 text-sm text-gray-700">
            <input type="checkbox" v-model="form.consent_evaluation" required class="mt-1 accent-purple-600" />
            Saglasna sam da učestvujem u evaluaciji Girls' Business Mentoring Programa, uključujući popunjavanje završne evaluacione ankete *
          </label>
        </div>
      </div>

      <!-- Poruke -->
      <div v-if="successMsg"
        class="col-span-1 md:col-span-2 bg-green-50 border border-green-200 text-green-700 rounded-lg p-4 text-sm">
        ✅ {{ successMsg }}
      </div>
      <div v-if="errorMsg"
        class="col-span-1 md:col-span-2 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm">
        ⚠️ {{ errorMsg }}
      </div>

      <!-- Submit -->
      <div class="col-span-1 md:col-span-2">
        <button type="submit" :disabled="loading"
          class="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 rounded-xl transition-colors duration-200 disabled:opacity-50">
          {{ loading ? 'Slanje...' : 'Pošalji prijavu' }}
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { registerStudent } from '../../services/mentoring.js'

const form = ref({
  full_name: '',
  email: '',
  university: '',
  faculty: '',
  year_of_study: '',
  city_country: '',
  areas_of_interest: '',
  has_business_idea: '',
  expectations: '',
  skills_to_improve: '',
  preferred_session_format: '',
  session_commitment: false,
  consent_data: false,
  consent_evaluation: false
})

const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const submitForm = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const formData = new FormData()
    Object.entries(form.value).forEach(([key, value]) => {
      formData.append(key, value)
    })

    await registerStudent(formData)
    successMsg.value = 'Vaša prijava je uspješno poslana!'

    form.value = {
      full_name: '', email: '', university: '', faculty: '',
      year_of_study: '', city_country: '', areas_of_interest: '',
      has_business_idea: '', expectations: '', skills_to_improve: '',
      preferred_session_format: '', session_commitment: false,
      consent_data: false, consent_evaluation: false
    }

  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Greška pri slanju prijave. Pokušajte ponovo.'
  } finally {
    loading.value = false
  }
}


onMounted(async () => {
  const token =
    localStorage.getItem('token') ||
    localStorage.getItem('access_token')

  if (!token) {
    console.log('Nema tokena')
    return
  }

  try {
    const response = await axios.get('http://localhost:8000/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const user = response.data

    form.value.full_name = user.full_name || ''
    form.value.email = user.email || ''

  } catch (err) {
    console.error(
      'Greška pri dohvaćanju korisničkih podataka:',
      err.response?.data || err
    )
  }
})
</script>