<template>
  <div id="app">
    <NavBar />
    <!-- Rejected mentor notification banner -->
    <div
      v-if="showRejectedBanner"
      class="bg-red-50 border-b border-red-200 px-4 py-3 flex items-center justify-between"
    >
      <div class="flex items-center gap-2 text-red-700 text-sm">
        <span>⚠️</span>
        <span>Vaša prijava za mentoricu je odbijena.</span>
        <span v-if="rejectionReason" class="text-red-600">Razlog: <strong>{{ rejectionReason }}</strong></span>
      </div>
      <div class="flex items-center gap-3">
        <router-link
          to="/mentoring/my-application-status"
          class="text-xs font-semibold px-3 py-1.5 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
        >
          Pošalji ponovo
        </router-link>
        <button @click="dismissRejectedBanner" class="text-red-400 hover:text-red-600 text-lg leading-none">×</button>
      </div>
    </div>
    <!-- Approved mentor notification banner -->
    <div
      v-if="showApprovedBanner"
      class="bg-green-50 border-b border-green-200 px-4 py-3 flex items-center justify-between"
    >
      <div class="flex items-center gap-2 text-green-700 text-sm">
        <span>✅</span>
        <span>Čestitamo! Vaša prijava za mentoricu je <strong>prihvaćena</strong>. Sada ste aktivna mentorica na platformi.</span>
      </div>
      <button @click="dismissApprovedBanner" class="text-green-400 hover:text-green-600 text-lg leading-none">×</button>
    </div>
    <main class="main-content">
      <router-view />
    </main>
    <FooterBar />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'

const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'App',
  components: { NavBar, FooterBar },
  data() {
    return {
      showRejectedBanner: false,
      showApprovedBanner: false,
      rejectionReason: null
    }
  },
  async mounted() {
    await this.checkMentorStatus()
  },
  methods: {
    dismissApprovedBanner() {
      this.showApprovedBanner = false
      localStorage.setItem('approved_banner_dismissed', 'true')
    },
    dismissRejectedBanner() {
      this.showRejectedBanner = false
      localStorage.setItem('rejected_banner_dismissed', 'true')
    },
    async checkMentorStatus() {
      const token = localStorage.getItem('token')
      const role = localStorage.getItem('user_role')
      if (!token || role === 'admin') return
      try {
        const res = await fetch(`${BASE_URL}/mentoring/my-application`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (res.ok) {
          const data = await res.json()
          if (data.status === 'REJECTED' && !localStorage.getItem('rejected_banner_dismissed')) {
            this.rejectionReason = data.rejection_reason || null
            this.showRejectedBanner = true
          } else if (data.status === 'APPROVED' && !localStorage.getItem('approved_banner_dismissed')) {
            this.showApprovedBanner = true
          }
        }
      } catch (e) {}
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f9f9f9;
  color: #333;
}
.main-content {
  /* max-width: 1200px; */
  margin: 0 auto;
  padding: 2rem;
}
.main-content:has(.profile-page) {
  max-width: 100%;
  margin: 0;
  padding: 0;
}
</style>