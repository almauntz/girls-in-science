<template>
  <div class="min-h-screen bg-gray-50 flex">

    <!-- ========== SIDEBAR ========== -->
    <aside class="w-64 min-h-screen bg-white border-r border-gray-100 shadow-sm flex flex-col">
      
      <div class="p-6 border-b border-gray-100">
        <h1 class="text-lg font-bold text-gray-800">Girls in Science</h1>
        <p class="text-xs text-gray-400 mt-1" v-if="username">{{ username }}</p>
      </div>

      <nav class="flex-1 p-4 space-y-1">
        
        <button
          @click="activeTab = 'profil'"
          :class="[
            'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
            activeTab === 'profil'
              ? 'bg-violet-50 text-violet-700 border border-violet-200'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
          ]"
        >
          <span class="text-lg"></span>
          Moj profil
        </button>

        <button
          @click="activeTab = 'dashboard'"
          :class="[
            'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
            activeTab === 'dashboard'
              ? 'bg-violet-50 text-violet-700 border border-violet-200'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
          ]"
        >
          <span class="text-lg"></span>
          Dashboard
        </button>

        <button
          @click="activeTab = 'aktivnosti'"
          :class="[
            'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
            activeTab === 'aktivnosti'
              ? 'bg-violet-50 text-violet-700 border border-violet-200'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
          ]"
        >
          <span class="text-lg"></span>
          Aktivnosti
        </button>

      </nav>
    </aside>

    <!-- ========== GLAVNI SADRŽAJ ========== -->
    <main class="flex-1 p-8 overflow-y-auto">

      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="text-gray-400 text-sm">Učitavanje...</div>
      </div>

      <div v-else>

        <!-- TAB: MOJ PROFIL -->
        <div v-if="activeTab === 'profil'">
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Moj profil</h2>
            <p class="text-gray-500 text-sm mt-1">Uredite svoje podatke</p>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6 max-w-2xl">

            <div v-if="successMessage"
                 class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage"
                 class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">
              {{ errorMessage }}
            </div>

            <form @submit.prevent="saveProfile" class="space-y-5">

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ime i prezime *</label>
                <input
                  v-model="form.full_name"
                  type="text"
                  placeholder="Unesite ime i prezime"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                         focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                />
                <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">{{ errors.full_name }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Oblast</label>
                <input
                  v-model="form.field"
                  type="text"
                  placeholder="Npr. Softversko inženjerstvo"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                         focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Biografija</label>
                <textarea
                  v-model="form.biography"
                  placeholder="Napišite nešto o sebi..."
                  rows="4"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                         focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none"
                ></textarea>
                <div class="flex justify-between mt-1">
                  <p v-if="errors.biography" class="text-red-500 text-xs">{{ errors.biography }}</p>
                  <span class="text-xs text-gray-400 ml-auto">{{ form.biography?.length || 0 }}/500</span>
                </div>
              </div>

              <div class="pt-2">
                <button
                  type="submit"
                  :disabled="!isFormValid"
                  class="w-full bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium
                         hover:bg-violet-700 transition-colors duration-200
                         disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Spremi promjene
                </button>
              </div>

            </form>
          </div>
        </div>

        <!-- TAB: DASHBOARD -->
        <div v-if="activeTab === 'dashboard'">
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Dashboard</h2>
            <p class="text-gray-500 text-sm mt-1">Pregled vaših radionica</p>
          </div>

          <div v-if="dashboardError" class="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-center text-sm">
            {{ dashboardError }}
          </div>

          <!-- Moje radionice -->
          <section class="mb-8">
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-2 h-6 bg-violet-500 rounded-full"></div>
              <h3 class="text-xl font-bold text-gray-800">Moje radionice</h3>
            </div>
            <div v-if="myWorkshops.length === 0"
                 class="bg-white border border-dashed border-gray-300 rounded-xl p-8 text-center text-gray-500 text-sm">
              Niste prijavljeni ni na jednu radionicu. Pogledajte dostupne radionice ispod!
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="w in myWorkshops" :key="w.id"
                   class="bg-white rounded-xl shadow-sm border border-violet-100 p-5 hover:shadow-md transition">
                <span class="text-xs font-semibold uppercase tracking-wider text-violet-600 bg-violet-50 px-2 py-1 rounded">Prijavljen/a</span>
                <h4 class="font-bold text-gray-900 mt-2">{{ w.title }}</h4>
                <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
                <div class="mt-4 pt-3 border-t border-gray-100 text-xs text-gray-500 flex justify-between">
                  <span>📅 {{ formatDate(w.date) }}</span>
                  <span>👥 Max: {{ w.capacity }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Nove radionice -->
          <section class="mb-8">
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
              <h3 class="text-xl font-bold text-gray-800">Nove radionice</h3>
            </div>
            <div v-if="newWorkshops.length === 0"
                 class="bg-white border border-gray-200 rounded-xl p-6 text-center text-gray-500 text-sm">
              Trenutno nema novih radionica dodanih u zadnjih 48h.
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div v-for="w in newWorkshops" :key="w.id"
                   class="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-blue-100 p-5 shadow-sm">
                <span class="text-xs font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded">Novo</span>
                <h4 class="font-bold text-gray-900 mt-2">{{ w.title }}</h4>
                <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
                <p class="text-blue-600 text-xs font-medium mt-3">📅 {{ formatDate(w.date) }}</p>
              </div>
            </div>
          </section>

          <!-- Dostupne radionice -->
          <section>
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-2 h-6 bg-green-500 rounded-full"></div>
              <h3 class="text-xl font-bold text-gray-800">Dostupne radionice</h3>
            </div>
            <div v-if="availableWorkshops.length === 0"
                 class="bg-white border border-gray-200 rounded-xl p-6 text-center text-gray-500 text-sm">
              Trenutno nema drugih dostupnih radionica za prijavu.
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="w in availableWorkshops" :key="w.id"
                   class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col justify-between hover:border-green-300 transition">
                <div>
                  <h4 class="font-bold text-gray-900">{{ w.title }}</h4>
                  <p class="text-gray-600 text-sm mt-1 line-clamp-3">{{ w.description }}</p>
                  <p class="text-gray-500 text-xs mt-3">📅 {{ formatDate(w.date) }}</p>
                </div>
                <div class="mt-5 pt-4 border-t border-gray-100 flex items-center justify-between">
                  <span class="text-xs text-gray-500">Mjestâ: {{ w.capacity }}</span>
                  <button
                    @click="handleRegister(w.id)"
                    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
                  >
                    Prijavi se
                  </button>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- TAB: AKTIVNOSTI -->
        <div v-if="activeTab === 'aktivnosti'">
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Aktivnosti</h2>
            <p class="text-gray-500 text-sm mt-1">Pregled vaših aktivnosti na platformi</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm p-8 text-center text-gray-400">
            <p class="text-4xl mb-3">⚡</p>
            <p class="text-sm">Aktivnosti će biti prikazane ovdje.</p>
          </div>
        </div>

      </div>
    </main>

  </div>
</template>

<script>
//import axios from 'axios'
import { getMyProfile, updateProfile } from '../../services/api.js'

export default {
  name: 'ProfilesView',

  data() {
    return {
      activeTab: 'profil',

      // Profil
      form: {
        full_name: '',
        biography: '',
        field: ''
      },
      errors: {
        full_name: '',
        biography: ''
      },
      successMessage: '',
      errorMessage: '',

      // Dashboard
      username: localStorage.getItem('username') || 'Korisnice',
      myWorkshops: [],
      newWorkshops: [],
      availableWorkshops: [],
      dashboardError: null,

      isLoading: false
    }
  },

  computed: {
    isFormValid() {
      return (
        this.form.full_name.trim() !== '' &&
        (this.form.biography?.length || 0) <= 500
      )
    }
  },

  async mounted() {
    this.isLoading = true
    await Promise.all([
      this.loadProfile(),
      this.fetchDashboardData()
    ])
    this.isLoading = false
  },

  methods: {

    async loadProfile() {
      try {
        const token = localStorage.getItem('token')
        const data = await getMyProfile(token)
        this.form.full_name = data.full_name || ''
        this.form.biography = data.biography || ''
        this.form.field = data.field || ''
      } catch (error) {
        this.errorMessage = 'Greška pri učitavanju profila.'
      }
    },

    validateForm() {
      this.errors = { full_name: '', biography: '' }
      let isValid = true

      if (!this.form.full_name || this.form.full_name.trim() === '') {
        this.errors.full_name = 'Ime ne smije biti prazno.'
        isValid = false
      }

      if (this.form.biography && this.form.biography.length > 500) {
        this.errors.biography = 'Biografija ne smije biti duža od 500 karaktera.'
        isValid = false
      }

      return isValid
    },

    async saveProfile() {
      if (!this.validateForm()) return

      this.successMessage = ''
      this.errorMessage = ''

      try {
        const token = localStorage.getItem('token')
        await updateProfile(token, {
          full_name: this.form.full_name,
          biography: this.form.biography,
          field: this.form.field
        })
        this.successMessage = 'Promjene su uspješno sačuvane!'
        setTimeout(() => { this.successMessage = '' }, 3000)
      } catch (error) {
        this.errorMessage = 'Greška pri čuvanju. Pokušajte ponovo.'
        setTimeout(() => { this.errorMessage = '' }, 3000)
      }
    },

    getAuthHeaders() {
      const token = localStorage.getItem('token')
      return { headers: { Authorization: `Bearer ${token}` } }
    },

    async fetchDashboardData() {
      this.dashboardError = null
      try {
        const response = await axios.get(
          'http://localhost:8000/profiles/dashboard',
          this.getAuthHeaders()
        )
        this.myWorkshops = response.data.my_workshops
        this.newWorkshops = response.data.new_workshops
        this.availableWorkshops = response.data.available_workshops
      } catch (err) {
        console.error('Greška pri učitavanju dashboarda:', err)
        this.dashboardError = 'Nije moguće učitati podatke. Provjerite jeste li prijavljeni.'
      }
    },

    async handleRegister(workshopId) {
      try {
        const response = await axios.post(
          `http://localhost:8000/profiles/dashboard/register?workshop_id=${workshopId}`,
          {},
          this.getAuthHeaders()
        )
        alert(response.data.message || 'Uspješno ste se prijavili na radionicu!')
        this.fetchDashboardData()
      } catch (err) {
        const errorMsg = err.response?.data?.detail || 'Greška pri prijavi na radionicu.'
        alert(errorMsg)
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('bs-BA', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>