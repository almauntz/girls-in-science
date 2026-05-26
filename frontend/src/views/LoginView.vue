
<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      
      <h1 class="text-2xl font-bold text-primary mb-2">Prijava</h1>
      <p class="text-gray-500 mb-6">Dobrodošla nazad!</p>

      <div v-if="error" class="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-4 text-sm">
        {{ error }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="tvoj@email.com"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Lozinka</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
          />
        </div>

        <button
          @click="handleLogin"
          :disabled="loading"
          class="bg-primary text-white py-2 rounded-lg hover:bg-violet-700 transition font-medium disabled:opacity-50"
        >
          {{ loading ? 'Prijava...' : 'Prijavi se' }}
        </button>
      </div>

      <p class="text-center text-sm text-gray-500 mt-6">
        Nemaš račun?
        <router-link to="/register" class="text-primary font-medium hover:underline">Registruj se</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { loginUser, getMe } from '../services/api'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = null

      try {
        const response = await loginUser(this.email, this.password)

        if (response.access_token) {
          localStorage.setItem('token', response.access_token)
          
          const user = await getMe(response.access_token)
          
          // DIREKTNA PROVJERA: Ako je korisnica deaktivirana, backend vrati 403 
          // i objekat user NEĆE imati u sebi 'role' ili 'full_name' (ili će imati 'detail' grešku)
          if (!user || user.detail || !user.role) {
            this.error = 'Vaš nalog je deaktiviran. Pristup odbijen.'
            localStorage.removeItem('token') // Brišemo token jer je nevažeći
            this.loading = false
            return // ZAUSTAVLJAMO izvršavanje ovdje, ne damo joj na /profiles!
          }
          
          // Ako je sve u redu i korisnica je aktivna, tek tada spremamo podatke i puštamo je
          localStorage.setItem('username', user.full_name)
          localStorage.setItem('user_role', user.role)
          this.$router.push('/profiles')
          
        } else {
          this.error = 'Pogrešan email ili lozinka.'
        }
      } catch (err) {
        console.error("Uhvaćena greška pri prijavi:", err.message)
        this.error = 'Došlo je do greške na serveru. Pokušajte ponovo.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>