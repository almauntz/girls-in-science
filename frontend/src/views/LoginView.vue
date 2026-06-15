
<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      
      <h1 class="text-2xl font-bold text-primary mb-2">Prijava</h1>
      <p class="text-gray-500 mb-6">Dobrodošla nazad!</p>

      <div v-if="error" class="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-4 text-sm">
        {{ error }}
      </div>

        <div v-if="isDeactivated" class="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg mb-4 text-sm">
            <p class="font-medium mb-2">Vaš nalog je deaktiviran.</p>
            <button
              v-if="canReactivate"
              @click="reactivateAccount"
              :disabled="reactivateLoading"
              class="bg-violet-600 text-white py-1.5 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition disabled:opacity-50"
            >
              {{ reactivateLoading ? 'Reaktivacija...' : 'Reaktiviraj nalog' }}
            </button>
            <p v-else class="text-sm text-yellow-700 mt-1">Obratite se administratoru za reaktivaciju.</p>
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
      error: null,
      isDeactivated: false,
      reactivateLoading: false,
      canReactivate: false
    }
  },
    methods: {
    async handleLogin() {
      this.loading = true
      this.error = null
      this.isDeactivated = false

      try {
        const response = await loginUser(this.email, this.password)
        localStorage.setItem('token', response.access_token)

        // Check profile status
        const profileResponse = await fetch('http://localhost:8000/profiles/me', {
          headers: { 'Authorization': `Bearer ${response.access_token}` }
        })

        if (profileResponse.status === 403) {
          const data = await profileResponse.json()
          localStorage.removeItem('token')
          this.isDeactivated = true
          this.canReactivate = data.detail?.reactivatable || false
        } else {
          const user = await getMe()
          localStorage.setItem('username', user.full_name)
          localStorage.setItem('user_role', user.role)
          this.$router.push('/profiles')
        }
      } catch (err) {
        this.error = err.data?.detail || err.message || 'Pogrešan email ili lozinka.'
      } finally {
        this.loading = false
      }
    },

    async reactivateAccount() {
      this.reactivateLoading = true
      this.error = null

      try {
        const response = await fetch('http://localhost:8000/profiles/reactivate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email, password: this.password })
        })

        const data = await response.json()

        if (response.ok) {
          localStorage.setItem('token', data.access_token)
          const user = await getMe(data.access_token)
          localStorage.setItem('username', user.full_name)
          this.$router.push('/profiles')
        } else {
          this.error = 'Greška pri reaktivaciji. Pokušajte ponovo.'
          this.isDeactivated = false
        }
      } catch (e) {
        this.error = 'Greška pri reaktivaciji.'
      } finally {
        this.reactivateLoading = false
      }
    }
  }
}

</script>