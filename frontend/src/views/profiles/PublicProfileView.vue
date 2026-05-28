<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-2xl mx-auto">

      <!-- Učitavanje -->
      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="text-gray-400 text-sm">Učitavanje...</div>
      </div>

      <!-- Greška -->
      <div v-else-if="error" class="bg-red-50 text-red-600 border border-red-200 rounded-xl px-6 py-4 text-sm">
        {{ error }}
      </div>

      <!-- Profil -->
      <div v-else>
        <!-- Header -->
<div
  class="relative w-full rounded-xl mb-6 overflow-hidden"
  style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%); min-height: 170px;"
>
  
  <div class="absolute w-full left-0 bottom-4 px-6 flex items-end gap-6">

    <div
      class="w-32 h-32 rounded-3xl border-4 border-white bg-violet-400 flex items-center justify-center overflow-hidden shadow-lg flex-shrink-0 cursor-pointer"
      @click="showAvatarModal = true"
    >
      <img
        v-if="profile.avatar"
        :src="`http://localhost:8000${profile.avatar}`"
        alt="Avatar"
        class="w-full h-full object-cover"
      />
      <span v-else class="text-5xl">👤</span>
    </div>

    <div class="mb-2 flex flex-col gap-2">
      <h2 class="text-3xl font-bold text-white leading-none">
        {{ profile.full_name }}
      </h2>

      <div class="flex flex-wrap gap-2 mt-1">

        <div
          v-if="profile.location"
          class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5"
        >
          <span>📍</span>
          {{ profile.location }}
        </div>

        <div
          v-if="profile.field"
          class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5"
        >
          <span>📖</span>
          {{ profile.field }}
        </div>

      </div>
    </div>

  </div>
</div>
      
        <!-- Informacije -->
        <div class="space-y-4">


          <!-- Oblast -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-violet-500">📚</span>
              <h3 class="text-sm font-semibold text-gray-800">Oblast</h3>
            </div>
            <p class="text-sm text-gray-700 px-4 py-3 bg-gray-50 rounded-xl border border-gray-100">
              {{ profile.field || 'Nije uneseno' }}
            </p>
          </div>

          <!-- Email — samo za prijavljene -->
          <div v-if="profile.email" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-violet-500">✉️</span>
              <h3 class="text-sm font-semibold text-gray-800">Email</h3>
            </div>
            <p class="text-sm text-gray-700">{{ profile.email }}</p>
          </div>

          <!-- Biografija -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-violet-500">📖</span>
              <h3 class="text-sm font-semibold text-gray-800">Biografija</h3>
            </div>
            <div class="border-l-4 border-violet-200 pl-4 py-1">
              <p class="text-sm text-gray-600 italic leading-relaxed">
                "{{ profile.biography || 'Nije uneseno' }}"
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
    <!-- Avatar lightbox modal -->
<div v-if="showAvatarModal && profile.avatar" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click="showAvatarModal = false">
  <div class="relative max-w-xs w-full mx-4" @click.stop>
    <button
      @click="showAvatarModal = false"
      class="absolute -top-3 -right-3 w-8 h-8 bg-white text-gray-700 rounded-full flex items-center justify-center text-sm font-bold hover:bg-gray-100 transition-colors z-10"
    >
      ✕
    </button>
    <img
      :src="`http://localhost:8000${profile.avatar}`"
      alt="Avatar"
      class="w-full rounded-2xl shadow-2xl"
    />
  </div>
</div>
  </div>
</template>

<script>
export default {
  name: 'PublicProfileView',

  data() {
    return {
      profile: {},
      isLoading: false,
      error: null,
      showAvatarModal: false
    }
  },

  async mounted() {
    this.isLoading = true
    await this.fetchProfile()
    this.isLoading = false
  },

  methods: {
    async fetchProfile() {
      const userId = this.$route.params.user_id
      const token = localStorage.getItem('token')

      try {
        const headers = {}
        if (token) {
          headers['Authorization'] = `Bearer ${token}`
        }

        const response = await fetch(`http://localhost:8000/profiles/${userId}`, {
          headers
        })

        if (response.status === 404) {
          this.error = 'Korisnica nije pronađena.'
          return
        }

        if (!response.ok) {
          this.error = 'Greška pri učitavanju profila.'
          return
        }

        this.profile = await response.json()

      } catch (e) {
        this.error = 'Nije moguće učitati profil.'
      }
    }
  }
}
</script>