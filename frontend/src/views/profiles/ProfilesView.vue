<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      
      <div class="mb-8 flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div>
          <h1 class="text-3xl font-bold text-gray-800">Moj Dashboard</h1>
          <p class="text-gray-500 mt-1" v-if="username">
            Dobrodošla nazad, <span class="font-semibold text-primary">{{ username }}</span>!
          </p>
        </div>
        <span class="px-3 py-1 bg-violet-100 text-primary rounded-full text-sm font-medium">
          Korisnički profil
        </span>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 text-lg">
        Učitavanje podataka sa platforme...
      </div>

      <div v-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-center">
        {{ error }}
      </div>

      <div v-if="!loading" class="space-y-10">
        
        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-primary rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Moje radionice</h2>
          </div>
          
          <div v-if="myWorkshops.length === 0" class="bg-white border border-dashed border-gray-300 rounded-xl p-8 text-center text-gray-500">
            Niste prijavljeni ni na jednu radionicu. Pogledajte dostupne radionice ispod!
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="w in myWorkshops" :key="w.id" class="bg-white rounded-xl shadow-sm border border-violet-100 p-5 hover:shadow-md transition">
              <span class="text-xs font-semibold uppercase tracking-wider text-primary bg-violet-50 px-2 py-1 rounded">Prijavljen/a</span>
              <h3 class="font-bold text-lg text-gray-900 mt-2">{{ w.title }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
              <div class="mt-4 pt-3 border-t border-gray-100 text-xs text-gray-500 flex justify-between">
                <span>📅 {{ formatDate(w.date) }}</span>
                <span>👥 Max: {{ w.capacity }}</span>
              </div>
            </div>
          </div>
        </section>

        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Nove radionice</h2>
          </div>
          
          <div v-if="newWorkshops.length === 0" class="text-gray-500 bg-white p-6 rounded-xl border text-center">
            Trenutno nema novih radionica dodanih u zadnjih 48h.
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-for="w in newWorkshops" :key="w.id" class="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-blue-100 p-5 shadow-sm">
              <span class="text-xs font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded">Novo</span>
              <h3 class="font-bold text-lg text-gray-900 mt-2">{{ w.title }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ w.description }}</p>
              <p class="text-blue-600 text-xs font-medium mt-3">📅 Održava se: {{ formatDate(w.date) }}</p>
            </div>
          </div>
        </section>

        <section>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-green-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-gray-800">Dostupne radionice</h2>
          </div>
          
          <div v-if="availableWorkshops.length === 0" class="text-gray-500 bg-white p-6 rounded-xl border text-center">
            Trenutno nema drugih dostupnih radionica za prijavu.
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="w in availableWorkshops" :key="w.id" class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col justify-between hover:border-green-300 transition">
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

export default {
  name: 'ProfilesView',
  data() {
    return {
      username: localStorage.getItem('username') || 'Korisnice',
      myWorkshops: [],
      newWorkshops: [],
      availableWorkshops: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    // Čim se stranica učita, povuci podatke sa backenda
    this.fetchDashboardData()
  },
  methods: {
    // Pomagač za kreiranje Authorization zaglavlja sa tokenom
    getAuthHeaders() {
      const token = localStorage.getItem('token')
      return { headers: { Authorization: `Bearer ${token}` } }
    },

    // Povlačenje podataka za sve tri sekcije (GIS4-19, GIS4-21, GIS4-22)
    async fetchDashboardData() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('http://localhost:8000/profiles/dashboard', this.getAuthHeaders())
        
        // Raspoređujemo podatke koje nam vraća naš FastAPI backend
        this.myWorkshops = response.data.my_workshops
        this.newWorkshops = response.data.new_workshops
        this.availableWorkshops = response.data.available_workshops
      } catch (err) {
        console.error('Greška pri učitavanju dashboarda:', err)
        this.error = 'Nije moguće učitati podatke. Provjerite jeste li prijavljeni.'
      } finally {
        this.loading = false
      }
    },

    // Funkcija za brzu prijavu na radionicu sa dashboarda (GIS4-18)
    async handleRegister(workshopId) {
      try {
        const response = await axios.post(
          `http://localhost:8000/profiles/dashboard/register?workshop_id=${workshopId}`, 
          {}, 
          this.getAuthHeaders()
        )
        
        alert(response.data.message || 'Uspješno ste se prijavili na radionicu!')
        // Ponovo učitaj podatke kako bi se radionica odmah prebacila u "Moje radionice"
        this.fetchDashboardData()
      } catch (err) {
        const errorMsg = err.response?.data?.detail || 'Greška pri prijavi na radionicu.'
        alert(errorMsg)
      }
    },

    // Formatiranje datuma u čitljiv oblik (npr. 15.05.2026. 18:00)
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