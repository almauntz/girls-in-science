<template>
  <aside class="w-64 bg-violet-300 flex flex-col" style="position: sticky; top: 0; align-self: flex-start; min-height: 722px;">
    <div class="m-4 rounded-xl bg-violet-600 p-6 flex flex-col items-center">
      <div class="w-16 h-16 rounded-full bg-violet-400 flex items-center justify-center overflow-hidden mb-3">
        <img v-if="avatarUrl" :src="avatarUrl" alt="Profilna slika" class="w-full h-full object-cover" />
        <span v-else class="text-3xl">👤</span>
      </div>
      <p class="text-sm font-semibold text-white">{{ fullName || username }}</p>
      <p class="text-xs text-violet-200 mt-0.5" v-if="field">{{ field }}</p>
      <span class="mt-3 text-xs font-bold bg-violet-500 text-white px-3 py-1 rounded-full uppercase tracking-wide">
        Studentica
      </span>
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