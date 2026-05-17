<template>
  <div>

   <!-- HEADER KARTICA -->
<div class="bg-violet-600 rounded-xl p-6 mb-6 flex items-center gap-5 max-w-2xl">
  
  <div class="relative cursor-pointer group flex-shrink-0" @click="$refs.fileInput.click()">
    <div class="w-20 h-20 rounded-full bg-violet-400 flex items-center justify-center overflow-hidden">
      <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" class="w-full h-full object-cover" />
      <span v-else class="text-4xl">👤</span>
    </div>
    <!-- hover overlay s kamera ikonom -->
    <div class="absolute inset-0 rounded-full bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
      <span class="text-white text-xl opacity-0 group-hover:opacity-100">📷</span>
    </div>
    <div v-if="isUploading" class="absolute inset-0 rounded-full bg-black bg-opacity-40 flex items-center justify-center">
      <span class="text-white text-xs">...</span>
    </div>
    <!-- X dugme u uglu -->
    <button
      v-if="avatarUrl"
      type="button"
      @click.stop="handleDeleteAvatar"
      class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-xs transition-colors"
    >
      ✕
    </button>
  </div>

  <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png" class="hidden" @change="handleAvatarChange" />

  <div>
    <h2 class="text-2xl font-bold text-white">{{ fullName || 'Korisnice' }}</h2>
    <p class="text-violet-200 text-sm mt-1">{{ field || 'Oblast nije unesena' }}</p>
    <p v-if="avatarError" class="text-red-200 text-xs mt-2">{{ avatarError }}</p>
  </div>

</div>

    <!-- FORMA -->
    <div class="bg-white rounded-xl shadow-sm p-6 max-w-2xl">

      <div v-if="successMessage" class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="saveProfile" class="space-y-5">

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ime i prezime *</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="Unesite ime i prezime"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
          />
          <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">{{ errors.full_name }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Oblast</label>
          <input
            v-model="form.field"
            type="text"
            placeholder="Npr. Softversko inženjerstvo"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Biografija</label>
          <textarea
            v-model="form.biography"
            placeholder="Napišite nešto o sebi..."
            rows="4"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none"
          ></textarea>
          <div class="flex justify-between mt-1">
            <p v-if="errors.biography" class="text-red-500 text-xs">{{ errors.biography }}</p>
            <span class="text-xs text-gray-400 ml-auto">{{ form.biography?.length || 0 }}/500</span>
          </div>
        </div>

        <div class="pt-2">
          <button
            type="submit"
            :disabled="!isFormValid"
            class="w-full bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Spremi promjene
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import { getMyProfile, updateProfile } from '../services/api.js'

export default {
  name: 'ProfileForm',

  props: {
    fullName: String,
    field: String,
    avatarUrl: String
  },

  emits: ['profile-updated', 'avatar-uploaded', 'avatar-deleted'],

  data() {
    return {
      form: {
        full_name: '',
        biography: '',
        field: ''
      },
      errors: {
        full_name: '',
        biography: ''
      },
      successMessage: '',
      errorMessage: '',
      isUploading: false,
      avatarError: ''
    }
  },

  computed: {
    isFormValid() {
      return (
        this.form.full_name.trim() !== '' &&
        (this.form.biography?.length || 0) <= 500
      )
    }
  },

  async mounted() {
    await this.loadProfile()
  },

  methods: {
    async loadProfile() {
      try {
        const token = localStorage.getItem('token')
        const data = await getMyProfile(token)
        this.form.full_name = data.full_name || ''
        this.form.biography = data.biography || ''
        this.form.field = data.field || ''
        this.$emit('profile-updated', data)
      } catch (error) {
        this.errorMessage = 'Greška pri učitavanju profila.'
      }
    },

    validateForm() {
      this.errors = { full_name: '', biography: '' }
      let isValid = true
      if (!this.form.full_name || this.form.full_name.trim() === '') {
        this.errors.full_name = 'Ime ne smije biti prazno.'
        isValid = false
      }
      if (this.form.biography && this.form.biography.length > 500) {
        this.errors.biography = 'Biografija ne smije biti duža od 500 karaktera.'
        isValid = false
      }
      return isValid
    },

    async saveProfile() {
      if (!this.validateForm()) return
      this.successMessage = ''
      this.errorMessage = ''
      try {
        const token = localStorage.getItem('token')
        await updateProfile(token, {
          full_name: this.form.full_name,
          biography: this.form.biography,
          field: this.form.field
        })
        this.successMessage = 'Promjene su uspješno sačuvane!'
        this.$emit('profile-updated', this.form)
        setTimeout(() => { this.successMessage = '' }, 3000)
      } catch (error) {
        this.errorMessage = 'Greška pri čuvanju. Pokušajte ponovo.'
        setTimeout(() => { this.errorMessage = '' }, 3000)
      }
    },

    async handleAvatarChange(event) {
      const file = event.target.files[0]
      if (!file) return

      this.isUploading = true
      this.avatarError = ''

      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
      if (!allowedTypes.includes(file.type)) {
        this.avatarError = 'Neispravan format! Dozvoljeni su samo JPG i PNG.'
        this.isUploading = false
        event.target.value = ''
        return
      }

      const maxSizeInBytes = 2 * 1024 * 1024
      if (file.size > maxSizeInBytes) {
        this.avatarError = 'Slika je prevelika! Maksimalna veličina je 2MB.'
        this.isUploading = false
        event.target.value = ''
        return
      }

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
        this.$emit('avatar-uploaded', data.avatar_url)

      } catch (error) {
        this.avatarError = error.message || 'Greška pri uploadu slike.'
      } finally {
        this.isUploading = false
        event.target.value = ''
      }
    },

    async handleDeleteAvatar() {
      if (!confirm('Jeste li sigurni da želite obrisati profilnu sliku?')) return

      this.avatarError = ''
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Greška pri brisanju.')
        }

        this.$emit('avatar-deleted')
      } catch (error) {
        this.avatarError = error.message || 'Nije moguće obrisati profilnu sliku.'
      }
    }
  }
}
</script>