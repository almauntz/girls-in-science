<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Moj profil</h2>
      <p class="text-gray-500 text-sm mt-1">Uredite svoje podatke</p>
    </div>

    <div class="bg-white rounded-xl shadow-sm p-6 max-w-2xl">

      <div v-if="successMessage"
           class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage"
           class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="saveProfile" class="space-y-5">

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ime i prezime *</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="Unesite ime i prezime"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                   focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
          />
          <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">{{ errors.full_name }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Oblast</label>
          <input
            v-model="form.field"
            type="text"
            placeholder="Npr. Softversko inženjerstvo"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                   focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Biografija</label>
          <textarea
            v-model="form.biography"
            placeholder="Napišite nešto o sebi..."
            rows="4"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                   focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none"
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
            class="w-full bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium
                   hover:bg-violet-700 transition-colors duration-200
                   disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Spremi promjene
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import { getMyProfile, updateProfile } from '../../services/api.js'

export default {
  name: 'ProfileForm',

  emits: ['profile-updated'],

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
      errorMessage: ''
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
        this.$emit('profile-updated', data)  // ← šalje podatke sidebaru
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
        this.$emit('profile-updated', this.form)  // ← ažurira sidebar
        setTimeout(() => { this.successMessage = '' }, 3000)
      } catch (error) {
        this.errorMessage = 'Greška pri čuvanju. Pokušajte ponovo.'
        setTimeout(() => { this.errorMessage = '' }, 3000)
      }
    }
  }
}
</script>