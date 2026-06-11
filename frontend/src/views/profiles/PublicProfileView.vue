<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-5xl mx-auto">

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
  <div class="absolute w-full left-0 bottom-4 px-6 flex items-end justify-between">

    <!-- Lijevo: avatar + ime + field -->
    <div class="flex items-end gap-6">
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
        <h2 class="text-3xl font-bold text-white leading-none">{{ profile.full_name }}</h2>
        <div v-if="profile.field"
          class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5 w-fit">
          <span>📖</span>{{ profile.field }}
        </div>
      </div>
    </div>

    <!-- Desno dolje: društvene mreže -->
    <div v-if="profile.linkedin_url || profile.github_url || profile.twitter_url"
      class="flex items-center gap-2 mb-2">
      <a v-if="profile.linkedin_url" :href="profile.linkedin_url" target="_blank"
        class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5 hover:bg-indigo-900/60 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
        </svg>
        LinkedIn
      </a>
      <a v-if="profile.github_url" :href="profile.github_url" target="_blank"
        class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5 hover:bg-indigo-900/60 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
        GitHub
      </a>
      <a v-if="profile.twitter_url" :href="profile.twitter_url" target="_blank"
        class="bg-indigo-900/40 border border-indigo-400/30 text-white text-xs px-3 py-1 rounded-full flex items-center gap-1.5 hover:bg-indigo-900/60 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </svg>
        Twitter (X)
      </a>
    </div>

  </div>
</div>

        <!-- Dvije kolone -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

          <!-- LIJEVA KOLONA -->
          <div class="lg:col-span-2 space-y-4">

            <!-- O meni -->
            <div v-if="profile.biography" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="text-violet-500">👤</span>
                <h3 class="text-sm font-semibold text-gray-800">O meni</h3>
              </div>
              <p class="text-sm text-gray-600 leading-relaxed">{{ profile.biography }}</p>
            </div>

            <!-- Naučno i radno iskustvo -->
            <div v-if="profile.experience && profile.experience.length > 0"
              class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="text-violet-500">💼</span>
                <h3 class="text-sm font-semibold text-gray-800">Naučno i radno iskustvo</h3>
              </div>
              <div v-for="(exp, i) in profile.experience" :key="i"
                class="flex gap-3 py-3 border-b border-gray-100 last:border-b-0 last:pb-0 first:pt-0">
                <div class="mt-1 flex-shrink-0">
                  <div class="w-2.5 h-2.5 rounded-full border-2 border-violet-500"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex justify-between items-start gap-2 flex-wrap">
                    <p class="text-sm font-medium text-gray-800">{{ exp.title }}</p>
                    <span class="text-xs px-2 py-0.5 bg-violet-50 text-violet-600 rounded-full whitespace-nowrap">
                      {{ exp.start_date }} · {{ exp.end_date || 'Trenutno' }}
                    </span>
                  </div>
                  <p class="text-xs text-violet-600 mt-0.5">{{ exp.organization }}</p>
                  <p v-if="exp.location" class="text-xs text-gray-400 flex items-center gap-1 mt-0.5">
                    📍 {{ exp.location }}
                  </p>
                  <p v-if="exp.description" class="text-xs text-gray-500 mt-1.5 leading-relaxed">
                    {{ exp.description }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Akademsko obrazovanje -->
            <div v-if="profile.education && profile.education.length > 0"
              class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-4">
                <span
                class="text-violet-500">📚</span>
                <h3 class="text-sm font-semibold text-gray-800">Akademsko obrazovanje i edukacije</h3>
              </div>
              <div v-for="(edu, i) in profile.education" :key="i"
                class="flex gap-3 py-3 border-b border-gray-100 last:border-b-0 last:pb-0 first:pt-0">
                <div class="mt-1 flex-shrink-0">
                  <div class="w-2.5 h-2.5 rounded-full border-2 border-green-500"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex justify-between items-start gap-2 flex-wrap">
                    <p class="text-sm font-medium text-gray-800">{{ edu.degree }}</p>
                    <span class="text-xs px-2 py-0.5 bg-green-50 text-green-700 rounded-full whitespace-nowrap">
                      {{ edu.start_date }} · {{ edu.end_date || 'Trenutno' }}
                    </span>
                  </div>
                  <p class="text-xs text-green-600 mt-0.5">{{ edu.institution }}</p>
                  <p v-if="edu.description" class="text-xs text-gray-500 mt-1.5 leading-relaxed">
                    {{ edu.description }}
                  </p>
                </div>
              </div>
            </div>

          </div>

          <!-- DESNA KOLONA -->
          <div class="lg:col-span-1 space-y-4">

            <!-- Jezici + Vještine -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">

              <!-- Jezici -->
              <div v-if="profile.languages && profile.languages.length > 0">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-violet-500">🌐</span>
                  <h3 class="text-sm font-semibold text-gray-800">Jezici</h3>
                </div>
                <div v-for="(lang, i) in profile.languages" :key="i" class="mb-3 last:mb-0">
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-sm text-gray-700">{{ lang.name }}</span>
                    <span class="text-xs text-gray-400">{{ lang.level }}</span>
                  </div>
                </div>
              </div>

              <!-- Divider samo ako ima i jezike i vještine -->
              <div v-if="profile.languages && profile.languages.length > 0 && profile.skills && profile.skills.length > 0"
                class="border-t border-gray-100 my-4">
              </div>

              <!-- Vještine -->
              <div v-if="profile.skills && profile.skills.length > 0">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-violet-500">🛠️</span>
                  <h3 class="text-sm font-semibold text-gray-800">Tehničke vještine</h3>
                </div>
                <div class="flex flex-wrap gap-2">
                  <span v-for="(skill, i) in profile.skills" :key="i"
                    class="text-xs px-3 py-1.5 bg-violet-50 text-violet-700 border border-violet-100 rounded-full">
                    {{ skill }}
                  </span>
                </div>
              </div>

            </div>

            <!-- Kontakt podaci -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="text-violet-500">✉️</span>
                <h3 class="text-sm font-semibold text-gray-800">Kontakt podaci</h3>
              </div>
              <div v-if="profile.email" class="flex items-start gap-3 py-2 border-b border-gray-100">
                <div class="w-7 h-7 rounded-lg bg-violet-50 flex items-center justify-center flex-shrink-0">
                  <span class="text-xs">✉️</span>
                </div>
                <div>
                  <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Email adresa</p>
                  <p class="text-sm text-gray-700 mt-0.5">{{ profile.email }}</p>
                </div>
              </div>
              <div v-if="profile.location" class="flex items-start gap-3 py-2">
                <div class="w-7 h-7 rounded-lg bg-violet-50 flex items-center justify-center flex-shrink-0">
                  <span class="text-xs">📍</span>
                </div>
                <div>
                  <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Lokacija</p>
                  <p class="text-sm text-gray-700 mt-0.5">{{ profile.location }}</p>
                </div>
              </div>
              <div v-if="!profile.email && !profile.location"
                class="text-sm text-gray-400 italic">Nema kontakt podataka.</div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Avatar lightbox modal -->
    <div v-if="showAvatarModal && profile.avatar"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      @click="showAvatarModal = false">
      <div class="relative max-w-xs w-full mx-4" @click.stop>
        <button @click="showAvatarModal = false"
          class="absolute -top-3 -right-3 w-8 h-8 bg-white text-gray-700 rounded-full flex items-center justify-center text-sm font-bold hover:bg-gray-100 transition-colors z-10">
          ✕
        </button>
        <img :src="`http://localhost:8000${profile.avatar}`" alt="Avatar" class="w-full rounded-2xl shadow-2xl" />
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
        if (token) headers['Authorization'] = `Bearer ${token}`
        const response = await fetch(`http://localhost:8000/profiles/${userId}`, { headers })
        if (response.status === 404) { this.error = 'Korisnica nije pronađena.'; return }
        if (!response.ok) { this.error = 'Greška pri učitavanju profila.'; return }
        this.profile = await response.json()
      } catch (e) {
        this.error = 'Nije moguće učitati profil.'
      }
    },

    levelToPercent(level) {
      const map = {
        'Maternji': 100, 'C2': 95, 'C1': 85,
        'B2': 70, 'B1': 55, 'A2': 35, 'A1': 20
      }
      return map[level] || 50
    }
  }
}
</script>