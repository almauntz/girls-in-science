<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Admin - Pregled Prijava</h1>

    <!-- Odabir radionice -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <label class="block text-lg font-semibold mb-4">Odaberi radionicu:</label>
      <select 
        v-model="selectedWorkshopId"
        @change="loadRegistrations"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="" disabled>-- Odaberi radionicu --</option>
        <option 
          v-for="workshop in workshops" 
          :key="workshop.ID_workshop" 
          :value="workshop.ID_workshop"
        >
          {{ workshop.title }} ({{ new Date(workshop.date).toLocaleDateString('sr-RS') }})
        </option>
      </select>
    </div>

    <!-- Poruka o učitavanju ili greški -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-600">Učitavanje...</p>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8">
      {{ error }}
    </div>

    <!-- Tablica sa prijavama -->
    <div v-if="!loading && selectedWorkshopId && registrations.length > 0" class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-4 border-b" style="background: #ede9fe; border-bottom-color: #ddd6fe;">
        <h2 class="text-xl font-semibold" style="color: #7c3aed;">
          Prijavljeni kandidati ({{ registrations.length }})
        </h2>
      </div>
      
      <table class="w-full">
        <thead class="bg-gray-500 border-b">
          <tr>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">Ime</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">Prezime</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">Email</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">Telefon</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">Iskustvo</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-white">GitHub</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(registration, index) in registrations" 
            :key="registration.id"
            :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-100'"
          >
            <td class="px-6 py-3 text-sm text-gray-900">{{ registration.first_name }}</td>
            <td class="px-6 py-3 text-sm text-gray-900">{{ registration.last_name }}</td>
            <td class="px-6 py-3 text-sm text-gray-900">{{ registration.email }}</td>
            <td class="px-6 py-3 text-sm text-gray-900">{{ registration.phone }}</td>
            <td class="px-6 py-3 text-sm text-gray-600">
              <span v-if="registration.previous_experience" class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                {{ registration.previous_experience }}
              </span>
              <span v-else class="text-xs text-gray-400">-</span>
            </td>
            <td class="px-6 py-3 text-sm">
              <a 
                v-if="registration.github_profile"
                :href="registration.github_profile"
                target="_blank"
                class="text-blue-600 hover:text-blue-800 underline"
              >
                Profil
              </a>
              <span v-else class="text-gray-400">-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Poruka kada nema prijava -->
    <div v-if="!loading && selectedWorkshopId && registrations.length === 0" class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
      Nema prijavljenih kandidata za odabranu radionicu.
    </div>
  </div>
</template>

<script>
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  name: 'RegistrationsView',
  data() {
    return {
      workshops: [],
      registrations: [],
      selectedWorkshopId: '',
      loading: false,
      error: null
    }
  },
  beforeMount() {
    // Provera da li je korisnik ulogovan
    const token = localStorage.getItem('token');
    
    if (!token) {
      this.$router.push('/login');
      return;
    }
  },
  mounted() {
    this.loadWorkshops();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('token');
      return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
    },
    async loadWorkshops() {
      try {
        this.loading = true;
        this.error = null;
        const response = await fetch(`${BASE_URL}/workshops/active`);
        this.workshops = await response.json();
      } catch (err) {
        this.error = 'Greška pri učitavanju radionica: ' + err.message;
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async loadRegistrations() {
      if (!this.selectedWorkshopId) {
        this.registrations = [];
        return;
      }

      try {
        this.loading = true;
        this.error = null;
        const response = await fetch(
          `${BASE_URL}/workshops/${this.selectedWorkshopId}/registrations`,
          { headers: this.getAuthHeaders() }
        );
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Greška pri učitavanju prijava');
        }
        
        this.registrations = await response.json();
      } catch (err) {
        this.error = 'Greška pri učitavanju prijava: ' + err.message;
        console.error(err);
        this.registrations = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
