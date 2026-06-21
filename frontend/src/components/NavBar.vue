<template>
  <nav class="bg-white border-b border-gray-100 shadow-sm">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

      <router-link to="/" class="text-xl font-bold text-primary">
        Girls in Science
      </router-link>

      <div class="flex gap-6">
        <router-link to="/workshops" class="text-gray-600 hover:text-primary font-medium transition">Workshops</router-link>
        <router-link to="/mentoring" class="text-gray-600 hover:text-primary font-medium transition">Mentoring</router-link>
        <router-link to="/role-models" class="text-gray-600 hover:text-primary font-medium transition">Role Models</router-link>
        <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium transition">Profili</router-link>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">

          <div class="relative" ref="bellRef">
            <button @click="toggleNotifications" class="relative p-1.5 text-gray-500 hover:text-primary transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 00-5-5.917V4a1 1 0 10-2 0v1.083A6 6 0 006 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span v-if="notifCount > 0"
                class="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs font-bold rounded-full h-4 w-4 flex items-center justify-center leading-none">
                {{ notifCount > 9 ? '9+' : notifCount }}
              </span>
            </button>

            <div v-if="showDropdown"
              class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-100 z-50 overflow-hidden">
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="text-sm font-semibold text-gray-700">Obavještenja</p>
              </div>
              <div v-if="notifications.length === 0" class="px-4 py-6 text-center text-gray-400 text-sm">
                Nema novih obavještenja.
              </div>
              <ul v-else class="max-h-72 overflow-y-auto divide-y divide-gray-50">
                <li v-for="n in notifications" :key="n.id" class="px-4 py-3 hover:bg-gray-50 transition">
                  <p class="text-sm font-semibold text-gray-800">{{ n.workshop ? n.workshop.title : n.title }}</p>
                  <template v-if="n.workshop">
                    <p class="text-xs text-gray-500 mt-1">📅 {{ formatDate(n.workshop.date) }}</p>
                    <p class="text-xs text-gray-500">🪑 Slobodnih mjesta: {{ n.workshop.free_spots }}</p>
                  </template>
                  <p v-else class="text-xs text-gray-500 mt-0.5">{{ n.body }}</p>
                </li>
              </ul>
              <div v-if="notifications.length > 0" class="px-4 py-2 border-t border-gray-100">
                <button @click="clearNotifications" class="w-full text-xs text-red-500 hover:text-red-700 font-medium py-1 transition">
                  Obriši sve
                </button>
              </div>
            </div>
          </div>

          <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logout" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-violet-700 transition">
            Registracija
          </router-link>
        </template>
      </div>

    </div>
  </nav>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NavBar',
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('token'),
      username: localStorage.getItem('username') || 'Profil',
      notifCount: 0,
      notifications: [],
      showDropdown: false,
      pollInterval: null,
    }
  },
  watch: {
    $route() {
      this.isLoggedIn = !!localStorage.getItem('token')
      this.username = localStorage.getItem('username') || 'Profil'
    }
  },
  mounted() {
    if (this.isLoggedIn) {
      this.fetchCount()
      this.pollInterval = setInterval(this.fetchCount, 60000)
    }
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeUnmount() {
    clearInterval(this.pollInterval)
    document.removeEventListener('click', this.handleOutsideClick)
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('token')
      return { headers: { Authorization: `Bearer ${token}` } }
    },
    async fetchCount() {
      try {
        const res = await axios.get('http://localhost:8000/profiles/notifications/count', this.getAuthHeaders())
        this.notifCount = res.data.count
      } catch {}
    },
    async toggleNotifications() {
      if (this.showDropdown) {
        this.showDropdown = false
        return
      }
      try {
        const res = await axios.get('http://localhost:8000/profiles/notifications', this.getAuthHeaders())
        this.notifications = res.data
        this.notifCount = 0
      } catch {
        this.notifications = []
      }
      this.showDropdown = true
    },
    handleOutsideClick(e) {
      if (this.$refs.bellRef && !this.$refs.bellRef.contains(e.target)) {
        this.showDropdown = false
      }
    },
    async clearNotifications() {
      try {
        await axios.delete('http://localhost:8000/profiles/notifications', this.getAuthHeaders())
      } catch {}
      this.notifications = []
      this.notifCount = 0
      this.showDropdown = false
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const d = new Date(dateString)
      return d.toLocaleDateString('bs-BA', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    logout() {
      clearInterval(this.pollInterval)
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('user_role')
      this.$router.push('/login')
    }
  }
}
</script>