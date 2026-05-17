<template>
  <aside class="w-64 min-h-screen bg-violet-300 border-r border-gray-100 shadow-sm flex flex-col">
    
    <div class="p-6 border-b border-gray-100">
      <h1 class="text-lg font-bold text-gray-800">Girls in Science</h1>
    </div>

    <div class="flex flex-col items-center py-6 border-b border-gray-100">
      <div class="w-16 h-16 rounded-full bg-violet-100 flex items-center justify-center overflow-hidden">
        <img v-if="avatarUrl" :src="avatarUrl" alt="Profilna slika" class="w-full h-full object-cover" />
        <span v-else class="text-3xl">👤</span>
      </div>

      <p class="text-sm font-semibold text-gray-800 mt-3">{{ fullName || username }}</p>
      <p class="text-xs text-black-500 mt-0.5" v-if="field">{{ field }}</p>
    </div>

    <nav class="flex-1 p-4 space-y-1">
      <button
        @click="$emit('tab-change', 'profil')"
        :class="[
          'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
          activeTab === 'profil'
            ? 'bg-violet-50 text-violet-700 border border-violet-200'
            : 'text-violet-600 hover:bg-violet-100 hover:text-violet-800'
        ]"
      >
        <span class="text-lg">👤</span>
        Moj profil
      </button>

      <button
        @click="$emit('tab-change', 'dashboard')"
        :class="[
          'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
          activeTab === 'dashboard'
            ? 'bg-violet-50 text-violet-700 border border-violet-200'
            : 'text-black-600 hover:bg-gray-50 hover:text-gray-800'
        ]"
      >
        <span class="text-lg">📊</span>
        Dashboard
      </button>

      <button
        @click="$emit('tab-change', 'aktivnosti')"
        :class="[
          'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
          activeTab === 'aktivnosti'
            ? 'bg-violet-50 text-violet-700 border border-violet-200'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
        ]"
      >
        <span class="text-lg">⚡</span>
        Aktivnosti
      </button>
    </nav>
  </aside>
</template>

<script>
export default {
  name: 'ProfileSidebar',

  props: {
    activeTab: String,
    fullName: String,
    field: String,
    avatarUrl: String
  },

  emits: ['tab-change'],

  data() {
    return {
      username: localStorage.getItem('username') || 'Korisnice'
    }
  }
}
</script>