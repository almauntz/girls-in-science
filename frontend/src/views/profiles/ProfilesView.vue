<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">

      <!-- HEADER -->
      <div class="mb-8 flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div>
          <h1 class="text-3xl font-bold text-gray-800">Moj Dashboard</h1>
          <p class="text-gray-500 mt-1" v-if="username">
            Dobrodošla nazad, <span class="font-semibold text-violet-600">{{ username }}</span>!
          </p>
        </div>
        <span class="px-3 py-1 bg-violet-100 text-violet-600 rounded-full text-sm font-medium">
          Korisnički profil
        </span>
      </div>

      <!-- LOADING -->
      <div v-if="isLoading" class="flex justify-center items-center py-10">
        <div class="text-gray-500 text-sm">Učitavanje...</div>
      </div>

      <div v-else class="space-y-10">

        <!-- ===================== -->
        <!-- SEKCIJA: MOJ PROFIL  -->
        <!-- ===================== -->
        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-violet-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Moj profil</h2>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6 max-w-2xl">

            <!-- Poruka uspjeha -->
            <div v-if="successMessage"
                 class="bg-green-50 text-green-700 border border-green-200
                        rounded-lg px-4 py-3 mb-4 text-sm">
              {{ successMessage }}
            </div>
            <!-- Poruka greške -->
            <div v-if="errorMessage"
                 class="bg-red-50 text-red-700 border border-red-200
                        rounded-lg px-4 py-3 mb-4 text-sm">
              {{ errorMessage }}
            </div>

            <form @submit.prevent="saveProfile" class="space-y-5">

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Ime i prezime *
                </label>
                <input
                  v-model="form.full_name"
                  type="text"
                  placeholder="Unesite ime i prezime"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2
                         text-sm focus:outline-none focus:ring-2
                         focus:ring-green-500 focus:border-transparent"
                />
                <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">
                  {{ errors.full_name }}
                </p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Oblast
                </label>
                <input
                  v-model="form.field"
                  type="text"
                  placeholder="Npr. Softversko inženjerstvo"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2
                         text-sm focus:outline-none focus:ring-2
                         focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Biografija
                </label>
                <textarea
                  v-model="form.biography"
                  placeholder="Napišite nešto o sebi..."
                  rows="4"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2
                         text-sm focus:outline-none focus:ring-2
                         focus:ring-green-500 focus:border-transparent resize-none"
                ></textarea>
                <div class="flex justify-between mt-1">
                  <p v-if="errors.biography" class="text-red-500 text-xs">
                    {{ errors.biography }}
                  </p>
                  <span class="text-xs text-gray-400 ml-auto">
                    {{ form.biography?.length || 0 }}/500
                  </span>
                </div>
              </div>

              <div class="pt-2">
                <button
                  type="submit"
                  :disabled="!isFormValid"
                  class="w-full bg-green-600 text-white py-2 px-4 rounded-lg
                         text-sm font-medium hover:bg-green-700
                         transition-colors duration-200
                         disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Spremi promjene
                </button>
              </div>

            </form>
          </div>
        </section>

        <!-- ========================= -->
        <!-- SEKCIJA: MOJE RADIONICE  -->
        <!-- ========================= -->
        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-violet-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Moje radionice</h2>
          </div>

          <div v-if="dashboardError" class="bg-red-50 text-red-600 p-4 rounded-xl mb-4 text-center">
            {{ dashboardError }}
          </div>

          <div v-if="myWorkshops.length === 0"
               class="bg-white border border-dashed border-gray-300 rounded-xl p-8 text-center text-gray-500">
            Niste prijavljeni ni na jednu radionicu. Pogledajte dostupne radionice ispod!
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="w in myWorkshops"
              :key="w.id"
              class="bg-white rounded-xl shadow-sm border border-violet-100 p-5 hover:shadow-md transition"
            >
              <span class="text-xs font-semibold uppercase tracking-wider text-violet-600 bg-violet-50 px-2 py-1 rounded">
                Prijavljen/a
              </span>
              <h3 class="font-bold text-lg text-gray-900 mt-2">{{ w.title }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
              <div class="mt-4 pt-3 border-t border-gray-100 text-xs text-gray-500 flex justify-between">
                <span>📅 {{ formatDate(w.date) }}</span>
                <span>👥 Max: {{ w.capacity }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- ======================== -->
        <!-- SEKCIJA: NOVE RADIONICE -->
        <!-- ======================== -->
        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Nove radionice</h2>
          </div>

          <div v-if="newWorkshops.length === 0"
               class="text-gray-500 bg-white p-6 rounded-xl border text-center">
            Trenutno nema novih radionica dodanih u zadnjih 48h.
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              v-for="w in newWorkshops"
              :key="w.id"
              class="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-blue-100 p-5 shadow-sm"
            >
              <span class="text-xs font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded">Novo</span>
              <h3 class="font-bold text-lg text-gray-900 mt-2">{{ w.title }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
              <p class="text-blue-600 text-xs font-medium mt-3">📅 Održava se: {{ formatDate(w.date) }}</p>
            </div>
          </div>
        </section>

        <!-- ============================= -->
        <!-- SEKCIJA: DOSTUPNE RADIONICE  -->
        <!-- ============================= -->
        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-green-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Dostupne radionice</h2>
          </div>

          <div v-if="availableWorkshops.length === 0"
               class="text-gray-500 bg-white p-6 rounded-xl border text-center">
            Trenutno nema drugih dostupnih radionica za prijavu.
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="w in availableWorkshops"
              :key="w.id"
              class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col justify-between hover:border-green-300 transition"
            >
              <div>
                <h3 class="font-bold text-lg text-gray-900">{{ w.title }}</h3>
                <p class="text-gray-600 text-sm mt-1 line-clamp-3">{{ w.description }}</p>
                <p class="text-gray-500 text-xs mt-3">📅 Datum: {{ formatDate(w.date) }}</p>
              </div>

              <div class="mt-5 pt-4 border-t border-gray-100 flex items-center justify-between">
                <span class="text-xs text-gray-500">Mjestâ: {{ w.capacity }}</span>
                <button
                  @click="handleRegister(w.id)"
                  class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition shadow-sm"
                >
                  Prijavi se
                </button>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { getMyProfile, updateProfile } from '../../services/api.js'

export default {
  name: 'ProfilesView',

  data() {
    return {
      // --- Profil ---
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

      // --- Dashboard / Radionice ---
      username: localStorage.getItem('username') || 'Korisnice',
      myWorkshops: [],
      newWorkshops: [],
      availableWorkshops: [],
      dashboardError: null,

      // Zajednički loading
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
    // Učitaj profil i dashboard paralelno
    this.isLoading = true
    await Promise.all([
      this.loadProfile(),
      this.fetchDashboardData()
    ])
    this.isLoading = false
  },

  methods: {

    // ==================
    // PROFIL metode
    // ==================

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

    // =====================
    // DASHBOARD metode
    // =====================

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