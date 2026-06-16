<template>
  <div class="p-1">
    <div v-if="dashboardError" class="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-center text-sm">
      {{ dashboardError }}
    </div>

    <div v-if="userRole === 'member'">
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Dashboard</h2>
        <p class="text-gray-500 text-sm mt-1">Pregled vaših radionica</p>
      </div>

      <section class="mb-8">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-2 h-6 bg-violet-500 rounded-full"></div>
          <h3 class="text-xl font-bold text-gray-800">Moje radionice</h3>
        </div>
        <div v-if="myWorkshops.length === 0"
             class="bg-white border border-dashed border-gray-300 rounded-xl p-8 text-center text-gray-500 text-sm">
          Niste prijavljeni ni na jednu radionicu.
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

      <section class="mb-8">
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
          <h3 class="text-xl font-bold text-gray-800">Nove radionice</h3>
        </div>
        <div v-if="newWorkshops.length === 0"
             class="bg-white border border-gray-200 rounded-xl p-6 text-center text-gray-500 text-sm">
          Trenutno nema novih radionica.
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

      <section>
        <div class="flex items-center space-x-2 mb-4">
          <div class="w-2 h-6 bg-green-500 rounded-full"></div>
          <h3 class="text-xl font-bold text-gray-800">Dostupne radionice</h3>
        </div>
        <div v-if="availableWorkshops.length === 0"
             class="bg-white border border-gray-200 rounded-xl p-6 text-center text-gray-500 text-sm">
          Trenutno nema dostupnih radionica.
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
                @click="$emit('register', w.id)"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
              >
                Prijavi se
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div v-else-if="userRole === 'mentor'" class="space-y-6">
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Mentorski panel</h2>
        <p class="text-gray-500 text-sm mt-1">Fokusiran na upravljanje edukativnim procesom</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-violet-500 rounded-full"></div>
            <h3 class="text-lg font-bold text-gray-800">Moje studentice</h3>
          </div>
          <div v-if="myStudents.length === 0"
               class="bg-gray-50 border border-dashed border-gray-300 rounded-xl p-6 text-center text-gray-500 text-sm">
            Trenutno nemate dodijeljenih studentica.
          </div>
          <div v-else class="space-y-3">
            <div v-for="s in myStudents" :key="s.id"
                 class="bg-violet-50 rounded-lg p-3 border border-violet-100">
              <p class="font-semibold text-gray-800 text-sm">{{ s.student_name }}</p>
              <p class="text-gray-500 text-xs">{{ s.student_email }}</p>
            </div>
          </div>
        </section>

        <section class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-purple-400 rounded-full"></div>
            <h3 class="text-lg font-bold text-gray-800">Zahtjevi mentoringa</h3>
          </div>
          <div v-if="mentorRequests.length === 0"
               class="bg-gray-50 border border-dashed border-gray-300 rounded-xl p-6 text-center text-gray-500 text-sm">
            Nema novih zahtjeva za mentorstvo.
          </div>
          <div v-else class="space-y-3">
            <div v-for="r in mentorRequests" :key="r.id"
                 class="bg-purple-50 rounded-lg p-3 border border-purple-100">
              <p class="font-semibold text-gray-800 text-sm">{{ r.student_name }}</p>
              <p class="text-gray-600 text-xs mt-1">{{ r.message }}</p>
              <p class="text-gray-400 text-xs mt-2">{{ formatDate(r.created_at) }}</p>
              <div class="flex gap-2 mt-3">
                <button @click="$emit('accept-request', r.id)"
                        class="bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-lg text-xs font-medium transition">
                  Prihvati
                </button>
                <button @click="$emit('reject-request', r.id)"
                        class="bg-red-100 hover:bg-red-200 text-red-700 px-3 py-1.5 rounded-lg text-xs font-medium transition">
                  Odbij
                </button>
              </div>
            </div>
          </div>
        </section>

        <section class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm md:col-span-2">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
            <h3 class="text-lg font-bold text-gray-800">Radionice na kojima ste mentor/ica</h3>
          </div>
          <div class="bg-gray-50 border border-dashed border-gray-300 rounded-xl p-6 text-center text-gray-500 text-sm">
            Niste angažovani kao mentor/ica na trenutnim radionicama.
          </div>
        </section>
      </div>
    </div>

    <div v-else-if="userRole === 'admin'" class="space-y-6">
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Admin</h2>
        <p class="text-gray-500 text-sm mt-1">Glavni panel za upravljanje platformom</p>
      </div>
      </div>
  </div>
</template>

<script>

import { getAllUsers } from '../services/api.js'

export default {
  name: 'DashboardTab',

  props: {
    userRole: { type: String, default: 'member' },
    myWorkshops: { type: Array, default: () => [] },
    newWorkshops: { type: Array, default: () => [] },
    availableWorkshops: { type: Array, default: () => [] },
    dashboardError: { type: String, default: null },
    myStudents: { type: Array, default: () => [] },
    mentorRequests: { type: Array, default: () => [] },
    mentorDashboardError: { type: String, default: null }
  },

  emits: ['register','accept-request', 'reject-request'],

  data() {
    return {
      stats: {
        total: 0,
        active: 0,
        inactive: 0,
        roles: { member: 0, mentor: 0, admin: 0 }
      }
    }
  },


  async mounted() {
    if (this.userRole === 'admin') {
      try {
        const token = localStorage.getItem('token')
        const users = await getAllUsers(token)
        
        this.stats.total = users.length
        this.stats.active = users.filter(u => u.is_active !== false).length
        this.stats.inactive = users.filter(u => u.is_active === false).length
        
        this.stats.roles.member = users.filter(u => u.role === 'member').length
        this.stats.roles.mentor = users.filter(u => u.role === 'mentor').length
        this.stats.roles.admin = users.filter(u => u.role === 'admin').length
      } catch (err) {
        console.error('Greška pri učitavanju statistike za admin dashboard:', err)
      }
    }
  },


  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('bs-BA', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    }
  }
}
</script>