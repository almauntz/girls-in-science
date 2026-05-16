<template>
  <aside class="w-64 min-h-screen bg-white border-r border-gray-100 shadow-sm flex flex-col">
    
    <!-- Logo -->
    <div class="p-6 border-b border-gray-100">
      <h1 class="text-lg font-bold text-gray-800">Girls in Science</h1>
    </div>

    <!-- Avatar sekcija -->
    <div class="flex flex-col items-center py-6 border-b border-gray-100">

      <div class="relative cursor-pointer group" @click="$refs.fileInput.click()">

        <img
          v-if="avatarUrl"
          :src="avatarUrl"
          alt="Profilna slika"
          class="w-16 h-16 rounded-full object-cover"
        />
        <div
          v-else
          class="w-16 h-16 rounded-full bg-violet-100 
                 flex items-center justify-center text-3xl"
        >
          👤
        </div>

        <div
          v-if="isUploading"
          class="absolute inset-0 rounded-full bg-black 
                 bg-opacity-40 flex items-center justify-center"
        >
          <span class="text-white text-xs">...</span>
        </div>

        <div
          v-else
          class="absolute inset-0 rounded-full bg-black bg-opacity-0 
                 group-hover:bg-opacity-20 transition-all duration-200 
                 flex items-center justify-center"
        >
          <span class="text-white text-xs opacity-0 group-hover:opacity-100">
            Promijeni
          </span>
        </div>

      </div>

      <input
        ref="fileInput"
        type="file"
        accept=".jpg,.jpeg,.png"
        class="hidden"
        @change="handleAvatarChange"
      />

      <p class="text-sm font-semibold text-gray-800 mt-3">
        {{ fullName || username }}
      </p>
      <p class="text-xs text-gray-400 mt-0.5" v-if="field">
        {{ field }}
      </p>

      <p v-if="avatarError" class="text-red-500 text-xs mt-2 text-center px-3">
        {{ avatarError }}
      </p>

    </div>

    <!-- Navigacija -->
    <nav class="flex-1 p-4 space-y-1">
      
      <button
        @click="$emit('tab-change', 'profil')"
        :class="[
          'w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-all flex items-center gap-3',
          activeTab === 'profil'
            ? 'bg-violet-50 text-violet-700 border border-violet-200'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
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
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
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

  emits: ['tab-change', 'avatar-uploaded'],

  data() {
    return {
      isUploading: false,
      avatarError: '',
      username: localStorage.getItem('username') || 'Korisnice'
    }
  },

  methods: {
    async handleAvatarChange(event) {
      const file = event.target.files[0]
      if (!file) return

      this.isUploading = true
      this.avatarError = ''

      try {
        const token = localStorage.getItem('token')
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail)
        }

        const data = await response.json()
        this.$emit('avatar-uploaded', data.avatar_url)  // ← šalje URL roditeljskoj komponenti

      } catch (error) {
        this.avatarError = error.message || 'Greška pri uploadu slike.'
      } finally {
        this.isUploading = false
        event.target.value = ''
      }
    }
  }
}
</script>