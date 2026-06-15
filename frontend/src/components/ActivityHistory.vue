<template>
  <div class="space-y-6">

    <div class="bg-white rounded-2xl shadow-sm p-6">
      <div class="flex items-center gap-2 mb-6">
        <span class="text-violet-500 text-lg">⚡</span>
        <h2 class="text-base font-semibold text-gray-800">Historija aktivnosti</h2>
      </div>

      <div v-if="isLoading" class="text-sm text-gray-400 text-center py-16">
        Učitavanje...
      </div>

      <div v-else-if="errorMessage" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 text-sm">
        {{ errorMessage }}
      </div>

      <div v-else-if="workshops.length === 0" class="flex flex-col items-center justify-center py-16 text-center">
        <span class="text-4xl mb-3">📭</span>
        <p class="text-sm font-medium text-gray-500">Nemate evidentiranih radionica.</p>
        <p class="text-xs text-gray-400 mt-1">Radionice na kojima ste prisustvovali pojaviće se ovdje.</p>
      </div>

      <ul v-else class="space-y-3">
        <li
          v-for="workshop in workshops"
          :key="workshop.id"
          class="flex items-start justify-between border border-gray-100 rounded-xl px-5 py-4 bg-gray-50 hover:bg-violet-50 hover:border-violet-100 transition-colors"
        >
          <div class="flex flex-col gap-1 flex-1 min-w-0 mr-4">
            <span class="text-sm font-semibold text-gray-800 truncate">{{ workshop.title }}</span>
            <span class="text-xs text-gray-400">{{ formatDate(workshop.date) }}</span>
            <span v-if="workshop.description" class="text-xs text-gray-500 line-clamp-2 mt-0.5">{{ workshop.description }}</span>
          </div>
          <span class="flex-shrink-0 text-xs font-medium px-3 py-1 rounded-full bg-green-100 text-green-700 mt-0.5">
            Završena
          </span>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ActivityHistory',

  data() {
    return {
      workshops: [],
      isLoading: false,
      errorMessage: ''
    }
  },

  async mounted() {
    await this.fetchHistory()
  },

  methods: {
    async fetchHistory() {
      this.isLoading = true
      this.errorMessage = ''
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/profiles/me/history', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!response.ok) throw new Error('Greška pri učitavanju historije.')
        this.workshops = await response.json()
      } catch (e) {
        this.errorMessage = e.message || 'Nije moguće učitati historiju radionica.'
      } finally {
        this.isLoading = false
      }
    },

    formatDate(dateStr) {
      const d = new Date(dateStr)
      return d.toLocaleDateString('bs-BA', { day: '2-digit', month: '2-digit', year: 'numeric' })
    }
  }
}
</script>
